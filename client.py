import inquirer
import socket 
from subprocess import run
from simple_chalk import chalk
from inquirer.themes import GreenPassion
from datetime import datetime
import validation
from json import dumps,loads
import os,sys

# Add modules path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "airline"))
from airline.amadeus_python import display,display_confirmation_price

try:
    c_socket = socket.socket()

    c_socket.connect(('localhost',7070))

    welcome_response = c_socket.recv(1024).decode()
    quote_response = c_socket.recv(1024).decode()

    # clear screen
    run('clear',shell=True)

    print(welcome_response)
    print(quote_response)

    questions = [
        inquirer.Text("src", message="Enter the Source",validate=validation.location_code_validation),
        inquirer.Text("dest", message="Enter the Destination",validate=validation.location_code_validation),
        inquirer.Text("date", message="Enter the Journey Date",validate=validation.date_validation),
        inquirer.Text("adults", message="How many Passengers?",validate=validation.check_number)
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

    run('clear',shell=True)
    display_confirmation_price(desired_flight)

    booking = [
        inquirer.List("booking_res",message=chalk.white.bold("Do you want to book the selected Flight?"),choices=['YES','NO'])
    ]

    booking_res = inquirer.prompt(booking,theme=GreenPassion())
    run("clear",shell=True)
    if(booking_res['booking_res']=="YES"):
        print(chalk.green.bold("Flight Booked"))
    else:
        print(chalk.red.bold("Flight Not Booked"))

# System related error
except socket.error as error: # equivalent to OSError
    print(chalk.red(error))

# address related error 
except socket.herror as error:
    print(chalk.red(error))

# catch timeout error
except socket.timeout as time_out_error:
    print(chalk.red(time_out_error))