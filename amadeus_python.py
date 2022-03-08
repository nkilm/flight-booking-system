from amadeus import Client, ResponseError
from dotenv import load_dotenv
from os import environ

load_dotenv()

amadeus = Client(
    client_id=environ.get("API_KEY"),
    client_secret=environ.get("API_SECRET")
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='BLR',
        destinationLocationCode='BOM',
        departureDate='2022-03-21',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)