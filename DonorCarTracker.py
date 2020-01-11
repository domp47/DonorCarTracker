from datetime import date, timedelta
import SendNotification
import ast
import Stark
import Parts4Less
import sqlite3
import configparser
import os

def findNew(connection, tableName, currentCars):
    newCars = []

    #Check if there's any cars today that weren't there yesterday
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    for car in currentCars:
        d = (car.stockNum, yesterday)
        checkPrevDay = f'SELECT EXISTS(SELECT * FROM {tableName} WHERE StockNumber = ? AND DateAccessed = ? LIMIT 1)'

        connection.execute(checkPrevDay, d)
        
        if connection.fetchone()[0] == 0:
            newCars.append(car)

    return newCars

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = dir_path + "/config.ini"

if not os.path.isfile(configFilename):
    print("No configuration file found. Please run Setup before running this.")
    exit(0)

config = configparser.RawConfigParser()
config.read(configFilename)

#New Cars List
newStark      = []
newParts4Less = []
newImpact     = []
newCopart     = []

#Get List of cars from respective databases
starkCars = []
for url in ast.literal_eval(config["STARK"]["URLS"]):
    res = Stark.getStarkCars(url, config['VIN_DIGIT']['ENGINE_CODE'])
    if res is not None:
        starkCars += res

parts4LessCars = []
for url in ast.literal_eval(config["PARTS_4_LESS"]["URLS"]):
    res = Parts4Less.getParts4LessCars(url)
    if res is not None:
        parts4LessCars += res

# impactCars = ImpactInventory.getImpactCars(config["IMPACT"]["URL"], config["IMPACT"]["Model"], config["IMPACT"]["Year"])
# copartCars = CopartInventory.getCopartCars(config["COPART"]["URL"], config["COPART"]["DATA"], config["COPART"]["COOKIE"])

db = sqlite3.connect(config["DATABASE"]["Path"])
connection = db.cursor()

today = date.today().strftime('%Y-%m-%d')

for car in starkCars:
    d = (car.stockNum, car.year, car.tranny, today)
    ins = 'INSERT INTO Stark (StockNumber, CarYear, MakeModel, Engine, DateAccessed) VALUES (?,?,?,?,?)'

    connection.execute(ins, d)

for car in parts4LessCars:
    d = (car.stockNum, car.year, car.makeAndModel, car.engine, today)
    ins = 'INSERT INTO Parts4Less (StockNumber, CarYear, MakeModel, Engine, DateAccessed) VALUES (?,?,?,?,?)'

    connection.execute(ins, d)

# for car in impactCars:
#     d = (car.stockNum, car.auctionDate, car.year, car.tranny, car.model, today)
#     ins = 'INSERT INTO Impact (StockNumber, AuctionDate, CarYear, Transmission, Model, DateAccessed) VALUES (?,?,?,?,?,?)'

#     connection.execute(ins, d)

# for car in copartCars:
#     d = (car.stockNum, car.auctionDate, car.year, car.tranny, car.model, car.loc, today)
#     ins = 'INSERT INTO Copart (StockNumber, AuctionDate, CarYear, Transmission, Model, Location, DateAccessed) VALUES (?,?,?,?,?,?,?)'

#     connection.execute(ins, d)

db.commit()

#Check if there's any cars today that weren't there yesterday
yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
for car in starkCars:
    d = (car.stockNum, yesterday)
    checkPrevDay = 'SELECT EXISTS(SELECT * FROM Stark WHERE StockNumber = ? AND DateAccessed = ? LIMIT 1)'

    connection.execute(checkPrevDay, d)
    
    if connection.fetchone()[0] == 0:
        newStark.append(car)

newStark = findNew(connection, 'Stark', starkCars)
newParts4Less = findNew(connection, 'Parts4Less', parts4LessCars)
# newImpact = findNew(connection, 'Impact', impactCars)
# newCopart = findNew(connection, 'Copart', copartsCars)

#Delete all records older than one week
negWeek = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')

getOlderThanWeek = 'DELETE FROM Stark WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

getOlderThanWeek = 'DELETE FROM Parts4Less WHERE DateAccessed <= ?'
connection.execute(getOlderThanWeek, (negWeek,))

# getOlderThanWeek = 'DELETE FROM Impact WHERE DateAccessed <= ?'
# connection.execute(getOlderThanWeek, (negWeek,))

# getOlderThanWeek = 'DELETE FROM Copart WHERE DateAccessed <= ?'
# connection.execute(getOlderThanWeek, (negWeek,))

db.commit()
db.close()

# if len(newStark) > 0 or len(newImpact) > 0 or len(newCopart) > 0:
#     SendNotification.sendNotification(newStark, newImpact, newCopart, config)