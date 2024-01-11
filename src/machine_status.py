"""
    This module validates all the characteristics that can be checked before cutting and engraving
    with the laser machine.

    The characteristics are as follows:

        - Laser doors: This characteristic checks if the doors of the laser machine are closed.
        - Smoke extractor: This characteristic checks if the smoke extractor is turned on.
        - Material workspace: This characteristic checks if there is material on the workspace area.
        - Available space: This characteristic checks if there is available space in the MDF for the new design.
        - LED strip: This characteristic checks if the LED strip is turned on.
        - Laser camera: This characteristic checks if the laser camera is working.


    Useful mosquitto commands:

        - mosquitto_pub -h 192.168.0.12 -p 1883 -t "machine_status/laser_doors" -m '{"laser_doors": {"status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/laser_doors" -m '{"laser_doors": {"status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/smoke_extractor" -m
            '{"smoke_extractor": {"status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/material_workspace" -m
            '{"material_workspace": {"status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/available_space" -m
            '{"available_space": {"status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/leds_strip" -m '{"leds_strip": {"status": true}}'
        - mosquitto_pub -h 192.168.1.192 -p 1883 -t "machine_status/laser_camera" -m
            '{"laser_camera": {"status": true}}'
        - mosquitto_sub -h broker.hivemq.com -p 1883 -t "machine_status/laser_doors" -q 1
        - mosquitto_pub -h broker.hivemq.com -p 1883 -t "machine_status/laser_doors" -m
            '{"laser_doors": {"source": "raspberry", "status": false}}'

    How to improve this code:
        - Task: Start with a publication to a topic called machine_status/starting_validation
          and the device should respond with a message to the same topic that it has started
          the process of validate characteristics.
        - Task: Same as above but to end the process.

"""
import json
import logging
from src.mqtt_client import MqttClient

laser_doors = False
smoke_extractor = False
material_workspace = False
available_space = False
leds_strip = False
laser_camera = False
TOPICS = [
    'machine_status/laser_doors',
    'machine_status/smoke_extractor',
    'machine_status/material_workspace',
    'machine_status/available_space',
    'machine_status/leds_strip',
    'machine_status/laser_camera'
]


class MachineStatus:
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
        self.publishing_request = False
        self.decoded_message = tuple

    def on_message_callback(self, client, userdata, msg):
        """
        The method is invoked when a message is received on a subscribed topic.

        If the msg contains information of a characteristics, then is validated the information.

        :param client:
        :param userdata:
        :param msg: incoming message
        :return:
        """
        global laser_doors, smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

        client_id = self.mqtt_client.get_client_id()
        if msg.topic == f"machine_status/laser_doors/{client_id}":
            print("Ignoring message sent by this client.")
            return

        if msg.topic == 'machine_status/laser_doors':
            laser_doors_source, laser_doors = self.decoding_topic_message(destination='laser_doors', message=msg)
            if laser_doors_source == 'esp32' and laser_doors:
                self.publishing_request = False

        if msg.topic == 'machine_status/smoke_extractor':
            smoke_extractor_source, smoke_extractor = self.decoding_topic_message(
                destination='smoke_extractor', message=msg)
            if smoke_extractor_source == 'esp32' and smoke_extractor:
                self.publishing_request = False

        if msg.topic == 'machine_status/material_workspace':
            material_workspace_source, material_workspace = self.decoding_topic_message(
                destination='material_workspace', message=msg)
            if material_workspace_source == 'esp32' and material_workspace:
                self.publishing_request = False

        if msg.topic == 'machine_status/available_space':
            available_space_source, available_space = self.decoding_topic_message(
                destination='available_space', message=msg)
            if available_space_source == 'esp32' and available_space:
                self.publishing_request = False

        if msg.topic == 'machine_status/leds_strip':
            leds_strip_source, leds_strip = self.decoding_topic_message(destination='leds_strip', message=msg)
            if leds_strip_source == 'esp32' and leds_strip:
                self.publishing_request = False

        if msg.topic == 'machine_status/laser_camera':
            laser_camera_source, laser_camera = self.decoding_topic_message(destination='laser_camera', message=msg)
            if laser_camera_source == 'esp32' and laser_camera:
                self.publishing_request = False

    def decoding_topic_message(self, destination: str, message) -> tuple:
        payload_message = json.loads(message.payload.decode())
        characteristic_source = payload_message[destination]['source']
        characteristic_status = payload_message[destination]['status']
        self.decoded_message = characteristic_source, characteristic_status
        logging.info(f'Topic: machine_status/{destination}. Message received from esp32: {message}')
        return self.decoded_message

    def pub_message(self, destination: str):
        """
        Method to publish a message to a specific topic

        :param destination: name of the characteristic to be validated
        :return:
        """
        message = {destination: {'source': 'raspberry', 'status': False}}
        topic = f"machine_status/{destination}"
        self.mqtt_client.publish(topic, json.dumps(message))
        logging.info(f'Topic: {topic}. Message sent to esp32: {message}')

    def laser_doors_status(self):
        """
        Method to publish that the doors of the laser machine should be validated

        :return:
        """
        if not self.publishing_request:
            self.pub_message(destination='laser_doors')
            self.publishing_request = True

    def smoke_extractor_status(self):
        """
        Method to publish that the Smoke extractor should be validated

        :return:
        """
        if not self.publishing_request:
            self.pub_message(destination='smoke_extractor')
            self.publishing_request = True

    def material_workspace_status(self):
        """
        Method to publish that the material workspace area should be validated

        :return:
        """
        if not self.publishing_request:
            self.pub_message(destination='material_workspace')
            self.publishing_request = True

    def available_space_status(self):
        """
        Method to publish that the available space should be validated

        :return:
        """
        if not self.publishing_request:
            self.pub_message(destination='available_space')
            self.publishing_request = True

    def leds_strip_status(self):
        """
        Method to publish that the leds strips should be validated

        :return:
        """
        if not self.publishing_request:
            self.pub_message(destination='leds_strip')
            self.publishing_request = True

    def laser_camera_status(self):
        """
        Method to publish that the laser camera should be validated

        :return:
        """
        if not self.publishing_request:
            self.pub_message(destination='laser_camera')
            self.publishing_request = True


def run_machine_status(broker_server_address: str):
    """

    Method tu start the machine status validation.

    :param broker_server_address: address of the mqtt broker
    :return:
    """
    global laser_doors, smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

    machine_status = MachineStatus(broker_server_address, broker_port=1883)

    while True:

        if not laser_doors and not machine_status.publishing_request:
            machine_status.laser_doors_status()

        if laser_doors and not smoke_extractor and not machine_status.publishing_request:
            print(" Estado de las puertas del Láser: Cerradas")
            machine_status.smoke_extractor_status()

        if laser_doors and smoke_extractor and not material_workspace and not machine_status.publishing_request:
            print("Smoke Extractor Validated")
            machine_status.material_workspace_status()

        if laser_doors and smoke_extractor and material_workspace and not available_space \
                and not machine_status.publishing_request:
            print("Material Workspace Validated")
            machine_status.available_space_status()

        if laser_doors and smoke_extractor and material_workspace and available_space \
                and not leds_strip and not machine_status.publishing_request:
            print("Available Space Validated")
            machine_status.leds_strip_status()

        if laser_doors and smoke_extractor and material_workspace and \
                available_space and leds_strip and not laser_camera and not machine_status.publishing_request:
            print("Leds Strip Validated")
            machine_status.laser_camera_status()

        if laser_doors and smoke_extractor and material_workspace:
            # and available_space and leds_strip and laser_camera:
            # print("Laser Camera Validated")
            machine_status_message_ = 'machine is ready to run'
            break

    return machine_status_message_
