# Parameters to know what device is connecting serial for
# Tested on Raspberry 4 model B


# To know idProduct and idVendor type:
# $ usb-devices
# Sculpfun S30 Board (This is the s30 board - work area 90*90 cm)
# idProduct = "7523"
# idVendor = "1a86"
# usb_name = sculpfun_laser_90_90
# Adding this product to usb rules
# sudo nano /etc/udev/rules.d/10-usb-serial.rules
# KERNELS=="1-1.1:1.0", SYMLINK+="sculpfun_90_90"
# sudo udevadm trigger


# Sculpfun S30 Board (This is the s30 board for rotatory machine - work area 40*40 cm)
# idProduct = ""
# idVendor = ""}
# usb_name = sculpfun_laser_40_40_rotatory
# Adding this product to usb rules
# sudo nano /etc/udev/rules.d/10-usb-serial.rules
# KERNELS=="1-1.2:1.0", SYMLINK+="sculpfun_rotatory"
# sudo udevadm trigger


# Sculpfun S9 Board (This is the first board that we buy)
# idProduct = "7523"
# idVendor = "1a86"
# usb_name = sculpfun_s9_proofs_board
# Adding this product to usb rules
# sudo nano /etc/udev/rules.d/10-usb-serial.rules
# (SUBSYSTEM=="tty", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", KERNEL=="ttyUSB2",
# ATTR{port_number}=="2", SYMLINK+="sculpfun_s9_proofs") (old)
# KERNELS=="1-1.3:1.0", SYMLINK+="sculpfun_s9_proofs"
# sudo udevadm trigger


def identifying_laser_board(board_to_use: str):

    if board_to_use == 'sculpfun_s9_proofs':
        port_name = "/dev/sculpfun_s9_proofs"
        baud_rate = 115200
    elif board_to_use == 'sculpfun_s30_90_90':
        port_name = "/dev/sculpfun_90_90"
        baud_rate = 115200
    elif board_to_use == 'sculpfun_s30_40_40_rotatory':
        port_name = "/dev/sculpfun_rotatory"
        baud_rate = 115200
    else:
        port_name = 'invalid board'
        baud_rate = 'invalid board'

    laser_machine_parameters = {
        'port': port_name,
        'baud_rate': baud_rate
    }

    return laser_machine_parameters
