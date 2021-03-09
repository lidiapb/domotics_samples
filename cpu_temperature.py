import time
import paho.mqtt.client as mqtt
from gpiozero import CPUTemperature
broker_address="192.168.0.10"

client = mqtt.Client()
client.connect(broker_address)
while (True):
	cpu = CPUTemperature()
	print (cpu.temperature)
	client.publish("cpu/temperature",cpu.temperature)
	time.sleep(3)

