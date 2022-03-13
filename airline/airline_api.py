"""
Checkout Airport Codes at
https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm

NOTE: 
GET NEW ACCESS TOKEN IF EXPIRED

"""
from requests import get
from dotenv import load_dotenv
from os import environ

load_dotenv()

src = input("Enter source:").replace(" ","").upper()
dest = input("Enter destination:").replace(" ","").upper()

URL = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={src}&destinationLocationCode={dest}&departureDate=2022-03-21&adults=1&max=2"

headers = {}
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer " + environ.get("AUTH")

response = get(URL,headers = headers)

results= response.json()

for item in results.items():
    print(item)
