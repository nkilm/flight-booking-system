from amadeus import Client, ResponseError
from dotenv import load_dotenv
from os import environ
from prettytable import PrettyTable

load_dotenv()

amadeus = Client(
    client_id=environ.get("API_KEY"),
    client_secret=environ.get("API_SECRET")
)

def display(res):
  t = PrettyTable(['ID', 'Seats','Duration'])

  for i in res: 
    id = i.get("id")
    seats = i.get("numberOfBookableSeats")
    duration = i.get("itineraries")[0]["duration"]
    t.add_row([id,seats,duration])
    # for j in i.get("itineraries")[0]["segments"]:
      # print(j["departure"]["iataCode"],j["departure"]["at"],end="")
      # print(j["arrival"]["iataCode"],j["arrival"]["at"])
      # print()
  print(t)
  

def check_flights(src,dest,date,adults):
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

def flight_booking(flight_obj):
    return amadeus.booking.flight_orders.post(flight_obj).data


def book_flight(flight_obj):
    # The flight ID comes from the Flight Create Orders (in test environment it's temporary)
    # Retrieve the order based on it's ID
    flight_booking = amadeus.booking.flight_orders.post(flight_obj).data
    amadeus.booking.flight_order(flight_booking['id']).get()

    # Delete the order based on it's ID
    amadeus.booking.flight_order(flight_booking['id']).delete()

if __name__=="__main__":
    # print(check_flights("blr","goi","2022-03-21",1))
    results = check_flights("blr","goi","2022-03-21",1)
    display(results)
    # print(confirm_price(flight_info))



    
