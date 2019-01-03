import requests
from ImpactRequest import ImpactSearch
from ImpactData import Impact
import json

postURL = "https://www.impactauto.ca/Search/GetSearchResult/"
model = "Corvette"

def getImpactCars(URL, model, fromYear=None):

    payload = json.dumps(ImpactSearch(model, fromYear).__dict__)

    header = {'Content-Type':'application/json'}
    r = requests.post(postURL, headers=header, data=payload)

    response = json.loads(r.text)

    runList = response["RunList"]

    inventory = []

    for item in runList:
        car = Impact(item["StockNum"],item["AuctionDate"],item["Year"],item["Transmission"],item["Model"])
        inventory.append(car)

    return inventory