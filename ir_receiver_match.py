#---------------------------------------------------------------------#
#Name - IR&NECDataCollect.py
#Description - Reads data from the IR sensor but uses the official NEC Protocol (command line version)
#Author - Lime Parallelogram
#Licence - Attribution Lime
#Date - 06/07/19 - 18/08/19
#---------------------------------------------------------------------#
#Imports modules
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

buttons_dict = {
	"0x300f7c03f": "ON",
	"0x300f740bf": "OFF",
	"0x300f720df": "RED",
	"0x300f7a05f": "GREEN",
	"0x300f7609f": "BLUE",
	"0x300f7e01f": "WHITE"
}
	
#==================#
#Promps for values
#Input pin
while True:
	PinIn = input("Please enter your sensor pin: ")
	try:
		PinIn = int(PinIn)
		break
	except:
		pass

#==================#
#Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PinIn,GPIO.IN)

#==================#
#Defines Subs	
def ConvertHex(BinVal): #Converts binary data to hexidecimal
	tmpB2 = int(str(BinVal), 2)
	return hex(tmpB2)
		
def getData(): #Pulls data from sensor
	num1s = 0 #Number of consecutive 1s
	command = [] #Pulses and their timings
	binary = 1 #Decoded binary command
	previousValue = 0 #The previous pin state
	value = GPIO.input(PinIn) #Current pin state
	
	while value: #Waits until pin is pulled low
		value = GPIO.input(PinIn)
	
	startTime = datetime.now() #Sets start time
	
	while True:
		
		if value != previousValue: #Waits until change in state occurs
			now = datetime.now() #Records the current time
			pulseLength = now - startTime #Calculate time in between pulses
			startTime = now #Resets the start time
			command.append((previousValue, pulseLength.microseconds)) #Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
		
		#Interrupts code if an extended high period is detected (End Of Command)	
		if value:
			num1s += 1
		else:
			num1s = 0
		
		if num1s > 10000:
			break
		
		#Reads values again
		previousValue = value
		value = GPIO.input(PinIn)
		
	#Covers data to binary
	for (typ, tme) in command:
		if typ == 1:
			if tme > 1500: #According to NEC protocol a gap of 1687.5 microseconds repesents a logical 1 so over 1000 should make a big enough distinction
				binary = binary * 10 + 1
			else:
				binary *= 10
				
	if len(str(binary)) > 34: #Sometimes the binary has two rouge charactes on the end
		binary = int(str(binary)[:34])
		
	return binary
	
def runTest(): #Actually runs the test
	#Takes samples
	command = ConvertHex(getData())
	print("Hex value: " + str(command)) #Shows results on the screen
	return command
	###

def find_button(hex_code):
	if(hex_code in buttons_dict):
		return buttons_dict[hex_code]
	else: 
		return("Unknown")

#==================#

while True:
  
  finalData = runTest()
  print(str(finalData))
  button = find_button(str(finalData))
  print("Button: " + str(button)) #Shows button on the screen
GPIO.cleanup()