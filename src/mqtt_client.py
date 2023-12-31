"""

In Raspberry, I have the following configuration in

    - $ sudo nano /etc/mosquitto/mosquitto.conf

Add the following lines to the file

    - allow_anonymous true
    - listener 1883

Restart the service

    - $ sudo service mosquitto restart

Verify the configuration:

    - $ sudo netstat -tulpn | grep 1883

Mqtt client publisher

    - $ mosquitto_pub -h 192.168.0.23 -p 1883 -t "my/topic" -m "Hello, MQTT!"

Mqtt client subscriber

    - $ mosquitto_sub -h 192.168.0.23 -p 1883 -t my/topic

"""
import time

import paho.mqtt.client as mqtt


class MqttClient:

    def __init__(self, broker_address, broker_port=1883, username=None, password=None):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.username = username
        self.password = password

        # Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(self.validate_connection)
        print(f"Connected with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(self.validate_connection)
        print(f"Disconnected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(self.validate_connection)
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    def connect(self):
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def validate_connection(self):
        return self.client.is_connected()


# Example usage:
mqtt_client = MqttClient("192.168.0.23", broker_port=1883)  # , username="Routiva_Laser", password="your_password")
mqtt_client.connect()
mqtt_client.subscribe("test/topic")
mqtt_client.publish("test/topic", "Hello I am Charly Mercury from laser")
time.sleep(1)
mqtt_client.disconnect()
