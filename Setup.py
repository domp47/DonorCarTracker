import configparser
import os.path, os
import errno
import sqlite3

configFilename = "/config.ini"
defaultDatabase = "/InvHistory.db"
dir_path = os.path.dirname(os.path.realpath(__file__))

fullConfig = dir_path + configFilename 
fullDatabase = dir_path + defaultDatabase

def createConfig():
    dbPath = input("Enter Database Path or leave it blank to set up database for first time: ")

    if dbPath == "":
        createDB()
        dbPath = fullDatabase

    #Stark Auto info
    starkQuery = input("Enter the URL to search Stark for automobiles: ")

    #Impact Auto info
    impactURL = input("Enter the URL for Impact Auto's search query: ")
    impactModel = input("Enter the car model searching for: ")
    impactYear = input("Enter the older possible year for the car or leave blank for no limit: ")
    impactYear = None if impactYear is "" else impactYear

    #Copart info
    print("To get the data string and cookie use a web browser network tool to get them from the search request. Cookie from \"Request Headers\" and data string from the source of \"Form Data\".")
    copartURL = input("Enter coparts search URL: ")
    copartData = input("Enter Copart's data string: ")
    copartCookie = input("Enter your Copart Cookie: ")

    #Email info
    fromEmail = input("Enter address of Email to send from: ")
    fromPass  = input("Enter password for Email: ")
    smtpServer= input("Enter SMTP server for Email: ")
    smtpPort  = input("Enter SMTP port for Email: ")
    toEmail = []

    print("Enter up to 10 email recipients, enter a blank email to stop before 10")

    for i in range(1,11):
        userIn = input(str(i)+": ")

        if userIn == "":
            break

        toEmail.append(userIn)

    config = configparser.ConfigParser()

    config["DATABASE"] = {'Path': dbPath}
    config["STARK"]    = {'URL': starkQuery}
    config["IMPACT"]   = {'URL': impactURL, 'Model': impactModel, 'Year':impactYear}
    config["COPART"]    = {'URL': copartURL, 'Data': copartData, 'Cookie':copartCookie}
    config["EMAIL"]    = {'FromAddr': fromEmail, 'FromPassword': fromPass, 'SMTP_Server':smtpServer, 'SMTP_Port': smtpPort, 'ToAddr': toEmail}

    with open(fullConfig, 'w') as f:
        config.write(f)

    print("Setup Complete!")


def createDB():
    print("Continuing will completely overwrite any existing database with the default name.")

    userInput = input("Enter [Y] to continue, Enter [q] or just close the program to cancel: ")
    
    if userInput.lower() == 'q':
        print("Cancelling Now, no changes were made to your database.")
        exit(0)
    elif userInput.upper() != 'Y':
        print("Abort.")
        exit(0)
    else:

        removeIfExists(fullDatabase)
        db = sqlite3.connect(fullDatabase)
        connection = db.cursor()

        connection.execute('CREATE TABLE "Impact" ( `Id` INTEGER PRIMARY KEY AUTOINCREMENT, `StockNumber` TEXT NOT NULL, `AuctionDate` TEXT NOT NULL, `CarYear` TEXT NOT NULL, `Transmission` TEXT, `Model` TEXT NOT NULL, `DateAccessed` TEXT NOT NULL )')
        connection.execute('CREATE TABLE "Stark" ( `Id` INTEGER PRIMARY KEY AUTOINCREMENT, `StockNumber` TEXT NOT NULL, `CarYear` TEXT NOT NULL, `Transmission` TEXT, `DateAccessed` TEXT NOT NULL )')
        connection.execute('CREATE TABLE "Copart" ( `Id` INTEGER PRIMARY KEY AUTOINCREMENT, `StockNumber`	TEXT NOT NULL, `AuctionDate`	TEXT NOT NULL, `CarYear`	TEXT NOT NULL, `Transmission`	TEXT NOT NULL, `Model`	TEXT NOT NULL, `Location`	TEXT NOT NULL, `DateAccessed`	TEXT NOT NULL);')

        db.commit()
        db.close()

def removeIfExists(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

if os.path.isfile(fullConfig):
    print("Configuration file already present. You can edit with a text editor if you wish to make individual changes.")
    print("Continuing will completely overwrite previous configurations.")

    userInput = input("Enter [Y] to continue, Enter [q] or just close the program to cancel:")

    if userInput.lower() == 'q':
        print("Cancelling Now, no changes were made to your configurations.")
        exit(0)
    elif userInput.upper() == 'Y':
        createConfig()
    else:
        print("Abort.")
        exit(0)
else:
    createConfig()