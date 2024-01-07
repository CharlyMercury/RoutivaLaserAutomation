# Complete project details at https://RandomNerdTutorials.com

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'machine_status/laser_doors':
        print(f'ESP received: {msg} ')


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
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


while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            distance = str(sensor.distance_cm()).encode()
            msg = b'{"laser_doors": {"source": esp32, "status": true}}' + distance
            client.publish(topic_pub, msg)
            last_message = time.time()
    except OSError as e:
        restart_and_reconnect()

# esptool --chip esp32 --port COM7 erase_flash
# esptool --chip esp32 --port COM7 --baud 460800 write_flash -z 0x1000 'C:\Users\Charly Mercury\Downloads\ESP32_GENERIC-20240105-v1.22.1.bin'

# ampy --port COM7 put boot.py
# ampy --port COM7 put main.py
# ampy --port COM7 put hcsr04.py
# ampy --port COM7 put reset_machine.py
# ampy --port COM7 put umqttsimple.py
