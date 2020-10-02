import ssd1306
from machine import Pin, I2C

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


oled_screen = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(0), sda=Pin(2)))
oled_screen.contrast(255) # set the brightness as the highest value
while True:
	input('>>>')
	showImage(oled_screen, 'countdown.txt')
	input('<<<')
	showImage(oled_screen, 'timeisup.txt')