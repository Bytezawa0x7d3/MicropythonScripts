from machine import Pin, PWM
import time

times = input('TIMES>>>')
beeper_pin = Pin(0, Pin.OUT)
pwm = PWM(beeper_pin)

for i in range(int(times)):
	pwm.freq(1000)
	pwm.duty(512)
	time.sleep(1)
	pwm.freq(0)
	pwm.duty(0)
	time.sleep(1)

pwm.deinit()