# Complete project details at https://RandomNerdTutorials.com
import json
import time

global checking_laser_doors, checking_smoke_extractor, material_workspace, available_space, leds_strip, laser_camera
from machine import Pin, ADC


def sub_cb(topic, msg):
    global checking_laser_doors, checking_smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

    payload_message = json.loads(msg.decode('utf-8'))

    if 'laser_doors' in payload_message:
        laser_doors_source = payload_message['laser_doors']['source']
        laser_doors_status = payload_message['laser_doors']['status']

        if laser_doors_source == 'raspberry' and not laser_doors_status and topic == b'machine_status/laser_doors':
            checking_laser_doors = True
            print(f'ESP received: {msg} ')

    if 'smoke_extractor' in payload_message:
        smoke_extractor_source = payload_message['smoke_extractor']['source']
        smoke_extractor_status = payload_message['smoke_extractor']['status']

        if smoke_extractor_source == 'raspberry' \
                and not smoke_extractor_status and topic == b'machine_status/smoke_extractor':
            checking_smoke_extractor = True
            print(f'ESP received: {msg} ')

    if 'material_workspace' in payload_message:
        material_workspace_source = payload_message['material_workspace']['source']
        material_workspace_status = payload_message['material_workspace']['status']

        if material_workspace_source == 'raspberry' \
                and not material_workspace_status and topic == b'machine_status/material_workspace':
            material_workspace = True
            print(f'ESP received: {msg} ')

    if 'available_space' in payload_message:
        available_space_source = payload_message['available_space']['source']
        available_space_status = payload_message['available_space']['status']

        if available_space_source == 'raspberry' \
                and not available_space_status and topic == b'machine_status/available_space':
            available_space = True
            print(f'ESP received: {msg} ')

    if 'leds_strip' in payload_message:
        leds_strip_source = payload_message['leds_strip']['source']
        leds_strip_status = payload_message['leds_strip']['status']

        if leds_strip_source == 'raspberry' \
                and not leds_strip_status and topic == b'machine_status/leds_strip':
            leds_strip = True
            print(f'ESP received: {msg} ')

    if 'laser_camera' in payload_message:
        laser_camera_source = payload_message['laser_camera']['source']
        laser_camera_status = payload_message['laser_camera']['status']

        if laser_camera_source == 'raspberry' \
                and not laser_camera_status and topic == b'machine_status/laser_camera':
            laser_camera = True
            print(f'ESP received: {msg} ')


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(b'machine_status/laser_doors')
    client.subscribe(b'machine_status/smoke_extractor')
    client.subscribe(b'machine_status/material_workspace')
    client.subscribe(b'machine_status/available_space')
    client.subscribe(b'machine_status/leds_strip')
    client.subscribe(b'machine_status/laser_camera')
    print(f'Connected to MQTT broker: {mqtt_server}')
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# ESP32
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

checking_laser_doors = False
checking_smoke_extractor = False
material_workspace = False
available_space = False
leds_strip = False
laser_camera = False

light_1 = ADC(Pin(34))
light_2 = ADC(Pin(35))
light_1.atten(ADC.ATTN_11DB)
light_2.atten(ADC.ATTN_11DB)


while True:
    try:
        client.check_msg()
        distance = sensor.distance_cm()
        light_value_1 = light_1.read()
        light_value_2 = light_2.read()
        print(distance, light_value_1, light_value_2)

        if distance <= 5 and checking_laser_doors:
            msg = b'{"laser_doors": {"source": "esp32", "status": true}}'
            client.publish(b'machine_status/laser_doors', msg)
            print(f'ESP sended: {msg} ')
            checking_laser_doors = False

        if light_value_1 >= 2000 and checking_smoke_extractor:
            msg = b'{"smoke_extractor": {"source": "esp32", "status": true}}'
            client.publish(b'machine_status/smoke_extractor', msg)
            print(f'ESP sended: {msg} ')
            checking_smoke_extractor = False

        if light_value_2 >= 2000 and material_workspace:
            msg = b'{"material_workspace": {"source": "esp32", "status": true}}'
            client.publish(b'machine_status/material_workspace', msg)
            print(f'ESP sended: {msg} ')
            material_workspace = False

    except OSError as e:
        restart_and_reconnect()

    time.sleep(0.5)


# esptool --chip esp32 --port COM7 erase_flash
# esptool --chip esp32 --port COM7 --baud 460800 write_flash -z 0x1000 'C:\Users\Charly Mercury\Downloads\ESP32_GENERIC-20240105-v1.22.1.bin'
# ampy --port COM7 put boot.py
# ampy --port COM7 put main.py
# ampy --port COM7 put hcsr04.py
# ampy --port COM7 put reset_machine.py
# ampy --port COM7 put umqttsimple.py
