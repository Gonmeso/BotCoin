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
import time

# Pruebas sobre las opciones que nos permite el bot
initialResponse = requests.get(cmn.url + 'getme')

updateResponse = requests.get(cmn.url + 'getUpdates')

# For sending messages to an specific chat
def sendMsg(msg, chat):
    
    # Parse to http
    msg = urllib.parse.quote_plus(msg)
    sendMsg = '{}sendMessage?chat_id={}&text={}'.format(cmn.url, str(chat), msg)
    
#    print(sendMsg)
    content = requests.post(sendMsg)
    
    if content.status_code != 200:
        print('Something went wrong!')
    else:
        print('Message sent')

# Easy function to transform json to python readable dictionaries
def jsonToDict(response):
    
    parsed = json.loads(response.content)
    
    return parsed

# Get the last update starting at the offset
def getLastUpdate(offset = None):
        
    request = cmn.url + 'getUpdates'
    
    if offset:
        request = request + '?offset={}'.format(offset)
        
    update = requests.get(request)
    update = jsonToDict(update)
    
    if  update['result']:
        
        lastUpdate = update['result']
    else:
        lastUpdate = False
        return lastUpdate 

    return lastUpdate

# Fast API request to get crypto prices and FX
def getLastCryptoPrice(crypto, fxCurrencies = cmn.mainCurrencies):
    
    s = ','
    currencies = s.join(fxCurrencies)
    lastPrice = requests.get(cmn.crypto_url + 'price?fsym={}&tsyms={}'.format(crypto, currencies))
    lastPrice = jsonToDict(lastPrice)
    
    #For readable information when executing it
    priceString = ''
    for key, value in lastPrice.items():
            
        priceString = (priceString + crypto + '/' + key + ' = ' + str(value) + '\n')
    
    return priceString

# Get the last handled update, useful when bot has been down
def getUpdateNumber():
    
    if os.path.exists(cmn.filePath + 'updateNumber.txt') == False:
        
        updateFile = open(cmn.filePath + 'updateNumber.txt', 'w')
        updateFile.write('0')
        updateNumber = 0
        updateFile.close()
        
    else:
        
        updateFile = open(cmn.filePath + 'updateNumber.txt', 'r')
        updateNumber = int(updateFile.readline())
        updateFile.close()
        
    return updateNumber

# Set last handled update
def setUpdateNumber(number):
    
    updateFile = open(cmn.filePath + 'updateNumber.txt', 'w')
    updateFile.flush()
    number = str(number)
    updateFile.write(number)
    updateFile.close()

# WIP function, to send keyboard with cryptocurrencies list
def sendCryptoKeyboard(chat, keyboard):
    
    sendMsg = '{}sendMessage?chat_id={}&reply_markup={}'.format(cmn.url, str(chat), json.dumps(keyboard))
    print(sendMsg)
    requests.post(sendMsg)

# Get all cryptocurrencies available at CryptoCompare
def getCryptoList():
    
    response = requests.get('https://www.cryptocompare.com/api/data/coinlist/')
    response = jsonToDict(response)
    
    cryptoKeys = response['Data'].keys()
    
    cryptoList = open(cmn.filePath + 'cryptoList.txt', 'w+')
    
    for key in cryptoKeys:
        try:
            info = str(key)
            info = info + ' ' + str(response['Data'][key]['CoinName'] + '\n')  
            cryptoList.write(info)
        except:
            print('Encoding error at {}'.format(key))
    
    cryptoList.close()
    
# Check if the ccy is available now    
def isCryptoAvailable(crypto):
    
    cryptoList = open(cmn.filePath + 'cryptoList.txt')
    
    for line in cryptoList:
        
        data = line.strip().split()
        
        if data[0] == crypto:
            return True
    
    return False

# Handle updates to retrieve cryptoccy prices
def handleUpdate(update):
    
    chat = update['from']['id']
    
    if 'text' in update:
        
        text = update['text']
        isCrypto = isCryptoAvailable(text)
        
        if isCrypto:
            
            prices = getLastCryptoPrice(text)
            sendMsg(prices, chat)
            
        elif text == 'ChapaGarito':
            cmn.keepExecution = False 
            
        
    return cmn.keepExecution
        
    

def main():
    
    offset = getUpdateNumber()
    updates = getLastUpdate(offset = offset)
    
    while cmn.keepExecution:
        
        offset = getUpdateNumber()
        updates = getLastUpdate(offset = offset)
        
        if updates and len(updates) > 0:
            
            lastUpdate = len(updates) - 1
            lastUnattended = updates[lastUpdate]['update_id']
            
            for update in updates:
                
                cmn.keepExecution = handleUpdate(update['message'])
                print('INFO: Update {} handled successfully'.format(update['update_id']))
                
                if not cmn.keepExecution:
                    print('WARN: the bot has been stopped')
                    break
                
            setUpdateNumber(int(lastUnattended) + 1 )
            
        else:
            print('No updates')
        
        time.sleep(5)
        

if __name__ == "__main__":
    
    main()

            
        