import socket
#import tqdm
import os

HOST = '127.0.0.1'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
BUFFER_SIZE = 4096
SEPARATOR = "<SEPERATOR>"
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
print(f"[*] Listening as {HOST}:{PORT}")

con, cliente = tcp.accept()
print(f"[+] {cliente} is connected.")
    
received  = con.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
#progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
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
print ('\nFinalizando conexao do cliente', cliente)
con.close()

