from socket import socket
from pyfiglet import figlet_format
from simple_chalk import chalk 
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), "airline"))
from airline.amadeus_python import check_flights,confirm_price
from json import loads,dumps

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
    
    booking_info_client = loads(c_socket.recv(1024).decode())
    print(booking_info_client)

    src = booking_info_client.get("src")
    dest = booking_info_client.get("dest")
    date = booking_info_client.get("date")
    adults = booking_info_client.get("adults")

    res = check_flights(src,dest,date,adults)

    c_socket.send(bytes(str(dumps(res)),"utf-8"))

    id = c_socket.recv(1024).decode()

    desired_flight = list(filter(lambda flight:flight["id"]=="5",res))

    print("desired Flight\n",desired_flight)

    price_conf_res = confirm_price(desired_flight)
    c_socket.send(bytes(str(dumps(price_conf_res)),"utf-8"))

    c_socket.close()