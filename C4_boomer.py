import tm1637, ssd1306, time, socket, network, json
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

def rcStart(AP, beeper, ip = '127.0.0.1', port = 24680, ):
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
		rd_info = rd_info.split('/')[1] # 将第一行分割并提取内容
		rd_info = rd_info[0:-5]
		del recv_data # 节省内存

		# 最后提取完毕的数据理应是一个 字符串形式的整数 作为倒计时的分钟数
		try:
			# 测试是否为一个可转型的整数
			minute = int(rd_info)
		except:
			# 若不可转型则不符合标准 pass后回到循环顶部等待接收下一个http头
			for _ in range(2):
				beeper.beep(0.1)
				time.sleep(0.1)
			continue
		else:
			# 可转型则判断是否在有效范围内
			if minute > 99 or minute < 1:
				for _ in range(3):
					beeper.beep(0.1)
					time.sleep(0.1)
				continue
			else:
				# 符合条件 关闭套接字和AP并返回int形式的整数
				rc_socket.close()
				AP.active(False)
				for _ in range(3):
					beeper.beep(0.3)
					time.sleep(0.2)
				return minute

def setUpAP(name = 'Micropython-AP', password = '', max_c = 1):
	ap = network.WLAN(network.AP_IF)
	if password =='':
		ap.config(essid = name, authmode=network.AUTH_OPEN)
	else:
		ap.config(essid = name, authmode = network.AUTH_WPA_WPA2_PSK, password = password, max_clients = max_c)
	ap.active(True)
	return ap

def selfCheck(beeper, oled_screen, num_screen):
	num_screen.write([127, 255, 127, 127]) # 数码管显示88:88
	oled_screen.fill(1) # 点亮OLED屏全部像素点
	oled_screen.show()

	for _ in range(3):
		beeper.beep(0.2)
		time.sleep(0.2)
	time.sleep(0.8)

	num_screen.write([0, 0, 0, 0]) # 清空数码管 OLED显示字符
	oled_screen.fill(0)
	oled_screen.text('Ready...', 32, 0)
	oled_screen.show()
	time.sleep(1)
	oled_screen.text('WAITING', 32, 9)
	oled_screen.show()
	beeper.beep(0.5)

def showImage(oled_screen, image_name):
	# OLED上显示点阵
	lattice_list = open('image_lattice.json', 'r')
	lattice = json.load(lattice_list) #读取相同位置下的json文件
	lattice_list.close() # 文件内容为类似 [[x, y], [x, y]] 的二位坐标阵列 

	oled_screen.fill(0) # 清空屏幕防止重叠显示
	for p in lattice[image_name]:
		oled_screen.pixel(p[0], p[1], 1) # 遍历二维坐标列表 逐个显示 
	oled_screen.show() # 最终在OLED上点亮

	del lattice

def countDown(minute, num_screen, beeper):
	# 参数minute为一个int形式的整数 代表倒计时分钟数
	num_screen.numbers(minute, 0)
	time.sleep(1)
	# 循环刷新数码管 显示倒计时时间
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

	for _ in range(5):
		num_screen.show('boon')
		beeper.beep(0.2)
		num_screen.write([0, 0, 0, 0])
		time.sleep(0.2)

def timeIsUp(num_screen):
	time.sleep(1)
	for _ in range(4):
		num_screen.show('You')
		time.sleep(0.5)
		num_screen.show('Are')
		time.sleep(0.5)
		num_screen.show('Fool')
		time.sleep(0.5)

def powerOff(oled_screen, num_screen, beeper):
	oled_screen.poweroff()
	num_screen.write([0, 0, 0, 0])
	beeper.stopBeep()

# 主函数
def main():
	# 为各设备分配GPIO并创建对象
	timer_screen = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
	beeper = Buzzer(pin_port = Pin(2, Pin.OUT))
	oled_screen = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(3), sda=Pin(4)))
	oled_screen.contrast(255) # oled亮度设为最大 255

	selfCheck(beeper, oled_screen, timer_screen) # 进行自检
	ap_obj = setUpAP(name = 'C4_Bomb', password = '10029930abc') # 打开热点
	minute = rcStart(ap_obj, beeper) # 打开套接字 等待接收http头并开始 等待期间主线程阻塞
	showImage(oled_screen, 'countdown') # 收到http后OLED显示点阵图片
	countDown(minute, timer_screen, beeper) # 数码管开始计时
	showImage(oled_screen, 'timeisup') # 显示结束后的点阵图
	timeIsUp(timer_screen)
	powerOff(oled_screen, timer_screen, beeper)