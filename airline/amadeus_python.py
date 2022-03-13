from amadeus import Client, ResponseError
from dotenv import load_dotenv
from os import environ
from texttable import Texttable
from currency_converter import CurrencyConverter
from simple_chalk import chalk

load_dotenv()

amadeus = Client(
    client_id=environ.get("API_KEY"),
    client_secret=environ.get("API_SECRET")
)

def display(res):
  # if(len(res)==0):
  #   print(chalk.bold.red("No Flights Available"))
  #   return
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
  # table.set_cols_align(["c", "c", "c", "c", "c","c","c"])
  curr = CurrencyConverter()
  
  for i in res: 
    id = i.get("id")
    seats = i.get("numberOfBookableSeats")
    duration = i.get("itineraries")[0]["duration"]

    price = i.get("price").get("grandTotal")
    price_inr = chalk.green(f"₹{round(curr.convert(price, 'EUR', 'INR'),2)}")

    oneway = "No" if i.get("oneWay")==0 else "Yes"

    departure = ""
    arrival = ""
    
    for j in i.get("itineraries")[0]["segments"]:
      departure += j["departure"]["iataCode"] + " " + " ".join(j["departure"]["at"].split("T")) + "\n"
      arrival += j["arrival"]["iataCode"] + " " + " ".join(j["arrival"]["at"].split("T")) + "\n"
    table.add_row([id,seats,duration,oneway,departure,arrival,price_inr])

  print(table.draw())

def check_flights(src,dest,date,adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
        originLocationCode=src.upper(),
        destinationLocationCode=dest.upper(),
        departureDate=date,
        adults=adults).data
        return response
        
    except ResponseError as error:
        return error

def confirm_price(flight_obj):
    return amadeus.shopping.flight_offers.pricing.post(flight_obj,include='credit-card-fees,other-services').data

def book_flight(flight_obj):
    # The flight ID comes from the Flight Create Orders (in test environment it's temporary)
    # Retrieve the order based on it's ID
    flight_booking = amadeus.booking.flight_orders.post(flight_obj).data
    amadeus.booking.flight_order(flight_booking['id']).get()

    # Delete the order based on it's ID
    amadeus.booking.flight_order(flight_booking['id']).delete()