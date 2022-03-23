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
        
        departure = ""
        arrival = ""

        for j in i.get("itineraries")[0]["segments"]:
          departure += j["departure"]["iataCode"] + " " + \
              " ".join(j["departure"]["at"].split("T")) + "\n"
          arrival += j["arrival"]["iataCode"] + " " + \
              " ".join(j["arrival"]["at"].split("T")) + "\n"
        table.add_row([id, seats, duration, departure,
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
    conf_price_res = conf_price_res.get("flightOffers")[0]
    try:
      table = Texttable(max_width=0)
      curr = CurrencyConverter()
      table.add_row([
        'Bookable Seats',
        'Duration', 
        'Departure',
        'Arrival',
        'Price(inc. of Taxes)',
        'Last Ticketing Date'
      ])
      last_date = conf_price_res.get("lastTicketingDate")
      seats = conf_price_res.get("numberOfBookableSeats")
      print(seats)
      duration = [i["duration"] for i in conf_price_res.get("itineraries")[0]["segments"]]
      price = conf_price_res.get("price").get("grandTotal")
      price_inr = f"₹{round(curr.convert(price, 'EUR', 'INR'),2)}"

      departure = ""
      arrival = ""

      for j in conf_price_res.get("itineraries")[0]["segments"]:
        departure += j["departure"]["iataCode"] + " " + \
            " ".join(j["departure"]["at"].split("T")) + "\n"
        arrival += j["arrival"]["iataCode"] + " " + \
            " ".join(j["arrival"]["at"].split("T")) + "\n"
      table.add_row([seats, duration, departure,arrival, price_inr, last_date])

      print(chalk.green.bold("General Information"))
      print(table.draw())

      print(chalk.green.bold("Flight Information"))
      table = Texttable()
      table.add_row([
        'Departure',
        'Arrival',
        'Aircraft Code',
        'Carrier Code',
        'Aircraft Number',
        'Number of Stops'
      ])

      for segment in conf_price_res.get("itineraries")[0]["segments"]:
        aircraft_code = segment["aircraft"]["code"]
        carrier_code =  segment["operating"]["carrierCode"]
        aircraft_number = segment["number"]
        stops = segment["numberOfStops"]
        dep = segment["departure"]["iataCode"] + " " + " ".join(segment["departure"]["at"].split("T"))
        arr = segment["arrival"]["iataCode"] + " " + " ".join(segment["arrival"]["at"].split("T"))
        table.add_row([dep,arr,aircraft_code,carrier_code,aircraft_number,stops])
        
      print(table.draw())

      print(chalk.green.bold("Pricing Information"))
      table = Texttable()
      base = round(curr.convert(conf_price_res.get("price")["base"], 'EUR', 'INR'),2)
      supplier = "₹"+str(round(curr.convert(conf_price_res.get("price")["fees"][0]["amount"], 'EUR', 'INR'),2))
      ticketing = "₹"+str(round(curr.convert(conf_price_res.get("price")["fees"][1]["amount"], 'EUR', 'INR'),2))
      grand_total = round(curr.convert(conf_price_res.get("price")["grandTotal"], 'EUR', 'INR'),2)
      refundable_taxes = "₹"+str(round(grand_total - base,2))
      base = "₹"+str(base)
      grand_total = "₹"+str(grand_total)
     
      table.add_row([
        'Base Price',
        'Supplier Fees',
        'Ticketing Fees',
        'Refundable Taxes',
        'Grand Total'
      ])

      table.add_row([base,supplier,ticketing,refundable_taxes,grand_total])
      
      print(table.draw())

    except ResponseError as error:  
      print(chalk.red.bold(f"Error in displaying confirmation price {error}"))
    except:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(chalk.red.bold(f"{exc_type}, {fname}, {exc_tb.tb_lineno},{exc_obj}"))

def confirm_price(flight_obj):
    try:
      return amadeus.shopping.flight_offers.pricing.post(flight_obj,include='credit-card-fees,other-services').data
    except ResponseError as error:
      print(chalk.red.bold(f"Error: {error}"))