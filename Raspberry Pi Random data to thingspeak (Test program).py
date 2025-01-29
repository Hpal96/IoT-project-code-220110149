#!/usr/bin/env python3

# This is a test file I used to check if my divice could communicated and send data to thingspeak 

import random # Generate random values 
import urllib.request # Send URL requests 
import threading # Timed function execution  

def thingspeak():
    threading.Timer(15, thingspeak).start()
    # sends random numbers from one to thirty 
    val = random.randint(1, 30)
    #Sends the data to the this URL
    URL = 'https://api.thingspeak.com/update?api_key='
    # My write API key
    KEY = ''
    # My two fields on my channel to display the random values 
    HEADER = '&field1={}&field2={}'.format(val, val)
    new_URL = URL + KEY + HEADER # https://api.thingspeak.com/update?api_key=7SZT6JKQ0C30UI2Q&field1={}&field2={}
    try:
        data = urllib.request.urlopen(new_URL)
        print(data.read())
    except Exception as e:
        #Prints error message 
        print(f"Error: {e}")

if __name__ == '__main__':
    #Funs the thingspeak function 
    thingspeak()
