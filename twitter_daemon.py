#!/usr/bin/env python

import twitter
import simplejson
import time
import requests

from bitcoinaverage.twitter_config import api

# requires  http://code.google.com/p/python-twitter/
# https://github.com/bear/python-twitter.git

URL = "https://api.bitcoinaverage.com/ticker/global/USD"

change = 0
oldprice = 0
perc = 0
direction = ""

while True:
    try:
        r = requests.get(URL).json()
    except(simplejson.decoder.JSONDecodeError, requests.exceptions.ConnectionErro):
        time.sleep(2)
        continue

    newprice = r['last']
    
    if oldprice > newprice:
        b = oldprice - newprice
        change = round(b, 2)
        direction = "down"
        if oldprice != 0:
            a = (change / oldprice)*100
            perc = round(a, 2)
    elif oldprice < newprice:
        b = newprice - oldprice
        change = round(b, 2)
        direction = "up"
        if oldprice != 0:
            a = (change / oldprice)*100
            perc = round(a, 2)
            
    if perc != 0 and change != 0 and direction != "":
        status = "Bitcoin Average Global Rate: ${0} ({1} ${2}) - https://BitcoinAverage.com".format(newprice,direction,change)
        status = api.PostUpdate(status)
    else:
        status = "Bitcoin Average Global Rate: ${0} - https://BitcoinAverage.com".format(newprice)
        status = api.PostUpdate(status)
        
    oldprice = newprice

    time.sleep(60*60*1)