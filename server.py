from socket import socket 

PORT = 6060
LISTENERS = 5

s_socket = socket()

s_socket.bind(('localhost',PORT))
print(f"Server started. Listening on PORT {PORT}")

s_socket.listen(LISTENERS)

while True:
    c_socket,addr = s_socket.accept()
    print(f"Connected with {addr}")

    # sending info to client
    c_socket.send(bytes("STATUS 200 OK","utf-8"))

    print("##############################################################")
    print("----------------------Flight Booking--------------------------")
    print("##############################################################")
    src = c_socket.recv(1024).decode()
    dest = c_socket.recv(1024).decode()
    date = c_socket.recv(1024).decode()
    print(f"Source: {src}\nDestination: {dest}\nDate Of Journey: {date}")

    print("\nAvailable Flights:\n")
    print("foobarbaz")

    c_socket.close()
