from socket import socket 
from subprocess import run
from simple_chalk import chalk

c_socket = socket()

c_socket.connect(('localhost',6060))

welcome_res = c_socket.recv(1024).decode()
quote_res = c_socket.recv(1024).decode()

# clear screen
run('clear',shell=True)
print(welcome_res)
print(quote_res)

src = input("Enter Source:")
dest = input("Enter destination: ")
date = input("Enter date of journey: ")

c_socket.send(bytes(src,'utf-8'))
c_socket.send(bytes(dest,'utf-8'))
c_socket.send(bytes(date,'utf-8'))