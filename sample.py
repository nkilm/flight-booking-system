from amadeus import Client, ResponseError
from dotenv import load_dotenv
from os import environ
from texttable import Texttable
from currency_converter import CurrencyConverter
from simple_chalk import chalk
import sys,os


inp = {
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

def display_confirmation_price(conf_price_res):
    try:
      table = Texttable(max_width=0)
      curr = CurrencyConverter()
      for i in conf_price_res.items():
        print(i)
      table.add_row([
        'Bookable Seats',
        'Duration',
        'Oneway',
        'Departure',
        'Arrival',
        'Price(inc. of Taxes)',
        'Last Ticketing Date'
      ])
      table.set_cols_align(["c", "c", "c", "c", "c","c","c"])
      last_date = conf_price_res.get("lastTicketingDate")
      seats = conf_price_res.get("numberOfBookableSeats")
      duration = conf_price_res.get("itineraries")[0]["duration"]
      price = conf_price_res.get("price").get("grandTotal")
      price_inr = f"₹{round(curr.convert(price, 'EUR', 'INR'),2)}"

      oneway = "No" if conf_price_res.get("oneWay") == 0 else "Yes"

      departure = ""
      arrival = ""

      for j in conf_price_res.get("itineraries")[0]["segments"]:
        departure += j["departure"]["iataCode"] + " " + \
            " ".join(j["departure"]["at"].split("T")) + "\n"
        arrival += j["arrival"]["iataCode"] + " " + \
            " ".join(j["arrival"]["at"].split("T")) + "\n"
      table.add_row([seats, duration, oneway, departure,arrival, price_inr, last_date])
      
      print(chalk.green.bold("General Information"))
      print(table.draw())

      print(chalk.green.bold("Flight Information"))
      table = Texttable()

      aircraft_code = conf_price_res.get("itineraries")[0]["segments"][0]["aircraft"]["code"]
      carrier_code =  conf_price_res.get("itineraries")[0]["segments"][0]["operating"]["carrierCode"]
      blacklisted_in_eu = conf_price_res.get("itineraries")[0]["segments"][0]["blacklistedInEU"]
      blacklisted_in_eu = "YES" if blacklisted_in_eu == 'False' else "NO"
      aircraft_number = conf_price_res.get("itineraries")[0]["segments"][0]["number"]
      stops = conf_price_res.get("itineraries")[0]["segments"][0]["numberOfStops"]
      
      table.add_row([
        'Aircraft Code',
        'Carrier Code',
        'Aircraft Number',
        'Blacklisted in EU(European Union)',
        'Number of Stops'
      ])

      table.add_row([aircraft_code,carrier_code,aircraft_number,blacklisted_in_eu,stops])
      print(table.draw())

      print(chalk.green.bold("Pricing Information"))
      table = Texttable()
      base = round(curr.convert(conf_price_res.get("price")["base"], 'EUR', 'INR'),2)
      supplier = "₹"+str(round(curr.convert(conf_price_res.get("price")["fees"][0]["amount"], 'EUR', 'INR'),2))
      ticketing = "₹"+str(round(curr.convert(conf_price_res.get("price")["fees"][1]["amount"], 'EUR', 'INR'),2))
      grand_total = round(curr.convert(conf_price_res.get("price")["grandTotal"], 'EUR', 'INR'),2)
      refundable_taxes = grand_total - base
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
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(chalk.red.bold(exc_type, fname, exc_tb.tb_lineno))


display_confirmation_price(inp)