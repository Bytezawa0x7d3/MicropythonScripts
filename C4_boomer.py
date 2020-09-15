import tm1637, ssd1306, time, socket, network
from machine import Pin

class Beeper():
	# 此类用于控制有源蜂鸣器 
	def __init__(self, pin_port):
		# pin_port为一个Pin对象
		# 初始值为高电平 因为低电平为触发
		self.pin_port = pin_port
		self.pin_port.on()

	def beep(self, duration):
		self.pin_port.off()
		time.sleep(duration)
		self.pin_port.on()

	def keepBeep(self):
		self.pin_port.off()

	def stopBeep():
		self.pin_port.on()

def rcStart(AP, password, ip = '127.0.0.1', port = 24680):
	# start count down through remote control (http)
	rc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	rc_socket.bind((ip, port))
	rc_socket.listen(1)

	while True:
		controller_socket, _ = rc_socket.accept()
		recv_data = controller_socket.recv(1024).decode() # 1024表示本次接收的最大字节数

		rd_info = recv_data.splitlines()[0]
		del recv_data

		if password in rd_info:
			rc_socket.close()
			AP.active(False)
			break

def setUpAP(name = 'Micropython-AP', password = '', max_c = 1):
	ap = network.WLAN(network.AP_IF)
	if pwd=='':
		ap.config(essid = eid, authmode=network.AUTH_OPEN)
	else:
		ap.config(essid = eid, authmode = network.AUTH_WPA_WPA2_PSK, password = pwd, max_clients = max_c)
	ap.active(True)