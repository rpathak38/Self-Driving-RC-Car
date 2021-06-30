import serial
import time
import threading


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


arduino = serial.Serial("/dev/cu.usbmodem11101")
print(arduino.name)

t1 = threading.Thread(target=serial_input, args=[arduino])
t2 = threading.Thread(target=serial_output, args=[arduino])

t1.start()
t2.start()
