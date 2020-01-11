import requests
from bs4 import BeautifulSoup as BS

class Stark:
    
    def __init__(self, stockNum, year, makeModel, engine):
        self.stockNum = stockNum
        self.year = year
        self.makeModel = makeModel
        self.engine = engine

    def toString(self):
        return f"Stock #: {self.stockNum}, Year: {self.year}, MakeModel: {self.makeModel}, Engine: {self.engine}"

    def __str__(self):
        return self.toString()
    
    def __repr__(self):
        return self.toString()

def getStarkCars(query, engineCode = None):

    r = requests.get(query)
    soup = BS(r.text, "html.parser")

    inventoryTable = soup.find("ul", {"id":"inventory-list"})

    if inventoryTable == None:
        return []

    inventoryList = inventoryTable.findAll("li", {"class":"table"})

    inventory = []

    for item in inventoryList:
        itemUrl = f"https://starkautosales.com/{item.find('a')['href']}"
        r = requests.get(itemUrl)

        soup = BS(r.text, "html.parser")

        attributeTable = soup.find("div", {"class":"sidebar-item-details"}).find_all("div")

        stockNum = None
        year = None
        make = None
        model = None
        engine = None
        vin = None

        for i in range(0, len(attributeTable), 3):
            attr = attributeTable[i].find_all("div")

            key = attr[0].string
            value = attr[1].string

            if key == "Stock #:":
                stockNum = value
            elif key == "Year:":
                year = value
            elif key == "Make:":
                make = value
            elif key == "Model:":
                model = value
            elif key == "Engine Size:":
                engine = value
            elif key == "VIN:":
                vin = value

        if engineCode is not None and not vin[7] == engineCode:
            continue

        inventory.append(Stark(stockNum, year, f"{make} {model}", engine))

    return inventory