# Parameters to know what device is connecting serial for
# Tested on Raspberry 4 model B

# Sculpfun S9 Board (This is the first board that we buy)
# idProduct = "7523"
# idVendor = "1a86"}
# usb_name = sculpfun_s9_proofs_board
# Adding this product to usb rules
# sudo nano /etc/udev/rules.d/10-usb-serial.rules
# SUBSYSTEM=="usb", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", SYMLINK+="sculpfun_s9_proofs_board"
# sudo udevadm trigger


# Sculpfun S30 Board (This is the s30 board - work area 90*90 cm)
# idProduct = ""
# idVendor = ""
# usb_name = sculpfun_laser_90_90
# Adding this product to usb rules
# sudo nano /etc/udev/rules.d/10-usb-serial.rules
# SUBSYSTEM=="usb", ATTRS{idProduct}=="", ATTRS{idVendor}=="", SYMLINK+="sculpfun_laser_90_90"
# sudo udevadm trigger


# Sculpfun S30 Board (This is the s30 board for rotatory machine - work area 40*40 cm)
# idProduct = ""
# idVendor = ""}
# usb_name = sculpfun_laser_40_40_rotatory
# Adding this product to usb rules
# sudo nano /etc/udev/rules.d/10-usb-serial.rules
# SUBSYSTEM=="usb", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", SYMLINK+="sculpfun_laser_40_40_rotatory"
# sudo udevadm trigger


def identifying_laser_board(board_to_use: str):

    if board_to_use == 'sculpfun_s9_proofs':
        port_name = "sculpfun_s9_proofs_board"
        baud_rate = 115200
    elif board_to_use == 'sculpfun_s30_90_90':
        port_name = "sculpfun_laser_90_90"
        baud_rate = 115200
    elif board_to_use == 'sculpfun_s30_40_40_rotatory':
        port_name = "sculpfun_laser_40_40_rotatory"
        baud_rate = 115200
    else:
        port_name = 'invalid board'
        baud_rate = 'invalid board'

    laser_machine_parameters = {
        'port': port_name,
        'baud_rate': baud_rate
    }

    return laser_machine_parameters
