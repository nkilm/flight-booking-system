import socket
from pyfiglet import figlet_format
from simple_chalk import chalk 
import os,sys

sys.path.append(os.path.join(os.path.dirname(__file__), "airline"))

from airline.amadeus_python import check_flights,confirm_price
from json import loads,dumps

PORT = 7070
LISTENERS = 5

try: 
    s_socket = socket.socket()

    s_socket.bind(('localhost',PORT)) # change 'localhost' to IP Addr to connect different laptops
    print(f"Server started. Listening on PORT {PORT}")

    s_socket.listen(LISTENERS)
except socket.error as error:
    print(chalk.red.bold(error))

except socket.herror as error:
    print(chalk.red.bold(error))

while True:
    try:
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

        desired_flight = list(filter(lambda flight:flight["id"]==id,res))

        print("desired Flight\n",desired_flight)

        price_conf_res = confirm_price(desired_flight)
        c_socket.send(bytes(str(dumps(price_conf_res)),"utf-8"))

        c_socket.close()
    # System related error
    except socket.error as error: # equivalent to OSError
        print(chalk.red(error))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(chalk.red.bold(exc_type, fname, exc_tb.tb_lineno))

    # address related error 
    except socket.herror as error:
        print(chalk.red(error))

    # catch timeout error
    except socket.timeout as time_out_error:
        print(chalk.red(time_out_error))

    except Exception as e:
        print(chalk.red.bold(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(chalk.red.bold(exc_type, fname, exc_tb.tb_lineno))
