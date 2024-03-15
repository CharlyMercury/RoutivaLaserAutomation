# Complete project details at https://RandomNerdTutorials.com
import json
import time

from machine import Pin, ADC

global turning_onoff_smoke_extractor, turning_onoff_led_lights, smoke_extractor_status, leds_strip_status


def sub_cb(topic, msg):
    global turning_onoff_smoke_extractor, turning_onoff_led_lights, smoke_extractor_status, leds_strip_status

    print(topic, msg)

    payload_message = json.loads(msg.decode('utf-8'))

    if 'smoke_extractor' in payload_message:
        smoke_extractor_source = payload_message['smoke_extractor']['source']
        smoke_extractor_status = payload_message['smoke_extractor']['status']

        if smoke_extractor_source == 'raspberry' \
                and topic == b'machine_status/smoke_extractor_actuator':
            turning_onoff_smoke_extractor = True
            print(f'ESP received: {msg} ')

    if 'leds_lights' in payload_message:
        leds_strip_source = payload_message['leds_lights']['source']
        leds_strip_status = payload_message['leds_lights']['status']

        if leds_strip_source == 'raspberry' \
                and topic == b'machine_status/leds_lights':
            turning_onoff_led_lights = True
            print(f'ESP received: {msg} ')


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(b'machine_status/smoke_extractor_actuator')
    client.subscribe(b'machine_status/leds_lights')
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

turning_onoff_led_lights = False
turning_onoff_smoke_extractor = False

pins_output_extractor = Pin(32, Pin.OUT)
pins_output_extractor.on()

pins_output_led_light = Pin(33, Pin.OUT)
pins_output_led_light.on()


while True:
    try:
        client.check_msg()

        if turning_onoff_smoke_extractor:
            print("Here")
            if smoke_extractor_status:
                pins_output_extractor.off()
            elif not smoke_extractor_status:
                pins_output_extractor.on()

            turning_onoff_smoke_extractor = False

        if turning_onoff_led_lights:

            if leds_strip_status:
                pins_output_led_light.off()
            elif not leds_strip_status:
                pins_output_led_light.on()

            turning_onoff_led_lights = False

    except OSError as e:
        restart_and_reconnect()

    time.sleep(0.5)
