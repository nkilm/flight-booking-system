from socket import socket 

c_socket = socket()

print("Connecting to server...")

c_socket.connect(('localhost',6060))

server_res = c_socket.recv(1024).decode()

print(f"SERVER: {server_res}")

src = input("Enter Source:")
dest = input("Enter destination: ")
date = input("Enter date of journey: ")

c_socket.send(bytes(src,'utf-8'))
c_socket.send(bytes(dest,'utf-8'))
c_socket.send(bytes(date,'utf-8'))

















