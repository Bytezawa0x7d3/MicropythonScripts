from machine import Pin
import time

beeper = Pin(1, Pin.OUT)
times = input('TIMES>>>')
	
for i in range(int(times)):
	beeper.value(0)
	time.sleep(0.1)
	beeper.value(1)
	time.sleep(0.9)
