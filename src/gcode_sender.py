"""
    With this script we can send G-code commands to the laser machine.
"""
import time
import serial


class GcodeSender:

    def __init__(self, port: str, baud_rate: int = 115200, laser_machine: str = '', timeout: int = 1):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.timeout = timeout
        self.laser_machine = laser_machine

    def connection(self):
        try:
            self.serial_connection = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=self.timeout)
            return f'Serial connection established on {self.port} at {self.baud_rate} bps.'
        except serial.SerialException as e:
            print(f"Error: {e}")
            return 'Serial Connection Failed'

    def __send_g_code_command(self, command: str):
        element_to_laser = command.strip().encode() + str.encode('\n')
        self.serial_connection.write(element_to_laser)
        response = self.serial_connection.readline().decode('utf-8').strip()
        while response != 'ok':
            response = self.serial_connection.readline().decode('utf-8').strip()
            time.sleep(0.001)

    def __wake_up_machine(self):
        self.__send_g_code_command(command="\r\n\r\n")
        self.serial_connection.flushInput()

    def __send_home_machine(self):
        print(self.laser_machine)
        if self.laser_machine is not 'sculpfun_s9_proofs':
            send_home_g_code = '$H'
            self.__send_g_code_command(command=send_home_g_code)

    def send_g_code(self, gcode_path: str):
        g_code_data = open(gcode_path, 'r')
        print('Wake up machine')
        self.__wake_up_machine()
        print('Sending Laser Machine to Home')
        self.__send_home_machine()

        print('Sending GCode')
        for g_code_command in g_code_data:
            if ';' in g_code_command:
                print(g_code_command)
            else:
                self.__send_g_code_command(command=g_code_command)
        return 'Finished'

    def close_serial_connection(self):
        if self.serial_connection.is_open:
            self.serial_connection.close()
            return "Serial connection closed."
