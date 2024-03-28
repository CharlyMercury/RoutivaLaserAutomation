from src.mqtt_client import MqttClient
from src.download_file_google_drive import GoogleDriveUtilities
import json

global file_name, laser_machine

machine_names = [
    'sculpfun_s9_proofs',
    'sculpfun_s30_90_90',
    'sculpfun_s30_40_40_rotatory'
]

mdf_types = [
    'natural_mdf',
    'varnished_mdf'
]

subscribing_topics = [
    'routiva_server/trigger_cutting'
]

publishing_topics = {
    "confirmation_trigger_cutting": "routiva_server/confirmation_trigger_cutting"
}


def validating_coming_information(msg_incoming_data: dict) -> tuple:
    global file_name, laser_machine

    if msg_incoming_data["machine_name"] in machine_names:
        if msg_incoming_data["mdf_type"] in mdf_types:
            if msg_incoming_data["file_name"] != "":
                if msg_incoming_data["folder_id"] != "":

                    print("Downloading File from Google Drive")

                    folder_id = msg_incoming_data["folder_id"]
                    file_name = msg_incoming_data['file_name']
                    credentials = msg_incoming_data['credentials']

                    google_drive_ = GoogleDriveUtilities(folder_id, credentials)
                    download_status, download_message = google_drive_.download_file(file_name)
                    google_drive_.delete_token_file()
                    remove_status, remove_message = google_drive_.remove_file_gdrive()

                    if download_status and remove_status:
                        validation_status = True
                        validation_error = "No errors"
                    else:
                        validation_status = False
                        validation_error = f"{download_message}, {remove_message}"
                else:
                    validation_status = False
                    validation_error = "Wrong file url"
            else:
                validation_status = False
                validation_error = "Wrong cutting file"
        else:
            validation_status = False
            validation_error = "Wrong mdf type"
    else:
        validation_status = False
        validation_error = "Wrong machine name"

    return validation_status, validation_error


class MqttServerBrokerClient:

    def __init__(self, mqtt_broker_address, broker_port):
        """
        Constructor of the class

        :param mqtt_broker_address: mqtt broker address
        :param broker_port: mqtt broker port
        """
        self.mqtt_client = MqttClient(broker_address=mqtt_broker_address,
                                      broker_port=broker_port,
                                      on_message_callback=self.on_message_callback)
        self.mqtt_client.connect('loop_forever', topics=subscribing_topics)
        self.file_name = ''
        self.laser_machine = ''

    def on_message_callback(self, client, userdata, msg):

        global file_name, laser_machine

        if msg.topic == 'routiva_server/trigger_cutting':

            message_in = json.loads(msg.payload.decode())
            file_name = message_in['file_name']
            laser_machine = message_in['machine_name']
            validation_status, validation_error = validating_coming_information(message_in)

            if validation_status and validation_error == "No errors":
                self.mqtt_client.publish(publishing_topics["confirmation_trigger_cutting"], "Initializing Cutting Process")
                self.mqtt_client.disconnect_client()
            if not validation_status:
                self.mqtt_client.publish(publishing_topics["confirmation_trigger_cutting"], validation_error)

        if msg.topic == 'routiva_server/confirmation_status_machine':

            print('')

    def return_parameters_(self):
        global file_name, laser_machine
        self.file_name = file_name
        self.laser_machine = laser_machine
