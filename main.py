"""
    The main objective of this project is to automate the process
     of cutting and engraving MDF with a laser machine

    The project is composed of the following components:
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


def run(g_code_file_: str, laser_machine_: str) -> None:
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
    broker_address = '192.168.1.192'  # 'broker.hivemq.com'
    machine_actuators = MachineActuators(broker_address, broker_port=1883)
    machine_actuators.turn_on_off_extractor(False)
    machine_actuators.turn_on_off_led_lights(False)

    try:
        time.sleep(1)
        machine_actuators.turn_on_off_extractor(True)
        time.sleep(1)
        machine_actuators.turn_on_off_led_lights(True)
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

    try:
        g_code_sender = GcodeSender(
            laser_machine_parameters['port'],
            laser_machine_parameters['baud_rate'])
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
            logging.info(f"Sending Gcode to machine: {g_code_file_}")
            # g_code_sender_status = g_code_sender.send_g_code(gcode_path=g_code_file_)
            g_code_sender_status = 'Finished'
            if g_code_sender_status == 'Finished':
                logging.info("Finishing job.")
                time.sleep(1)
                machine_actuators.turn_on_off_extractor(False)
                time.sleep(1)
                machine_actuators.turn_on_off_led_lights(False)
                g_code_sender.close_serial_connection()
        else:
            raise Exception(" Problem to connect to machine ")
    except Exception as err:
        logging.error(f'An error occurred: {err}', exc_info=True)


if __name__ == "__main__":
    new_file = 'example_3_cajita_6_6'
    g_code_file = f"examples/{new_file}.gcode"
    laser_machine = 'sculpfun_s30_90_90'
    run(g_code_file, laser_machine)
