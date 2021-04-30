# A sketch to test the serial communication with the Arduino.

import serial
import time
import serial.tools.list_ports
import string
#'/dev/ttyACM0'
# -- Commands --
#   z100    Moves the carriage down 100 mm
#   z-100   Moves the carriage up 100 mm
#   Home    Moves the carriage to the home position

class usbCommunication():
    # def __init__(self, port, baudRate):
    def __init__(self,serialnumber, baudRate):
        self.port = self.findArduinoPort(serialnumber)
        self.message = None
        self.ser = serial.Serial(self.port, baudRate, timeout=1)

	#Input: #z100 for z 100mm down. z-100 for 100mm up
	# Homing: send "home"
    def sendMessage(self, msg):
        self.ser.write(msg.encode('utf-8'))

	#Output: Confirms whats has been sent
	# if input NOT understood it reports that aswell
    def readMessage(self):
        self.message = self.ser.readline().decode('utf-8').rstrip("\r,\n")
        print(self.message)

    def returnMessage(self):
        self.message = self.ser.readline().decode('utf-8').rstrip("\r,\n")
        return self.message
        
    def messageRecieved(self):
        if(self.ser.in_waiting > 0):
            return True
        else:
            return False

    def findSerialNumber():
        for pInfo in serial.tools.list_ports.comports():
            print(pInfo.serial_number)
    #        if "Arduino" in pInfo.description: // Only works with UNO!
                #return pInfo.serial_number;
        print("No Arduino detected")
        return "0"

    def findArduinoPort(self,serial_number):
        for portInfo in serial.tools.list_ports.comports():
            if portInfo.serial_number == serial_number:
                return serial.Serial(portInfo.device).port
        raise IOError("Could not find an arduino - is it plugged in?")


