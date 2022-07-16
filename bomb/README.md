# FoolsTimeBomb_micropython

## Micropython based C4 time bomb modle (Under construction)

> A time bomb model with an OLED and 4-number screen and a beeper, which can only be used for a prank (can't explode...)

## Instructions

### Wiring

* TM1637
	* CLK - GPIO16
	* DIO - GPIO5<br>

* Beeper
	* I/O - GPIO4

* SSD1306(I2C)
	* SCL - GPIO0
	* SDA - GPIO2

### Files

* **mian.py**
This script is the main body of the project, upload it to the board and run it according to the startup instructions.

* **create_pixels_list.py**
This script is used to convert the PPM image to pixel coordinates and write the coordinates to a TXT file. The coordinates of each image will occupy a TXT file. In the txt file, each line has the coordinates of ten pixels, which are separated by spaces. 
> Please refer to the notes of this script for details

* **txt files**
They are used to store the pixel coordinates that came from PPM images. Be created by *create_pixels_list.py*, be read by *main.py*. The meaning of its existence is to allow the OLED screen to display ppm images, because ppm images are unreadable for OLED screen but txt files are able to be read by it.

### Startup

1. Connect the equipments according to the wiring instructions, and you can solve the power supply mode by yourself.

2. When the board is powered on, the four digit display and OLED screen will all light up, and the buzzer will sound three times. After that, screens will all go out and the OLED screen will display *Ready...* and *WAITING*, and the buzzer will sound once. The oled screen will also show the IP and Port. It means you can proceed to the next step.

3. After that, the board will set up an access point with name 'C4_Bomb' and password '100299301bc'.Connect the access point with phone or PC, the board only accept one device.
> The name and password here are the default content, but you can change it to what you expect in the source code. Find more details in main.py

4. *http://192.168.4.1:24680/5*
*192,168.4.1* is IP and *24680* is port number, you can see it on OLED screen. Open this URL with a browser after connect to the access point. Then the board will start a 5-minute count down.
> You can change the port via source code, the countdown time is also can be changed by type a different number in the end of the URL. **(only accept integers between 1-99)**<br>The IP address may be dynamic and its value is displayed on the OLED screen after each boot. Here is an example, **you should modify the IP address in the link according to what is displayed**.

5. Wait and guess what will happen in the end of count down.