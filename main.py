"""
    With this script we can send G-code commands to the laser machine.
"""
import time
import serial
from src.g_code_draw import draw_g_code

# Serial port and baud rate
serial_port = "COM3"
baud_rate = 115200

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)


def send_g_code_command(command_: str, commands_delay_: int):
    element_to_laser = command_.strip().encode() + str.encode('\n')
    ser.write(element_to_laser)
    response = ser.readline().decode('utf-8').strip()
    time.sleep(commands_delay_)

    while response != "ok" and response != "" and command_ != '$H':
        ser.write(element_to_laser)
        raw_response = ser.readline()
        response = raw_response.decode('utf-8').strip()
        time.sleep(commands_delay_)


def send_g_code(list_g_code):
    # Time delay
    commands_delay = 0

    for element in list_g_code:

        if 'Cut @' in element:
            speed = float(element.split('Cut @')[1].replace('mm/min, 100% power', ''))
            if speed <= 1000:
                commands_delay = 0.2
            if speed > 1000:
                commands_delay = 0.025

        # Send data
        if ';' in element:
            print(element)
        else:
            send_g_code_command(command_=element, commands_delay_=commands_delay)


def run(g_code_file_):
    g_code_draw = draw_g_code(file_g_code_name=g_code_file_)

    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)
    ser.flushInput()

    print('Sending Home')
    extra_element = '$H'
    send_g_code_command(command_=extra_element, commands_delay_=0)

    time.sleep(2)

    try:

        print('Sending GCode')
        send_g_code(g_code_draw)

    finally:
        # Close the serial connection
        ser.close()


if __name__ == "__main__":
    new_file = 'example_3_cajita_6_6'
    svg_file = f"examples/{new_file}.svg"
    g_code_file = f"examples/{new_file}.gcode"
    run(g_code_file)
