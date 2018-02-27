# -*- coding: utf-8 -*-
"""
        BotCoin MAIN
        Created by:     GNM
"""

import urllib
import requests
import json
import os
import Common as cmn

# Pruebas sobre las opciones que nos permite el bot
initialResponse = requests.get(cmn.url + 'getme')

updateResponse = requests.get(cmn.url + 'getUpdates')

# For sending messages to an specific chat
def sendMsg(msg, chat):
    
    sendMsg = '{}sendMessage?chat_id={}&text={}'.format(cmn.url, str(chat), msg)
    
    print(sendMsg)
    content = requests.post(sendMsg)
    
    if content.status_code != 200:
        print('Something went wrong!')
    else:
        print('Message sent')

def jsonToDict(response):
    
    parsed = json.loads(response.content)
    
    return parsed

def getLastUpdate(offset = None):
    
    request = cmn.url + 'getUpdates'
    
    if offset:
        request = request + '?offset={}'.format(offset)
        
    update = requests.get(request)
    update = jsonToDict(update)
    lastUpdate = update['result'][0]['update_id']
    
    return lastUpdate

def getLastCryptoPrice(crypto, fxCurrencies = cmn.mainCurrencies):
    
    s = ','
    currencies = s.join(fxCurrencies)
    lastPrice = requests.get(cmn.crypto_url + 'price?fsym={}&tsyms={}'.format(crypto, currencies))
    lastPrice = jsonToDict(lastPrice)
    
    for key, value in lastPrice.items():
            
        print(crypto + '/' + key + ' = ' + str(value))
    
    return lastPrice

def getUpdateNumber():
    
    
    if os.path.exists('C:/Py_projects/files/updateNumber.txt') == False:
        
        updateFile = open('C:/Py_projects/files/updateNumber.txt', 'w')
        updateFile.write('0')
        updateNumber = 0
        updateFile.close()
        
    else:
        
        updateFile = open('C:/Py_projects/files/updateNumber.txt', 'r')
        updateNumber = int(updateFile.readline())
        updateFile.close()
        
    return updateNumber

def setUpdateNumber(number):
    
    updateFile = open('C:/Py_projects/files/updateNumber.txt', 'w')
    updateFile.flush()
    number = str(number)
    updateFile.write(number)
    updateFile.close()

def sendCryptoKeyboard(chat, keyboard):
    
    
    sendMsg = '{}sendMessage?chat_id={}&reply_markup={}'.format(cmn.url, str(chat), keyboard)
    print(sendMsg)
    requests.post(sendMsg)