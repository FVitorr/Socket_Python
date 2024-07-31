import socket
import tqdm
import os

class ClientOn:
    def __init__(self, HOST = '127.0.0.1', PORT = 1451 ) -> None:
        self.SEPARATOR = "<SEPARATOR>"
        self.HOST = HOST  # Endereço IP do Servidor
        self.PORT = PORT             # Porta que o Servidor está
        self.BUFFER_SIZE = 4096

        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.HOST, self.PORT)
        self.tcp.connect(dest)
        print(f"[+] Connected to {self.HOST}:{self.PORT}")

    def send_file(self, filename):
        con = self.tcp
        file_size = os.path.getsize(filename)
        con.send(f"{filename}{self.SEPARATOR}{file_size}".encode())
        print(f"<- Sending file {filename} ->")

        # Inicializa a barra de progresso
        progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                con.sendall(bytes_read)
                progress.update(len(bytes_read))

        print(f"[+] File {filename} sent successfully.")
        con.close()

    def receive_file(self):
        con = self.tcp        
        received = con.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # Inicializa a barra de progresso
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                bytes_read = con.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

        print(f"[+] File {filename} received successfully.")
        con.close()

# Exemplo de uso
if __name__ == "__main__":
    client = ClientOn()
    # Para enviar um arquivo:
    # client.send_file("path/to/file")
    # Para receber um arquivo:
    client.receive_file()
