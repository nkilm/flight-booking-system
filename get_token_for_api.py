from requests import post
from dotenv import load_dotenv
from os import environ

URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

load_dotenv()

header = {}

header['content-type'] = "application/x-www-form-urlencoded"

r = post(URL,
  headers=header,
  auth=(environ.get("API_KEY"),environ.get("API_SECRET")),
  json={
    "grant_type": "client_credentials"
  }
)

response = r.json()

print(response)