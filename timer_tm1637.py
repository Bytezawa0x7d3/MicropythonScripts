# 使用第三方库'tm1637'驱动数码管显示倒计时
import tm1637
from machine import Pin
import time
tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))

tm.write([127, 255, 127, 127])
time.sleep(1)
tm.write([0, 0, 0, 0])
time.sleep(1)

tm.numbers(5, 0)
time.sleep(1)
for m in range(4, -1, -1):
	for s in range(59, -1, -1):
		tm.numbers(m, s)
		time.sleep(1)

tm.write([0, 0, 0, 0])
time.sleep(1)
for _ in range(5):
	tm.write([0b01111100, 0b00111111, 0b00111111, 0b01010100])
	time.sleep(0.5)
	tm.write([0, 0, 0, 0])
	time.sleep(0.5)
