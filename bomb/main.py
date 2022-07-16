import tm1637, ssd1306, time, socket, network, json
from machine import Pin, I2C

# used to control a beeper
class Buzzer():
	def __init__(self, pin_port):
		# pin_port is a Pin objet for the beeper's IO port. 
		# turn on the pin as default value to make sure it is silent
		self.pin_port = pin_port
		self.pin_port.on()

	def beep(self, duration):
		# beep for a period of time
		# duration is the number of seconds that lasts
		self.pin_port.off()
		time.sleep(duration)
		self.pin_port.on()

	def keepBeep(self):
		# beep whitout stop
		self.pin_port.off()

	def stopBeep(self):
		# stop beep and keep silent
		self.pin_port.on()

# be ready for get http and start count down
def rcStart(AP, beeper, oled_screen, port = 24680):
	# AP is a micropython network.WLAN() object, This parameter is required for shut down the AP

	# creat a TCP socket
	rc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	rc_socket.bind(('0.0.0.0', port))
	rc_socket.listen(1) # only listen 1 client to aviod others control this.

	# show the ip and port of board's access point
	oled_screen.text(AP.ifconfig()[0], 8, 18)
	oled_screen.text(str(port), 34, 27)
	oled_screen.show()

	while True:
		controller_socket, _ = rc_socket.accept()
		recv_data = controller_socket.recv(1024).decode()

		# Split and eliminate all the useless in HTTP content, leaving only what is needed
		# http://192.168.4.1:24680/5   ->   "5" (5 is able to change to another numbers)
		# "5" is the number of minutes to count down
		# 192.168.4.1 is an example of IP, please change it to what oled shows
		# 24680 is the default value of port, doesn't neet to change.
		rd_info = recv_data[5:].split(' ')[0]
		del recv_data

		# Determine whether it is a value that can be received and used as minute to count down
		try:
			# only an integer in string form can be int()
			minute = int(rd_info)
		except:
			# show error by beep, and wait for another http request
			for _ in range(2):
				beeper.beep(0.1)
				time.sleep(0.1)
			continue
		else:
			# only accept an integer betwee 1 and 99
			if minute > 99 or minute < 1:
				for _ in range(3):
					beeper.beep(0.1)
					time.sleep(0.1)
				continue
			else:
				# close the socket and AP to aviod connections without permission
				rc_socket.close()
				AP.active(False)
				for _ in range(3):
					beeper.beep(0.3)
					time.sleep(0.2)
				return minute

# create an AP , start and return it
def setUpAP(name = 'Micropython-AP', psd = ''):
	ap = network.WLAN(network.AP_IF)
	ap.active(True)
	if psd =='':
		ap.config(essid = name, authmode = network.AUTH_OPEN)
	else:
		ap.config(essid = name, authmode = network.AUTH_WPA_WPA2_PSK, password = psd)

	return ap

# A process of self-check
def selfCheck(beeper, oled_screen, num_screen):
	num_screen.write([127, 255, 127, 127]) # 4-digits screen shows 88:88
	oled_screen.fill(1) # light up all pixels on OLED
	oled_screen.show()

	for _ in range(3):
		beeper.beep(0.2)
		time.sleep(0.2)
	time.sleep(0.8)

	# show ready and waiting on screen
	num_screen.write([0, 0, 0, 0])
	oled_screen.fill(0)
	oled_screen.text('Ready...', 32, 0)
	oled_screen.show()
	time.sleep(1)
	oled_screen.text('WAITING', 32, 9)
	oled_screen.show()
	beeper.beep(0.5)

# read the txt file and show image
def showImage(oled_screen, file_path):
	# file_path is the path of a txt file that contains the coordinate of pixels
	file = open(file_path, 'r')
	oled_screen.fill(0) # shutdown all pixels at first to aviod the stack with previous image

	reading = True
	while reading:
		line = file.readline()[:-1] # only read one line in each cycle and remove '\n' in the end
		if line == '': # stop read when finish
			reading = False
			del line
		else:
			pix_lst = line.split(' ') # x,y x,y x,y >>> ['x,y', 'x,y', 'x,y']
			del line
			for p in pix_lst:
				p = p.split(',') # x,y >>> [x, y]
				oled_screen.pixel(int(p[0]), int(p[1]), 1) # change the pixel's state to ON
			del pix_lst
			del p # delete useless variables to save memory

	oled_screen.show() # show all ON pixels on OLED

# show the time of count down by refresh the 4-digit screen each second
def countDown(minute, num_screen, beeper):
	# minute is an integer
	num_screen.numbers(minute, 0)
	time.sleep(1)
	# refresh and show rest time and beep
	for m in range(minute - 1, -1, -1):
		for s in range(59, -1, -1):
			rest_time = 1.0
			num_screen.numbers(m, s)
			if m == 0:
				if s <= 5:
					for _ in range(4):
						beeper.beep(0.1)
						time.sleep(0.15)
					rest_time -= 1.0
				elif s <= 10:
					for _ in range(2):
						beeper.beep(0.1)
						time.sleep(0.4)
					rest_time -= 1.0
				else:
					beeper.beep(0.1)
					rest_time -= 0.1
			else:
				if s % 2 == 0:
					beeper.beep(0.1)
					rest_time -= 0.1
			time.sleep(rest_time)

	# blink and show text on it
	for _ in range(5):
		num_screen.show('boon')
		beeper.beep(0.4)
		num_screen.write([0, 0, 0, 0])
		time.sleep(0.4)

# Behavior after timing
def timeIsUp(num_screen):
	time.sleep(1)
	for _ in range(5):
		num_screen.show('You')
		time.sleep(0.8)
		num_screen.show('Are')
		time.sleep(0.8)
		num_screen.show('Fool')
		time.sleep(0.8)

# turn off all devices
def powerOff(oled_screen, num_screen, beeper):
	oled_screen.poweroff()
	num_screen.write([0, 0, 0, 0])
	beeper.stopBeep()

def main():
	# distribution pins and create objects for devices
	timer_screen = tm1637.TM1637(clk=Pin(16), dio=Pin(5))
	beeper = Buzzer(pin_port = Pin(4, Pin.OUT))
	oled_screen = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(0), sda=Pin(2)))
	oled_screen.contrast(255) # set the brightness as the highest value

	# do self-check
	selfCheck(beeper, oled_screen, timer_screen)
	# turn up ap
	ap_obj = setUpAP(name = 'C4_Bomb', psd = '10029930abc')
	# wait for http request from user and block process unitl get a acceptable http request
	minute = rcStart(ap_obj, beeper, oled_screen)
	# show the image during countdown
	showImage(oled_screen, 'countdown.txt')
	# start countdown
	countDown(minute, timer_screen, beeper)
	# show the image in the end of the process
	showImage(oled_screen, 'timeisup.txt')
	# finish the process
	timeIsUp(timer_screen)
	powerOff(oled_screen, timer_screen, beeper) # close all, reboot the board to play again.

if __name__ == "__main__":
	main()