# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
# Complete project details at https://RandomNerdTutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/
from time import sleep

ssid = 'Totalplay-2.4G-fee0'
password = 'UUuQkjdK56LGPyjX'
mqtt_server = '192.168.100.192'
# ssid = 'IZZI-6D04'
# password = 'F0AF85386D04'
# mqtt_server = 'broker.hivemq.com'
# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())

last_message = 0
message_interval = 10
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())
