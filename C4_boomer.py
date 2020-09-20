import tm1637, ssd1306, time, socket, network
from machine import Pin, I2C

class Buzzer():
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

	def stopBeep(self):
		self.pin_port.on()

def rcStart(AP, password, ip = '127.0.0.1', port = 24680):
	# 创建套接字 接受http头并分析 对比激活密码
	# start count down through remote control (http)
	rc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	rc_socket.bind((ip, port))
	rc_socket.listen(1) # 最多接入一个客户端

	while True:
		controller_socket, _ = rc_socket.accept()
		recv_data = controller_socket.recv(1024).decode() # 1024表示本次接收的最大字节数

		rd_info = recv_data.splitlines()[0] # 将全部http头内容按行分割为列表 保留第一行
		del recv_data # 节省内存

		if password in rd_info: # 对比收到的内容是否符合password 符合则跳出循环并关闭套接字与AP
			rc_socket.close()
			AP.active(False)
			break

def setUpAP(name = 'Micropython-AP', password = '', max_c = 1):
	ap = network.WLAN(network.AP_IF)
	if password =='':
		ap.config(essid = name, authmode=network.AUTH_OPEN)
	else:
		ap.config(essid = name, authmode = network.AUTH_WPA_WPA2_PSK, password = password, max_clients = max_c)
	ap.active(True)
	return ap

# 为各设备分配GPIO并创建对象
timer_screen = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
beeper = Buzzer(pin_port = Pin(2, Pin.OUT))
oled_screen = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(3), sda=Pin(4)))

def selfCheck(beeper, oled_screen, num_screen):
	num_screen.write([127, 255, 127, 127]) # 数码管显示88:88
	oled_screen.fill(1) # 点亮OLED屏全部像素点
	oled_screen.show()

	for _ in range(3):
		beeper.beep(0.2)
		time.sleep(0.2)
	time.sleep(0.8)

	num_screen.write([0, 0, 0, 0]) # 清空数码管 OLED显示'Ready...'
	oled_screen.fill(0)
	oled_screen.text('Ready...', 32, 0)
	oled_screen.show()
	time.sleep(1)
	oled_screen.text('WAITING', 32, 9)
	oled_screen.show()
	beeper.beep(0.5)