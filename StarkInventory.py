import requests
from bs4 import BeautifulSoup as BS
from StarkData import Stark

# query = "https://starkautosales.com/inventory.php?startyear=2006&location=TORONTO&model=CORVETTE"
query = "https://starkautosales.com/inventory.php?startyear=2006&location=&model=4+SERIES"

def getStarkCars(query):

    r = requests.get(query)
    soup = BS(r.text, "html.parser")

    inventoryTable = soup.find("ul", {"id":"inventory-list"})

    inventoryList = inventoryTable.findAll("li", {"class":"table"})

    inventory = []

    for item in inventoryList:
        attributes = item.findAll("div")

        car = Stark(attributes[1].string, attributes[2].string, attributes[8].string)

        inventory.append(car)

    return inventory

print(getStarkCars(query))