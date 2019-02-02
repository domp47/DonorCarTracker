import requests
import json
from CopartData import Copart
from datetime import datetime
from dateutil import tz

def getCopartCars(url, data, cookie):

    header = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    header["accept"] = "application/json"
    header["cookie"] = cookie

    r = requests.post(url, headers=header, data=data)

    runList = json.loads(r.text)["data"]["results"]["content"]
    inventory = []

    for item in runList:
        if item["bf"]:
        
            ts = int(item["ad"])/1000
            auctDate = datetime.utcfromtimestamp(ts)
            auctDate = auctDate.replace(tzinfo=tz.tzutc())
            auctDate = auctDate.astimezone(tz.tzlocal()).strftime("%Y-%m-%d")

            car = Copart(item["lotNumberStr"], auctDate, item["lcy"], item["tmtp"], item["lm"], item["yn"])
            inventory.append(car)

    return inventory