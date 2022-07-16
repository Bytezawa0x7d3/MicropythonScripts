import numpy as np
from PIL import Image
import json

# convert ppm image to pixels lists and write each picture's list to each json files
def createPixelsList(name_obj = {}):
	# name_obj is a dictionary, keys are lists' name and values are Image object
	xs_dic = {} 
	for name, obj in name_obj.items():
		xs_dic[name] = []
		mat= np.array(obj)
		line = 0
		px = 0
		for linee in mat:
			for pxx in linee:
				if pxx < 180:
					xs_dic[name].append([px,line])
				px += 1
			line += 1
			px = 0

	# xs_dic is a dictionaty as the final result, keys are names (string) and values are list contains lists
	for name, lst in xs_dic.items():
		'''
		# create json files, dump pixels lists to each file.
		js_file_obj = open(name + '.json', 'w')
		json.dump(lst, js_file_obj)
		js_file_obj.close()
		'''
		# create a txt and write pixels' position into it, each line contains up to ten pixels.
		file = open(name + '.txt', 'w')
		pix_str = ""
		for i in range(len(lst)):
			pix_str += str(lst[i][0]) + ',' + str(lst[i][1])
			if str(i)[-1] == '9':
				pix_str += '\n'
			else:
				pix_str += ' '
		file.write(pix_str)
		file.close()
	
	return None

# open two ppm pictures via Image's open function in PIL module
countdown = Image.open(r'countdown.ppm')
timeisup = Image.open(r'timeisup.ppm')
# Run the function.
createPixelsList({'countdown':countdown, 'timeisup':timeisup})
input('Finished.')