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
from hcsr04 import HCSR04
from time import sleep

ssid = 'INFINITUM2A5B_2.4'
password = 'FMxMFmE237'
mqtt_server = '192.168.1.192'
# ssid = 'IZZI-6D04'
# password = 'F0AF85386D04'
# mqtt_server = 'broker.hivemq.com'
# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'machine_status/laser_doors'
topic_pub = b'machine_status/laser_doors'

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
