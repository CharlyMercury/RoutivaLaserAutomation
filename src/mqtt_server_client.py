import time
from mqtt_client import MqttClient
from download_file_google_drive import GoogleDriveUtilities


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
    'routiva_server/trigger_cutting',
]

publishing_topics = {
    "confirmation_trigger_cutting": "routiva_server/confirmation_trigger_cutting"
}


def validating_coming_information(msg_incoming_data: dict) -> tuple:

    if msg_incoming_data["machine_name"] in machine_names:
        if msg_incoming_data["mdf_type"] in mdf_types:
            if msg_incoming_data["file_name"] != "":
                if msg_incoming_data["folder_id"] != "":

                    print("downloading_file")

                    folder_id = msg_incoming_data["folder_id"]
                    file_name = msg_incoming_data['file_name']
                    google_drive_ = GoogleDriveUtilities(folder_id)
                    download_status, download_message = google_drive_.download_file(file_name)
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


def custom_on_message(client, userdata, msg):

    if msg.topic == 'routiva_mqtt_broker/trigger_cutting':
        validation_status, validation_error = validating_coming_information(msg.payload.decode())

        if validation_status and validation_error == "No errors":
            mqtt_client.publish(publishing_topics["confirmation_trigger_cutting"], "Initializing Cutting Process")
        if not validation_status:
            mqtt_client.publish(publishing_topics["confirmation_trigger_cutting"], validation_error)

    if msg.topic == 'routiva_mqtt_broker/confirmation_status_machine':

        print('')


mqtt_client = MqttClient('broker.hivemq.com', broker_port=1883,
                         username="Routiva_Laser", password="your_password",
                         on_message_callback=custom_on_message)
mqtt_client.connect()
mqtt_client.subscribe(subscribing_topics)
time.sleep(1)
mqtt_client.disconnect()
