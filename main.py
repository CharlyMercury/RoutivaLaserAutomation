"""
    With this script we can send G-code commands to the laser machine.
"""
import time

from src.identify_laser_machine import identifying_laser_board
from src.gcode_sender import GcodeSender


def run(g_code_file_, laser_machine_):

    laser_status = False

    laser_machine_parameters = identifying_laser_board(laser_machine_)
    g_code_sender = GcodeSender(
        laser_machine_parameters['port'],
        laser_machine_parameters['baud_rate'])

    connection_response = g_code_sender.connection()
    if connection_response == f'Serial connection established on ' \
                              f'{laser_machine_parameters["port"]} at ' \
                              f'{laser_machine_parameters["baud_rate"]} bps.':
        laser_status = True
    elif connection_response == 'Serial Connection Failed':
        laser_status = False

    if laser_status:
        time.sleep(4)
        g_code_sender_status = g_code_sender.send_g_code(gcode_path=g_code_file_)
        if g_code_sender_status == 'Finished':
            g_code_sender.close_serial_connection()


if __name__ == "__main__":

    new_file = 'example_3_cajita_6_6'
    g_code_file = f"examples/{new_file}.gcode"
    laser_machine = 'sculpfun_s9_proofs'
    run(g_code_file, laser_machine)
