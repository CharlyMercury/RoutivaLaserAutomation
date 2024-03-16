"""
    This module turn on/off all the machine actuators (motors & lights) before cutting and engraving
    with the laser machine.

    The characteristics are as follows:

        - Smoke extractor: This characteristic checks if the smoke extractor is turned on.
        - LED lights: This characteristic checks if the LED strip is turned on.

    Useful mosquitto commands:

        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/smoke_extractor_actuator"
            -m '{"smoke_extractor": {"source": "raspberry", "status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/leds_lights"
            -m '{"leds_lights": {"source": "raspberry", "status": true}}'

"""
import json
import logging
from src.mqtt_client import MqttClient

TOPICS = [
    'machine_status/smoke_extractor_actuator',
    'machine_status/leds_lights'
]


class MachineActuators:
    """

    This class contains all the methods and attributes to validate the characteristics that can be
    checked before cutting and engraving with the laser machine.

    MQTT is the protocol used to connect with the sensors and actuators.

    """
    def __init__(self, mqtt_broker_address: str, broker_port: int):
        """
        Constructor of the class

        :param mqtt_broker_address: mqtt broker address
        :param broker_port: mqtt broker port
        """
        self.mqtt_client = MqttClient(broker_address=mqtt_broker_address,
                                      broker_port=broker_port,
                                      on_message_callback=self.on_message_callback)
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(TOPICS)

    def on_message_callback(self, client, userdata, msg):
        """
        The method is invoked when a message is received on a subscribed topic.

        If the msg contains information of a characteristics, then is validated the information.

        :param client:
        :param userdata:
        :param msg: incoming message
        :return:
        """
        print(msg)

    def pub_message(self, destination: str, status: bool = False):
        """
        Method to publish a message to a specific topic

        :param status: status of the actuator
        :param destination: name of the characteristic to be validated
        :return:
        """
        message = {destination: {'source': 'raspberry', 'status': status}}
        topic = f"machine_status/{destination}"
        self.mqtt_client.publish(topic, json.dumps(message))
        logging.info(f'Topic: {topic}. Message sent to esp32: {message}')

    def turn_on_off_extractor(self, state):
        self.pub_message("smoke_extractor", state)

    def turn_on_off_led_lights(self, state):
        self.pub_message("leds_lights", state)


def run_machine_actuators(broker_server_address: str, actuators_state: bool = False):
    """

    Method tu start the machine status validation.

    :param actuators_state: state of the actuators
    :param broker_server_address: address of the mqtt broker
    :return:
    """
