"""

    This class manages exchange of data with a mqtt broker.

In Raspberry, For Local mqtt broker I have the following configuration in

    - $ sudo nano /etc/mosquitto/mosquitto.conf

Add the following lines to the file

    - allow_anonymous true
    - listener 1883

Restart the service

    - $ sudo service mosquitto restart

Verify the configuration:

    - $ sudo netstat -tulpn | grep 1883

Mqtt client publisher

    - $ mosquitto_pub -h 192.168.1.192 -p 1883 -t "my/topic" -m "Hello, MQTT!"

Mqtt client subscriber

    - $ mosquitto_sub -h 192.168.1.192 -p 1883 -t my/topic

"""
import time
import paho.mqtt.client as mqtt


class MqttClient:
    """
        Mqtt client
    """

    def __init__(self, broker_address, broker_port: int = 1883, username=None, password=None, on_message_callback=None):
        """
        We have the following parameters for the class constructor.

        :param broker_address: address of the broker
        :param broker_port:  port of the broker
        :param username: username if exists
        :param password: password of user
        :param on_message_callback: function for mqtt subscriptions
        """
        self.client = mqtt.Client(client_id="raspberry")
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.username = username
        self.password = password

        # Set callbacks
        self.client.on_connect = self.__on_connect__
        self.client.on_disconnect = self.__on_disconnect__

        # Set on_message callback dynamically
        if on_message_callback:
            self.client.on_message = on_message_callback
        else:
            self.client.on_message = self.__default_on_message__

        self.client_id = None

    def __on_connect__(self, client, userdata, flags, rc):
        """
        Mqtt Client initializing method.

        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        print(self.validate_connection)
        print(f"Connected with result code {rc}")
        # self.client_id = client._client_id.decode()

    def __on_disconnect__(self, client, userdata, rc):
        """
        Mqtt Client finalizing method.

        :param client:
        :param userdata:
        :param rc:
        :return:
        """
        self.client.loop_stop()
        self.client.disconnect()
        print(self.validate_connection)
        print(f"Disconnected with result code {rc}")

    def __default_on_message__(self, client, userdata, msg):
        """
        Default method for subscribing topics.

        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        if msg.topic == f"your/topic/{self.client_id}":
            print("Ignoring message sent by this client.")
            return
        print(self.validate_connection)
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    def connect(self, type_of_connection: str = 'loop_start', topics=None):
        """
        Connection Method

        :return:
        """
        if topics is None:
            topics = []
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_address, self.broker_port, 60)
        if type_of_connection == 'loop_start':
            self.client.loop_start()
        elif type_of_connection == 'loop_forever':
            self.subscribe(topics)
            self.client.loop_forever()

    def disconnect_client(self):
        """
        Disconnection Method

        :return:
        """
        self.client.on_disconnect(self.client, self.client._userdata, 0)

    def publish(self, topic, message):
        """
        Publishing Method

        :param topic:
        :param message:
        :return:
        """
        self.client.publish(topic, message)

    def subscribe(self, topics):
        """
        Subscribing Method

        :param topics:
        :return:
        """
        for topic in topics:
            # print(f"Subscribing to {topics}")
            self.client.subscribe(topic)

    def validate_connection(self):
        """
        Validationg Method of mqtt conection

        :return:
        """
        return self.client.is_connected()

    def get_client_id(self):
        """
        Client Id Method

        :return:
        """
        return self.client.client_id


# Example usage:
# Define a custom on_message callback
# def custom_on_message(client, userdata, msg):
#     print(f"Custom on_message: Received message on topic {msg.topic}: {msg.payload.decode()}")
# Example usage:
# mqtt_client = MqttClient("192.168.0.23", broker_port=1883,
# username="Routiva_Laser", password="your_password", on_message_callback=custom_on_message)
# mqtt_client.connect()
# mqtt_client.subscribe("test/topic")
# mqtt_client.publish("test/topic", "Hello I am Charly Mercury from laser")
# time.sleep(1)
# mqtt_client.disconnect()
