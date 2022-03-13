from amadeus import Client, ResponseError
from dotenv import load_dotenv
from os import environ, sep

load_dotenv()

amadeus = Client(
    client_id=environ.get("API_KEY"),
    client_secret=environ.get("API_SECRET")
)

flight_info = {
      "type": "flight-offer",
      "id": "1",
      "source": "GDS",
      "instantTicketingRequired": False,
      "nonHomogeneous": False,
      "oneWay": False,
      "lastTicketingDate": "2022-03-21",
      "numberOfBookableSeats": 9,
      "itineraries": [
        {
          "duration": "PT1H30M",
          "segments": [
            {
              "departure": {
                "iataCode": "BLR",
                "at": "2022-03-21T19:00:00"
              },
              "arrival": {
                "iataCode": "GOI",
                "at": "2022-03-21T20:30:00"
              },
              "carrierCode": "AI",
              "number": "9547",
              "aircraft": {
                "code": "ATR"
              },
              "operating": {
                "carrierCode": "9I"
              },
              "duration": "PT1H30M",
              "id": "27",
              "numberOfStops": 0,
              "blacklistedInEU": False
            }
          ]
        }
      ],
      "price": {
        "currency": "EUR",
        "total": "29.55",
        "base": "20.00",
        "fees": [
          {
            "amount": "0.00",
            "type": "SUPPLIER"
          },
          {
            "amount": "0.00",
            "type": "TICKETING"
          }
        ],
        "grandTotal": "29.55"
      },
      "pricingOptions": {
        "fareType": [
          "PUBLISHED"
        ],
        "includedCheckedBagsOnly": True
      },
      "validatingAirlineCodes": [
        "AI"
      ],
      "travelerPricings": [
        {
          "travelerId": "1",
          "fareOption": "STANDARD",
          "travelerType": "ADULT",
          "price": {
            "currency": "EUR",
            "total": "29.55",
            "base": "20.00"
          },
          "fareDetailsBySegment": [
            {
              "segmentId": "27",
              "cabin": "ECONOMY",
              "fareBasis": "SIP9I",
              "class": "S",
              "includedCheckedBags": {
                "weight": 15,
                "weightUnit": "KG"
              }
            }
          ]
        }
      ]
    }

def display(res):
  print("ID\tAvailable_Seats\t\t\tDuration\tDeparture\tArrival")
  for i in res:
    id = i.get("id")
    seats = i.get("numberOfBookableSeats")
    duration = i.get("itineraries")[0]["duration"]
    print(f"{id}\t\t{seats}\t{duration}\t",end="")
    for j in i.get("itineraries")[0]["segments"]:
      print(j["departure"]["iataCode"],j["departure"]["at"],end="")
      print(j["arrival"]["iataCode"],j["arrival"]["at"])
      print()
  

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



    
