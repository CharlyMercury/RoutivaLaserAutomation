"""
To START the machine to cut a product, we initialize with the following commands:
    - Laser secure turn off
    - We send the following commands:
        G00 - Rapid Positioning:
            G00 is used for rapid tool movements to a specific position. This command is employed to move the tool
            quickly without cutting or engraving.
        G17 - Plane Selection:
            G17 selects the XY plane. In the context of GRBL, it specifies that movements and coordinates will occur
            in the XY plane.
        G40 - Cutter Compensation Cancel:
            G40 cancels tool compensation. This command is used to deactivate tool radius compensation, meaning the
            tool will cut at the exact position specified in the G-code program without considering the tool's radius.
        G21 - Millimeters as Units:
            G21 sets units of measurement to millimeters. This command indicates that coordinates and displacements
            in the G-code program will be in millimeters.
        G54 - Work Coordinate System:
            G54 selects the work coordinate system. In GRBL and other CNC implementations, G54 is commonly used to
            set the default work coordinate system. There may be multiple work coordinate systems (G54, G55, G56, etc.)
             to facilitate switching between different clamping configurations or part locations on the machine.
    - Switch to absolute coordinates.
    - Turn on the air assist.
"""


def init_commands():
    """
    G-code commands to initialize laser machine.

    :return: list with commands
    """
    command_1 = b"M5"
    command_2 = b"G00 G17 G40 G21 G54"
    command_3 = b"G90"
    command_4 = b"M8"
    command_list = [command_1, command_2, command_3, command_4]

    return command_list
