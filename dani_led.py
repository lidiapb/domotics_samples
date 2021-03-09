import time
from ircodec.command import CommandSet
controller = CommandSet.load('LED_REMOTE.json')

while True:
	controller.emit('ON')
	time.sleep(1)
	controller.emit('RED')
	time.sleep(1)
	controller.emit('GREEN')
	time.sleep(1)
	controller.emit('BLUE')
	time.sleep(1)
	controller.emit('WHITE')
	time.sleep(1)
	controller.emit('OFF')
	time.sleep(1) 
