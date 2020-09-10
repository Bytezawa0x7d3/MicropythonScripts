# 使开发板连接至路由器

import network

def doConnect(essid, pwd):
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected():
		print('[INFO] Connecting to network...')
		wlan.connect(essid, pwd)
		while not wlan.isconnected():
			pass
	print('[INFO] Connection was successful.\n[INFO] Network config:', wlan.ifconfig())

doConnect('PeterDuanBigAsshole', '5d8b66dfabc31b')
input('[INFO] Script process finished.')