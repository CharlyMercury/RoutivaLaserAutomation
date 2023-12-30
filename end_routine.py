"""
To FINISH a job, the following steps are performed:

    - Turn off the air assist.
    - Decrease the laser power to 0%.
    - Turn off the laser.
    - Switch to absolute coordinates.
    - Move to the origin.
    - Stop the program and turn off the machine.

"""


def end_commands():
    """
    G-code commands to finalize laser machine.

    :return: list with commands
    """

    command_1 = b"M9"
    command_2 = b"G1 S0"
    command_3 = b"M5"
    command_4 = b"G90"
    command_5 = b"G0 F9000 X0 Y0"
    command_6 = b"M2"
    command_list = [command_1, command_2, command_3, command_4, command_5, command_6]

    return command_list
