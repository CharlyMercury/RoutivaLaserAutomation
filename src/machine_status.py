import threading
from mqtt_client import MqttClient

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

    def on_message_callback(self, client, userdata, msg):

        global laser_doors, smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

        client_id = self.mqtt_client.get_client_id()
        # Ignore messages sent by this client
        if msg.topic == f"your/topic/{client_id}":
            print("Ignoring message sent by this client.")
            return

        if msg.topic == 'machine_status/laser_doors':
            payload_message = msg.payload.decode
            laser_doors = payload_message['laser_doors']['status']

        if msg.topic == 'machine_status/smoke_extractor':
            payload_message = msg.payload.decode
            smoke_extractor = payload_message['smoke_extractor']['status']

        if msg.topic == 'machine_status/material_workspace':
            payload_message = msg.payload.decode
            material_workspace = payload_message['material_workspace']['status']

        if msg.topic == 'machine_status/available_space':
            payload_message = msg.payload.decode
            available_space = payload_message['available_space']['status']

        if msg.topic == 'machine_status/leds_strip':
            payload_message = msg.payload.decode
            leds_strip = payload_message['leds_strip']['status']

        if msg.topic == 'machine_status/laser_camera':
            payload_message = msg.payload.decode
            laser_camera = payload_message['laser_camera']['status']

    def laser_doors_status(self):
        status = {'laser_doors': {'status': False}}
        self.mqtt_client.publish("machine_status/laser_doors", status)

    def smoke_extractor_status(self):
        status = {'smoke_extractor': {'status': False}}
        self.mqtt_client.publish("machine_status/smoke_extractor", status)

    def material_workspace_status(self):
        status = {'material_workspace': {'status': False}}
        self.mqtt_client.publish("machine_status/material_workspace", status)

    def available_space_status(self):
        status = {'available_space': {'status': False}}
        self.mqtt_client.publish("machine_status/available_space", status)

    def leds_strip_status(self):
        status = {'leds_strip': {'status': False}}
        self.mqtt_client.publish("machine_status/leds_strip", status)

    def laser_camera_status(self):
        status = {'laser_camera': {'status': False}}
        self.mqtt_client.publish("machine_status/laser_camera", status)


def run():
    global laser_doors, smoke_extractor, material_workspace, available_space, leds_strip, laser_camera

    while not laser_doors and \
            not smoke_extractor and \
            not material_workspace and \
            not available_space and not leds_strip and \
            not laser_camera:
        return True


if __name__ == '__main__':
    machine_status = MachineStatus("192.168.0.23", broker_port=1883)
    # Create a daemon thread
    daemon_thread = threading.Thread(target=run)
    daemon_thread.daemon = True
    daemon_thread.start()
