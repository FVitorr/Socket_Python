import socket
import tqdm
import os

class ServeOn:
    def __init__(self, host='127.0.0.1', port=1451):
        self.HOST = host             # Endereço IP do Servidor
        self.PORT = port             # Porta que o Servidor está
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"

        # Configura o socket
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen(3)
        print(f"[*] Listening as {self.HOST}:{self.PORT}")

        # Aceita a conexão do cliente
        self.con, self.cliente = self.tcp.accept()
        print(f"[+] {self.cliente} is connected.")

    def receive_file(self):
        con = self.con
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
                    # Se não houver mais dados, o arquivo foi transmitido
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

        print(f"[+] File {filename} received successfully.")
        con.close()

    def send_file(self, filename):
        con = self.con
        file_size = os.path.getsize(filename)
        con.send(f"{filename}{self.SEPARATOR}{file_size}".encode())
        print("<- Sending file ->")

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

# Exemplo de uso
if __name__ == "__main__":
    server = ServeOn()
    # Para receber um arquivo:
    # server.receive_file()
    # Para enviar um arquivo:
    file_path = "/home/vitor/Downloads/BigBuckBunny_640x360.m4v"
    server.send_file(file_path)
