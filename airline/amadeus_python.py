from amadeus import Client, ResponseError
from dotenv import load_dotenv
from os import environ
from texttable import Texttable
from currency_converter import CurrencyConverter
from simple_chalk import chalk
import sys,os

load_dotenv()

amadeus = Client(
    client_id=environ.get("API_KEY"),
    client_secret=environ.get("API_SECRET")
)


def display(res):
    try:
      table = Texttable(max_width=0)
      table.add_row([
        'ID',
        'Seats',
        'Duration',
        'Oneway?',
        'Departure',
        'Arrival',
        'Price(inc. of Taxes)',
        'Last Ticketing Date'
        ])
      table.set_cols_align(["c", "c", "c", "c", "c","c","c"])
      curr = CurrencyConverter()

      for i in res:
        id = i.get("id")
        seats = i.get("numberOfBookableSeats")
        duration = i.get("itineraries")[0]["duration"]
        last_ticketing_date = i.get("lastTicketingDate")
        price = i.get("price").get("grandTotal")
        price_inr = chalk.green(f"₹{round(curr.convert(price, 'EUR', 'INR'),2)}")

        oneway = "No" if i.get("oneWay") == 0 else "Yes"

        departure = ""
        arrival = ""

        for j in i.get("itineraries")[0]["segments"]:
          departure += j["departure"]["iataCode"] + " " + \
              " ".join(j["departure"]["at"].split("T")) + "\n"
          arrival += j["arrival"]["iataCode"] + " " + \
              " ".join(j["arrival"]["at"].split("T")) + "\n"
        table.add_row([id, seats, duration, oneway, departure,
                      arrival, price_inr, last_ticketing_date])

      print(table.draw())
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(chalk.red.bold(exc_type, fname, exc_tb.tb_lineno))

def check_flights(src, dest, date, adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
        originLocationCode=src.upper(),
        destinationLocationCode=dest.upper(),
        departureDate=date,
        adults=adults).data
        return response

    except ResponseError as error:
        return error


def display_confirmation_price(conf_price_res):
    try:
      table = Texttable(max_width=0)
      curr = CurrencyConverter()
      for i in conf_price_res.items():
          print(i)
          
    except ResponseError as error:
      print(chalk.red.bold(f"Error in displaying confirmation price {error}"))
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(chalk.red.bold(exc_type, fname, exc_tb.tb_lineno))


def confirm_price(flight_obj):
    try:
      return amadeus.shopping.flight_offers.pricing.post(flight_obj,include='credit-card-fees,other-services').data
    except ResponseError as error:
      print(chalk.red.bold(f"Error: {error}"))

def book_flight(flight_obj):
    # The flight ID comes from the Flight Create Orders (in test environment it's temporary)
    # Retrieve the order based on it's ID
    flight_booking = amadeus.booking.flight_orders.post(flight_obj).data
    amadeus.booking.flight_order(flight_booking['id']).get()

    # Delete the order based on it's ID
    amadeus.booking.flight_order(flight_booking['id']).delete()