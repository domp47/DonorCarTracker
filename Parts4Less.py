import requests
from bs4 import BeautifulSoup as BS

class P4L:
    def __init__(self, stockNum, year, makeAndModel, engine):
        self.stockNum = stockNum
        self.year = year
        self.makeAndModel = makeAndModel
        self.engine = engine

    def toString(self):
        return f"Stock #: {self.stockNum}, Year: {self.year}, Engine: {self.engine}"

def getParts4LessCars(query):
    r = requests.get(query)
    soup = BS(r.text, "html.parser")

    allCars = soup.find_all("div", class_="itemList_absolute_outer_container")

    if allCars == None:
        return []

    inventory = []

    for car in allCars:
        ymm = car.find("div", {"class":"itemList_YearMakeModelName"}).string
        stockNum = car.find("div", {"class":"itemList_ItemStocknumber"}).contents[1].strip()
        engine = car.find("div", {"class":"itemList_strItemBasicFeatures"}).contents[0].split('|')[-1].strip()

        inventory.append(P4L(stockNum, int(ymm[:4].strip()), ymm[4:].strip(), engine))

    return inventory