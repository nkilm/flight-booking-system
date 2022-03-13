import inquirer
import re
from socket import socket 
from subprocess import run
from simple_chalk import chalk
from inquirer.themes import GreenPassion
from datetime import datetime
import validation

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

booking_info["date"] = datetime.strptime(booking_info.get("date"), "%d/%m/%Y").strftime("%Y/%m/%d")

c_socket.send(bytes(str(booking_info),'utf-8'))