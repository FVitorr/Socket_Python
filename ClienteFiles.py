import socket
import tqdm
import os

SEPARATOR = "<SEPERATOR>"
host = '127.0.0.1'     # Endereco IP do Servidor
porta = 5000            # Porta que o Servidor esta
BUFFER_SIZE = 4096

#NOME FILE
while(True):
    filename = str(input("Path File:"))
    try:
        file_size = os.path.getsize(filename)
        break
    except:
        print("<-- File not found -->")

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, porta)
print(f"Connecting to {host}:{porta}")
tcp.connect(dest)

tcp.send (f"{filename}{SEPARATOR}{file_size}".encode())
print("<- CRTL-X end connecting ->")

# start sending the file
progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        tcp.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
tcp.close()
