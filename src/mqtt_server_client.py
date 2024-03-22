from src.mqtt_client import MqttClient
from src.download_file_google_drive import GoogleDriveUtilities


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

    if msg_incoming_data["machine_name"] in machine_names:
        if msg_incoming_data["mdf_type"] in mdf_types:
            if msg_incoming_data["file_name"] != "":
                if msg_incoming_data["folder_id"] != "":

                    print("downloading_file")

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

    def on_message_callback(self, client, userdata, msg):

        print(msg.topic, msg.payload.decode())

        if msg.topic == 'routiva_mqtt_broker/trigger_cutting':
            validation_status, validation_error = validating_coming_information(msg.payload.decode())

            if validation_status and validation_error == "No errors":
                self.mqtt_client.publish(publishing_topics["confirmation_trigger_cutting"], "Initializing Cutting Process")
            if not validation_status:
                self.mqtt_client.publish(publishing_topics["confirmation_trigger_cutting"], validation_error)

        if msg.topic == 'routiva_mqtt_broker/confirmation_status_machine':

            print('')


"""message = {
    "machine_name": "sculpfun_s30_90_90", 
    "mdf_type": "natural_mdf",
    "file_name": "pedido_31_ago.gcode",
    "folder_id": "1Clv8oI2A3zdSZeqg5oFlXGLsxFN6GhKL",
    "credentials": 
        {"access_token": "ya29.a0Ad52N39FPIly7SfyGzckS25yYgm6_ZaDE2IBmhj_Pbksu0TmJOxXVeWZPOq8VDsxq4c_VdbFc8rYJXFaONrtzAWl3P3zWerTgQVejq-pWhij6nctpOftDwU_pEDLtc3tPdQCPo_cpdNrgpVVH-skugsDtnxTLnc7WV0vaCgYKAfESARASFQHGX2Mi42C2Cgpdt3lJ92ROtYr_5A0171",
        "client_id": "965793021308-sim1mdfeke46riovdc6kg4pl5mtmntt3.apps.googleusercontent.com",
        "client_secret": "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",
        "refresh_token": "1//0f9aBDF0SNUqoCgYIARAAGA8SNwF-L9IrK7oHGXS5sCwwsblyhFdc8O2KEwC5NJ2zzT2_7Wv8hsVr4R1D_OZNBxIvw4ros4g7Loo",
        "token_expiry": "2024-03-22T16:58:19Z",
        "token_uri": "https://oauth2.googleapis.com/token",
        "user_agent": None,
        "revoke_uri": "https://oauth2.googleapis.com/revoke",
        "id_token": None,
        "id_token_jwt": None,
        "token_response": {
            "access_token": "ya29.a0Ad52N39FPIly7SfyGzckS25yYgm6_ZaDE2IBmhj_Pbksu0TmJOxXVeWZPOq8VDsxq4c_VdbFc8rYJXFaONrtzAWl3P3zWerTgQVejq-pWhij6nctpOftDwU_pEDLtc3tPdQCPo_cpdNrgpVVH-skugsDtnxTLnc7WV0vaCgYKAfESARASFQHGX2Mi42C2Cgpdt3lJ92ROtYr_5A0171",
            "expires_in": 3599,
            "refresh_token": "1//0f9aBDF0SNUqoCgYIARAAGA8SNwF-L9IrK7oHGXS5sCwwsblyhFdc8O2KEwC5NJ2zzT2_7Wv8hsVr4R1D_OZNBxIvw4ros4g7Loo",
            "scope": "https://www.googleapis.com/auth/drive",
            "token_type": "Bearer"
        },
        "scopes": [
            "https://www.googleapis.com/auth/drive"
        ],
        "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
        "invalid": False,
        "_class": "OAuth2Credentials",
        "_module": "oauth2client.client"
        }
}"""
