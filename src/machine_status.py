import threading
import json
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

    def __init__(self, mqtt_server, broker_port):
        self.mqtt_client = MqttClient(mqtt_server,
                                      broker_port=broker_port,
                                      on_message_callback=self.on_message_callback)
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(TOPICS)
        self.publishing_request = False

    @staticmethod
    def on_message_callback(client, userdata, msg):

        global laser_doors, smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

        # client_id = self.mqtt_client.get_client_id()
        # Ignore messages sent by this client
        # if msg.topic == f"your/topic/{client_id}":
            # print("Ignoring message sent by this client.")
            # return

        if msg.topic == 'machine_status/laser_doors':
            payload_message = json.loads(msg.payload.decode())
            laser_doors = payload_message['laser_doors']['status']

        if msg.topic == 'machine_status/smoke_extractor':
            payload_message = json.loads(msg.payload.decode())
            smoke_extractor = payload_message['smoke_extractor']['status']

        if msg.topic == 'machine_status/material_workspace':
            payload_message = json.loads(msg.payload.decode())
            material_workspace = payload_message['material_workspace']['status']

        if msg.topic == 'machine_status/available_space':
            payload_message = json.loads(msg.payload.decode())
            available_space = payload_message['available_space']['status']

        if msg.topic == 'machine_status/leds_strip':
            payload_message = json.loads(msg.payload.decode())
            leds_strip = payload_message['leds_strip']['status']

        if msg.topic == 'machine_status/laser_camera':
            payload_message = json.loads(msg.payload.decode())
            laser_camera = payload_message['laser_camera']['status']

    def laser_doors_status(self):
        if not self.publishing_request:
            status = {'laser_doors': {'status': False}}
            self.mqtt_client.publish("machine_status/laser_doors", json.dumps(status))
            self.publishing_request = True

    def smoke_extractor_status(self):
        if not self.publishing_request:
            status = {'smoke_extractor': {'status': False}}
            self.mqtt_client.publish("machine_status/smoke_extractor", json.dumps(status))
            self.publishing_request = True

    def material_workspace_status(self):
        if not self.publishing_request:
            status = {'material_workspace': {'status': False}}
            self.mqtt_client.publish("machine_status/material_workspace", json.dumps(status))
            self.publishing_request = True

    def available_space_status(self):
        if not self.publishing_request:
            status = {'available_space': {'status': False}}
            self.mqtt_client.publish("machine_status/available_space", json.dumps(status))
            self.publishing_request = True

    def leds_strip_status(self):
        if not self.publishing_request:
            status = {'leds_strip': {'status': False}}
            self.mqtt_client.publish("machine_status/leds_strip", json.dumps(status))
            self.publishing_request = True

    def laser_camera_status(self):
        if not self.publishing_request:
            status = {'laser_camera': {'status': False}}
            self.mqtt_client.publish("machine_status/laser_camera", json.dumps(status))
            self.publishing_request = True


def run_machine_status():
    global laser_doors, smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

    machine_status = MachineStatus("192.168.0.23", broker_port=1883)

    while True:

        if not laser_doors:
            machine_status.laser_doors_status()

        if laser_doors and not smoke_extractor and machine_status.publishing_request:
            machine_status.publishing_request = False
            machine_status.smoke_extractor_status()

        if laser_doors and smoke_extractor and not material_workspace and machine_status.publishing_request:
            machine_status.publishing_request = False
            machine_status.material_workspace_status()

        if laser_doors and smoke_extractor and material_workspace and not available_space \
                and machine_status.publishing_request:
            machine_status.publishing_request = False
            machine_status.available_space_status()

        if laser_doors and smoke_extractor and material_workspace and available_space \
                and not leds_strip and machine_status.publishing_request:
            machine_status.publishing_request = False
            machine_status.leds_strip_status()

        if laser_doors and smoke_extractor and material_workspace and \
                available_space and leds_strip and not laser_camera and machine_status.publishing_request:
            machine_status.publishing_request = False
            machine_status.laser_camera_status()

        if laser_doors and smoke_extractor and material_workspace and available_space and \
                leds_strip and laser_camera:
            machine_status_message_ = 'machine is ready to run'
            break

    return machine_status_message_


"""
mosquitto_pub -h 192.168.0.23 -p 1883 -t "machine_status/laser_doors" -m '{"laser_doors": {"status": true}}'
mosquitto_pub -h 192.168.0.23 -p 1883 -t "machine_status/smoke_extractor" -m '{"smoke_extractor": {"status": true}}'
mosquitto_pub -h 192.168.0.23 -p 1883 -t "machine_status/material_workspace" -m '{"material_workspace": {"status": true}}'
mosquitto_pub -h 192.168.0.23 -p 1883 -t "machine_status/available_space" -m '{"available_space": {"status": true}}'
mosquitto_pub -h 192.168.0.23 -p 1883 -t "machine_status/leds_strip" -m '{"leds_strip": {"status": true}}'
mosquitto_pub -h 192.168.0.23 -p 1883 -t "machine_status/laser_camera" -m '{"laser_camera": {"status": true}}'
"""