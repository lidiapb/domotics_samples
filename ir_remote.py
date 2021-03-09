import time
from ircodec.command import CommandSet
controller = CommandSet(emitter_gpio=4, receiver_gpio=14, name='LED controller')

controller.add('ON')
controller.add('OFF')
controller.add('RED')
controller.add('GREEN')
controller.add('BLUE')
controller.add('WHITE')

controller.save_as('LED_REMOTE.json')
print(controller)
time.sleep(3)
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

