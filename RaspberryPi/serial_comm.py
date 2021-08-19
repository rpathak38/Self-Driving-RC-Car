import serial
import time
import threading
from simple_term_menu import TerminalMenu
import serial.tools.list_ports as port_list


def serial_output(ser: serial.Serial):
    while True:
        while ser.inWaiting():
            temp = ser.readline().replace('\r'.encode(), '\n'.encode())
            print(temp.decode("utf-8")[:-2])


def serial_input(ser: serial.Serial):
    complete = False
    serial_command = None
    while True:
        serial_command = input() + '\n'
        ser.write(serial_command.encode())


def serial_input_ping(ser: serial.Serial, serial_command: str):
    serial_command = serial_command + "\n"
    ser.write(serial_command.encode())


print("Please select the correct Arduino device from the listed ports")
ports = list(port_list.comports())
ports_display = [str(p.name) + " / " + str(p.manufacturer) for p in ports]
terminal_menu = TerminalMenu(ports_display)
menu_entry_index = terminal_menu.show()
device = str(ports[menu_entry_index].device)

arduino = serial.Serial(device)
print(arduino.name)

print("Please select the mode in which you would like to operate")
modes = ["Serial Communication", "Computer Vision"]
terminal_menu = TerminalMenu(modes)
mode_index = terminal_menu.show()

# pure serial communication case
if mode_index == 0:
    t1 = threading.Thread(target=serial_input, args=[arduino])
    t2 = threading.Thread(target=serial_output, args=[arduino])
    t1.start()
    t2.start()

else:
    t1 = threading.Thread(target=serial_output, args=[arduino])
    t1.start()
