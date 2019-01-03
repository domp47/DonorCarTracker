from datetime import date, timedelta
import StarkInventory
import ImpactInventory
import sqlite3

#Stark Information
# starkQuery = "https://starkautosales.com/inventory.php?startyear=2006&location=TORONTO&model=CORVETTE"
starkQuery = "https://starkautosales.com/inventory.php?startyear=2006&location=&model=4+SERIES"

#Impact Auto Information
postURL = "https://www.impactauto.ca/Search/GetSearchResult/"
model = "Corvette"
startYear = "2006"

#New Cars List
newStark  = []
newImpact = []

#Get List of cars from respective databases
starkCars  = StarkInventory.getStarkCars(starkQuery)
impactCars = ImpactInventory.getImpactCars(postURL, model, startYear)

#TODO change to config file
db = sqlite3.connect('./InvHistory.db')
connection = db.cursor()

today = date.today().strftime('%Y-%m-%d')

"""for car in starkCars:
    d = (car.stockNum, car.year, car.tranny, today)
    ins = 'INSERT INTO Stark (StockNumber, CarYear, Transmission, DateAccessed) VALUES (?,?,?,?)'

    connection.execute(ins, d)

for car in impactCars:
    d = (car.stockNum, car.auctionDate, car.year, car.tranny, car.model, today)
    ins = 'INSERT INTO Impact (StockNumber, AuctionDate, CarYear, Transmission, Model, DateAccessed) VALUES (?,?,?,?,?,?)'

    connection.execute(ins, d)

db.commit()"""

yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

for car in starkCars:
    d = (car.stockNum, yesterday)
    checkPrevDay = 'SELECT EXISTS(SELECT * FROM Stark WHERE StockNumber = ? AND DateAccessed = ? LIMIT 1)'

    connection.execute(checkPrevDay, d)
    
    if connection.fetchone()[0] == 0:
        newStark.append(car)

for car in impactCars:
    d = (car.stockNum, yesterday)
    checkPrevDay = 'SELECT EXISTS(SELECT * FROM Impact WHERE StockNumber = ? AND DateAccessed = ? LIMIT 1)'

    connection.execute(checkPrevDay, d)

    if connection.fetchone()[0] == 0:
        newImpact.append(car)   

#Delete all records older than one week
negWeek = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')

getOlderThanWeek = 'DELETE FROM Stark WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

getOlderThanWeek = 'DELETE FROM Impact WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

db.commit()
db.close()

if len(newStark) > 0 or len(newImpact) > 0:
    sendEmail = 1