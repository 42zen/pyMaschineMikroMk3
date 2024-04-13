import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_address = ('localhost', 7777)
print('connecting to', server_address)
client_socket.connect(server_address)

while True:
    data = client_socket.recv(1024)
    print('received', data.decode())