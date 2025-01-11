#!/usr/bin/env python3

# nessessary modules for the prodram to work  
import urllib.request # Sends HTTP requests
import time # Time functionallity for time related tasks
import threading # Allows different functions to run at the same time
from seeed_dht import DHT  # seed_dht has to be installed on your system.
from grove.display.jhd1802 import JHD1802 # Library for grove LCD display

# Turns on the temperature and humidity sensor 
sensor = DHT("11", 5)

# Here's the URL that I want to sent the data to 
URL = 'https://api.thingspeak.com/update?api_key=7SZT6JKQOC30UI2Q'

# Used to help with synchronisation of both functions 
lock = threading.Lock()

def main():
    # Grove - 16x2 LCD(White on Blue) connected to I2C port
    lcd = JHD1802()

    # Grove - Temperature&Humidity Sensor connected to port D5
    sensor = DHT('11', 5)

    while True:
        with lock:
            humi, temp = sensor.read()

        # Temperature and humidity readings on console
        print('temperature {}C, humidity {}%'.format(temp, humi))

        # Prints temperature reading on the LCD display
        lcd.setCursor(0, 0)
        lcd.write('temperature: {0:2}C'.format(temp))


        # Prints humitity reading on the LCD display
        lcd.setCursor(1, 0)
        lcd.write('humidity: {0:5}%'.format(humi))

        # Updates display every one second 
        time.sleep(1)


def thingspeak():
    threading.Timer(10, thingspeak).start()
    try:
        with lock:
            temp, humidity = sensor.read()


         # CHecks the sensor readings 
        if temp is None or humidity is None:
            print('Failed. Please wait while it\'s retrying...')
            return

        # Makes a HTTP request with sensor data
        HEADER = f'&field1={temp}&field2={humidity}'
        new_URL=URL+HEADER

        # Sends the HTTP to ThingSpeak along with the sensor data
        data=urllib.request.urlopen(new_URL)

        # Displays the data being sent to the console
        print(f'Sending data: Temperature = {temp}C, Humidity = {humidity}%')
        print(data.read())
    except Exception as e:
        # Prints an error message In case of failure.
        print(f'error: {e}')

if __name__ == '__main__':

    # Starts the send dara to thinkspeak function 
    thingspeak()

    # Starts the function to display data to LCD display
    main()