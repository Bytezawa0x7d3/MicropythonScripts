# 使用第三方库'tm1637'驱动数码管显示倒计时
import tm1637
from machine import Pin
import time

# 构建tm1637驱动类 为蜂鸣器创建Pin
tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
beeper = Pin(0, Pin.OUT)

tm.write([127, 255, 127, 127])
beeper.off()
time.sleep(1)
tm.write([0, 0, 0, 0])
beeper.on()
time.sleep(1)

tm.numbers(3, 0)
time.sleep(1)
for m in range(2, -1, -1):
	for s in range(59, -1, -1):
		rest_time = 1.0
		tm.numbers(m, s)
		if m == 0:
			if s <= 5:
				for i in range(4):
					beeper.off()
					time.sleep(0.1)
					beeper.on()
					time.sleep(0.15)
				rest_time -= 1.0
			elif s <= 10:
				for _ in range(2):
					beeper.off()
					time.sleep(0.1)
					beeper.on()
					time.sleep(0.4)
				rest_time -= 1.0
			else:
				beeper.off()
				time.sleep(0.1)
				beeper.on()
				rest_time -= 0.1
		else:
			if s % 2 == 0:
				beeper.off()
				time.sleep(0.1)
				beeper.on()
				rest_time -= 0.1
		time.sleep(rest_time)

tm.write([0, 0, 0, 0])
beeper.off()
for _ in range(3):
	tm.write([0b01111100, 0b00111111, 0b00111111, 0b01010100])
	time.sleep(0.5)
	tm.write([0, 0, 0, 0])
	time.sleep(0.5)
beeper.on()