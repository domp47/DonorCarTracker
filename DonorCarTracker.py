from datetime import date, timedelta
import SendNotification
import StarkInventory
import ImpactInventory
import CopartInventory
import sqlite3
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = dir_path + "/config.ini"

if not os.path.isfile(configFilename):
    print("No configuration file found. Please run Setup before running this.")
    exit(0)

config = configparser.RawConfigParser()
config.read(configFilename)

#New Cars List
newStark  = []
newImpact = []
newCopart = []

#Get List of cars from respective databases
starkCars  = StarkInventory.getStarkCars(config["STARK"]["URL"])
impactCars = ImpactInventory.getImpactCars(config["IMPACT"]["URL"], config["IMPACT"]["Model"], config["IMPACT"]["Year"])
copartCars = CopartInventory.getCopartCars(config["COPART"]["URL"], config["COPART"]["DATA"], config["COPART"]["COOKIE"])

db = sqlite3.connect(config["DATABASE"]["Path"])
connection = db.cursor()

today = date.today().strftime('%Y-%m-%d')

for car in starkCars:
    d = (car.stockNum, car.year, car.tranny, today)
    ins = 'INSERT INTO Stark (StockNumber, CarYear, Transmission, DateAccessed) VALUES (?,?,?,?)'

    connection.execute(ins, d)

for car in impactCars:
    d = (car.stockNum, car.auctionDate, car.year, car.tranny, car.model, today)
    ins = 'INSERT INTO Impact (StockNumber, AuctionDate, CarYear, Transmission, Model, DateAccessed) VALUES (?,?,?,?,?,?)'

    connection.execute(ins, d)

for car in copartCars:
    d = (car.stockNum, car.auctionDate, car.year, car.tranny, car.model, car.loc, today)
    ins = 'INSERT INTO Copart (StockNumber, AuctionDate, CarYear, Transmission, Model, Location, DateAccessed) VALUES (?,?,?,?,?,?,?)'

    connection.execute(ins, d)

db.commit()

#Check if there's any cars today that weren't there yesterday
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

for car in copartCars:
    d = (car.stockNum, yesterday)
    checkPrevDay = 'SELECT EXISTS(SELECT * FROM Impact WHERE StockNumber = ? AND DateAccessed = ? LIMIT 1)'

    connection.execute(checkPrevDay, d)

    if connection.fetchone()[0] == 0:
        newCopart.append(car)

#Delete all records older than one week
negWeek = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')

getOlderThanWeek = 'DELETE FROM Stark WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

getOlderThanWeek = 'DELETE FROM Impact WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

getOlderThanWeek = 'DELETE FROM Copart WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

db.commit()
db.close()

if len(newStark) > 0 or len(newImpact) > 0 or len(newCopart) > 0:
    SendNotification.sendNotification(newStark, newImpact, newCopart, config)