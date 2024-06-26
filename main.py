"""
    The main objective of this project is to automate the process
     of cutting and engraving MDF with a laser machine

    The project is composed of the following components:
        - A module/function called machine_actuators/MachineActuators, which turn on/off
        the actuators present in the laser machine.
        - A module/function called machine_status/run_machine_status, which validates several
        characteristics before sending the laser to cut.
        - A module/function called identify_laser_machine/identifying_laser_board, which returns
        a laser machine based on the input parameter.
        - A module/class called gcode_sender/GcodeSender, which sends the input G-code to the
        previously selected laser machine.

    Use the following command in a PowerShell command prompt to connect to the Raspberry Pi using SSH:
        - ssh edumediatics@192.168.1.192

"""
import time
import logging
import datetime
import os
from src.machine_status import run_machine_status
from src.machine_actuators import MachineActuators
from src.identify_laser_machine import identifying_laser_board
from src.gcode_sender import GcodeSender
from src.mqtt_server_client import MqttServerBrokerClient


# Get the current date and time
absolute_path = os.getcwd()
print(absolute_path)
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'{absolute_path}/logs/{formatted_datetime}.log'
)


def run() -> None:
    """
    Main function.

    :param g_code_file_: name of the gcode file to send to the laser machine.
    :param laser_machine_: name of the laser machine.
    :return: None
    """
    laser_status = False
    laser_machine_parameters = {
        'port': '',
        'baud_rate': 0
    }
    machine_status = 'machine is ready to run'
    broker_address = '192.168.100.192'
    server_broker_address = '192.168.100.192'
    laser_machine_, file_path = '', ''
    mqtt_client = MqttServerBrokerClient(server_broker_address, 1883)
    machine_actuators = MachineActuators(broker_address, broker_port=1883)

    while True:
        # First State - Download gcode
        try:
            while True:
                if mqtt_client.validation_status:
                    mqtt_client.return_parameters_()
                    file_path = f"gcodes/{mqtt_client.file_name}"
                    laser_machine_ = mqtt_client.laser_machine
                    logging.info(f"Gcode has been downloaded successfully: {file_path}")
                    break
        except Exception as err:
            logging.error(f'An error occurred: {err}', exc_info=True)

        print("First State -  Download gcode:  PASSED ")

        # Second State - Turn On Actuators and checking Machine State
        try:
            machine_actuators.turn_on_off_actuators(False)
            machine_actuators.turn_on_off_actuators(True)
            # machine_status = run_machine_status(broker_address)
            if machine_status == "machine is ready to run":
                logging.info("Machine Status validated: let's get the machine name")
        except Exception as err:
            logging.error(f'An error occurred: {err}', exc_info=True)

        try:
            if machine_status == "machine is ready to run":
                laser_machine_parameters = identifying_laser_board(laser_machine_)
                logging.info(f"Machine Name: {laser_machine_parameters}")
            else:
                raise Exception("The Machine is not ready to run")
        except Exception as err:
            logging.error(f'An error occurred: {err}', exc_info=True)

        print("Second State -  Actuators and Sensors:  PASSED ")
        time.sleep(5)
        # Third State - Send Gcode
        try:
            g_code_sender = GcodeSender(
                laser_machine_parameters['port'],
                laser_machine_parameters['baud_rate'],
                laser_machine_
                )
            connection_response = g_code_sender.connection()
            if connection_response == f'Serial connection established on ' \
                                      f'{laser_machine_parameters["port"]} at ' \
                                      f'{laser_machine_parameters["baud_rate"]} bps.':
                laser_status = True
                logging.info(f" Connected to laser machine: {connection_response}")
            elif connection_response == 'Serial Connection Failed':
                laser_status = False

            if laser_status:
                time.sleep(4)
                logging.info(f"Sending Gcode to machine: {file_path}")
                print(file_path)
                g_code_sender_status = g_code_sender.send_g_code(gcode_path=file_path)

                if g_code_sender_status == 'Finished':
                    logging.info("Finishing job.")
                    os.remove(f"./gcodes/{mqtt_client.file_name}")
                    machine_actuators.turn_on_off_actuators(False)
                    g_code_sender.close_serial_connection()
            else:
                raise Exception(" Problem to connect to machine ")
        except Exception as err:
            logging.error(f'An error occurred: {err}', exc_info=True)

        print("Third State -  Send Gcode:  PASSED ")


if __name__ == "__main__":
    run()
