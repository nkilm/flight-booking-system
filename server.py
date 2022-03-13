from socket import socket
from pyfiglet import figlet_format
from simple_chalk import chalk 

PORT = 7070
LISTENERS = 5

s_socket = socket()

s_socket.bind(('localhost',PORT))
print(f"Server started. Listening on PORT {PORT}")

s_socket.listen(LISTENERS)
    

while True:
    c_socket,addr = s_socket.accept()
    print(f"Connected with {addr}")

    # sending info to client
    welcome_msg = chalk.green(figlet_format("Flight Booking",font="slant"))
    c_socket.send(bytes(welcome_msg,"utf-8"))

    quote = " ".join(["\t\t","  ",chalk.whiteBright("Let Your"),chalk.cyanBright.bold("Dreams"),chalk.whiteBright("take a"),chalk.cyanBright.bold("Flight"),"\U00002708\n\n"])
    c_socket.send(bytes(quote,"utf-8"))
    
    booking_info_client = c_socket.recv(1024).decode()
    print(booking_info_client)

    print("\nAvailable Flights:\n")

    c_socket.close()