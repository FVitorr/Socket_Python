import socket
import tqdm
import os

class serveOn:
    def __init__(self,host = '120.0.0.1',port = 22):
        HOST = host             # Endereco IP do Servidor
        PORT = port          # Porta que o Servidor esta
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPERATOR>"
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)
        tcp.bind(orig)
        tcp.listen(3)
        print(f"[*] Listening as {HOST}:{PORT}")

        self.con, self.cliente = tcp.accept()
        print(f"[+] {self.cliente} is connected.")

    def recived_file(self):
        con = self.con        
        received  = con.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = con.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                #progress.update(len(bytes_read))

        # close the client socket

    def send_file(self,filename,file_size):
        con = self.con
        con.send (f"{filename}{self.SEPARATOR}{file_size}".encode())
        print("<- CRTL-X end connecting ->")

        # start sending the file
        progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                con.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket



