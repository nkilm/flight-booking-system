import inquirer
from socket import socket 
from subprocess import run
from simple_chalk import chalk
from inquirer.themes import GreenPassion
from datetime import datetime
import validation
from json import dumps,loads
import os,sys

sys.path.append(os.path.join(os.path.dirname(__file__), "airline"))
from airline.amadeus_python import display,display_confirmation_price

c_socket = socket()

c_socket.connect(('localhost',7070))

welcome_response = c_socket.recv(1024).decode()
quote_response = c_socket.recv(1024).decode()

# clear screen
run('clear',shell=True)

print(welcome_response)
print(quote_response)

questions = [
    inquirer.Text("src", message="Enter the Source"),
    inquirer.Text("dest", message="Enter the Destination"),
    inquirer.Text("date", message="Enter the Journey Date",validate=validation.date_validation),
    inquirer.Text("adults", message="How many Passengers?")
]

booking_info = inquirer.prompt(questions, theme=GreenPassion())

booking_info["date"] = datetime.strptime(booking_info.get("date"), "%d/%m/%Y").strftime("%Y-%m-%d")

# send the booking info the socket of the server 
c_socket.send(bytes(str(dumps(booking_info)),'utf-8'))

flights = loads(c_socket.recv(int(5e+6)).decode())
display(flights)

print("\n")
id = [
    inquirer.Text("id",message="Enter the corresponding ID of the Flight you want to book")
]

flight_id = inquirer.prompt(id,theme=GreenPassion())

# send flight id to server
c_socket.send(bytes(str(flight_id["id"]),'utf-8'))

desired_flight = loads(c_socket.recv(int(2e+6)).decode())

display_confirmation_price(desired_flight)
