import os
import serial
import serial.tools.list_ports
import binascii
import time
from datetime import datetime
from constants import *

class Engine:
    def __init__(self):
        self.serial_port = None

    def ports_dict(self) -> dict:
        ports_in_system = {}
        ports = serial.tools.list_ports.comports()
        for port, descriptor, hwid in sorted(ports):
            ports_in_system[port] = descriptor
        return ports_in_system

    def write_logs(self, mode, text):
        if not os.path.exists("logs/"):
            os.makedirs("logs/")
        file = f"logs/err.txt"
        with open(file, mode) as fil_er:
            fil_er.write(f"\n{datetime.now()} {text}")

    def find_in_descriptor(self, value):  # "USB Serial Port"/ "ch a"
        ports_in_system = self.ports_dict()

        if not ports_in_system:  # no ports in system
            text = "No available ports in system"
            self.write_logs("a+", text)

        else:
            power_desc = value
            for port, descriptor in ports_in_system.items():
                if power_desc.lower() in descriptor.lower():
                    return port  # , descriptor

    def power_on_0ff(self, command):
        port = self.find_in_descriptor("USB Serial Port")
        try:
            self.serial_port = serial.Serial(port, 9600, timeout=0.4, inter_byte_timeout=0.3)
            for i in range(10):
                request = self.serial_port.read_until(expected="\n", size=20)
                if binascii.hexlify(request[4:5]) == b"10" and binascii.hexlify(request[-6:-5]) == b"00":
                    self.serial_port.write(command)
                    break
                elif binascii.hexlify(request[4:5]) == b"10" and binascii.hexlify(request[-6:-5]) == b"01":
                    break
            else:
                text = "cant found UPS status after 10 try's"
                self.write_logs("a+", text)

            time.sleep(3)
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            if self.serial_port.is_open:
                self.serial_port.close()

        except Exception as e:
            text = f"Error opening port '{e}'." \
                   f"Power control port with 'USB Serial Port' was not found in the descriptor."
            self.write_logs("a+", text)

        if not self.serial_port:
            text = "power port 'USB Serial Port' not found"
            self.write_logs("a+", text)

    def validator_init(self):
        port = self.find_in_descriptor("ch a")
        try:
            # stopbits=serial.STOPBITS_ONE, dsrdtr=True, inter_byte_timeout=0.05
            self.serial_port = serial.Serial(port, 115200, timeout=0.1)
            time.sleep(2)
            # Инициализация
            self.send_to_port(CMD1)
            self.send_to_port(CMD2)
            self.send_to_port(CMD3)
            self.send_to_port(CMD4)
            self.send_to_port(CMD5)
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            # self.serial_port.close()
        except ValueError:
            self.serial_port.close()

        except Exception as e:
            text = f"error open port '{e}'"
            self.write_logs("a+", text)

        if not self.serial_port:
            text = "The validator control port with 'Ch A' was not found in the descriptor."
            self.write_logs("a+", text)

        return self.serial_port

    def send_to_port(self, data):
        time.sleep(0.1)
        self.serial_port.write(data)



