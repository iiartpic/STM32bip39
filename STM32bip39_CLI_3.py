resurse = [
"https://www.yakaboo.ua/ua/svjatkovi-deserti.html",
"https://www.yakaboo.ua/ua/najkraschi-stravi-na-schoden-i-na-svjata.html",
"https://www.yakaboo.ua/ua/solodka-nedilja.html",
"https://www.yakaboo.ua/ua/picca-zapekanki-pirogi.html",
"https://www.yakaboo.ua/ua/domashnij-hlib.html",
"https://www.yakaboo.ua/ua/deserty-bez-vypechki.html",
"https://www.yakaboo.ua/ua/pirogi-pirozhki-bulochki-gotovim-iz-slojonogo-testa.html"
]

col = [[0],[1],[2],[3],[4],[5],[6],]
#==============================================================================
#python -m serial.tools.list_ports | python -m serial.tools.miniterm <port_name>

import re
import pandas as pd
import numpy as np
import time
import os
import serial
import serial.tools.list_ports as port_list
import subprocess

pd.set_option('display.max_colwidth', None)

position = ['___N___']

num = np.array(col)

df = pd.DataFrame(num, index=resurse, columns=position)
print(df)
#print(resurse)

ports = list(port_list.comports())
print(ports[0].device)
port = ports[0].device
baudrate = '115200'
ser = serial.Serial(port=port, baudrate=baudrate,
								bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)

def showentropy(cid):
    return os.system("echo {} | ent".format(cid))


def cid(file):
	# #cid0 = subprocess.run(["npx", "ipfs-only-hash", "--cid-version", "0", "catt.png"], text=True)
	# #cid1 = subprocess.run(["npx", "ipfs-only-hash", "--cid-version", "1", "catt.png"], text=True)
	# sp = subprocess.Popen(["npx", "ipfs-only-hash", "--cid-version", "0", "{}".format(file)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	# cid0, errors0 = sp.communicate()
	# sp.wait()

	# cid0 = cid0.rstrip()
	# print(cid0)
	# #print(errors0)

	sp = subprocess.Popen(["npx", "ipfs-only-hash", "--cid-version", "1", "{}".format(file)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
	cid1, errors0 = sp.communicate()
	sp.wait()

	cid1 = cid1.rstrip()
	#print(cid1)
	#print(errors0)
	return cid1


def responce_serial():
	ser.flushInput()
	time.sleep(0.1)	
	while True:
		if ser.inWaiting() > 0:
			#time.sleep(0.1)
			response = ser.readline()
			decoded = response.decode("utf-8")
			print(decoded)
			if "m/44'/0'/0'/0/" in decoded:
				pass
			#	print(decoded)
			elif "------------- END -------------" in decoded:
				break;

def main():
	cp = os.path.dirname(os.path.abspath(__file__))
	dir_img = os.path.join(cp, "img")
	#re.findall(r'[^\/]+(?=\.)',string) # or re.findall(r'([^\/]+)\.',string)
	list_of_files = sorted(file for file in os.listdir(dir_img) 
						   if os.path.isfile(os.path.join(dir_img, file)))
	#print(list_of_files)
	names = ''
	for idx, x in enumerate(list_of_files):
		name = re.findall(r'[^\/]+(?=\.)',x)
		#name = re.findall(r'([^\/]+)\.',x)
		s = ''.join(name)
		names = names + str(idx)+'-'+s+' '
	
	print(names)

	_query_string = input("Query:")

	#n = int(input("Enter number of elements : "))
	#index_list = list(map(int,input("\nEnter the numbers : ").strip().split()))[:n]
	#print("\nList is - ", index_list)
	
	#query_string = "2 5 7;12 16 22"
	l = _query_string.split(";")

	sl = l[1].split(" ")
	index_list = list(map(int, sl))
	cid_s = ""
	for i,j in enumerate(index_list):
		cid_s = cid_s + cid(os.path.join(dir_img, list_of_files[j]))
		#print(cid_s)
		
	#cid_h = cid_s.encode('utf-8')
	#cid_h.hex()
	#print(cid_h)
	#showentropy(cid_s)
	query_string = l[0].replace(' ', ',')+";"+cid_s+";"

	#print(query_string)

	#print(l[0])
	#print(l[0].replace(' ', ','))

	#query_string = l[0].replace(' ', ',')+";"+"6c565499b6de92b5ed74e9e8658588357bd2d77f34a9074e7a4c469755c3e499"+";"
	#print(query_string)

	#query_string = "2,5,22;{};".format(ent)
	#query_string = "0,3;7c565499b6de92b5ed74e9e8658588357bd2d77f34a9074e7a4c469755c3e499;"
	ser.write(str.encode(query_string+'\r\n'))
	responce_serial()
		
	time.sleep(3)
	ser.close()
	print("com port closed")



if __name__ == "__main__":				
	main()