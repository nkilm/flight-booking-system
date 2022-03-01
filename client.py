from socket import socket 

c_socket = socket()

print("Connecting to server...")

c_socket.connect(('localhost',6060))

server_res = c_socket.recv(1024).decode()

print(f"SERVER: {server_res}")

















