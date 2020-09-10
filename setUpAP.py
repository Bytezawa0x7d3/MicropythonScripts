# 将开发板设为一个路由器
import network

def setUpAP(eid = 'Micropython-AP', pwd = '', max_c = 1):
	print('[INFO] Setting up the access-point......')
	ap = network.WLAN(network.AP_IF)
	if pwd=='':
		ap.config(essid = eid, authmode=network.AUTH_OPEN)
	else:
		ap.config(essid = eid, authmode = network.AUTH_WPA_WPA2_PSK, \
			password = pwd, max_clients = max_c)
	ap.active(True)
	print('[INFO] access-point set up successfully.')

setUpAP(eid = 'PeterDuanBigAsshole', pwd = '5d8b66dfabc31b')
input('[INFO] Script process finished.')