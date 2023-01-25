import socket, os
from time import sleep

# constants

ip,port = 'localhost',9999
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
disk_path = ['A:','B:','C:','E:','F:','D:']

try:
	a = client.connect((ip, port))
	print(f'[CONNECT] to {ip}:{port}')
except:
	print('[ERROR] server is turned off')
	sleep(0.44444)
	exit()
# starting function

def file_info():
	
	file_name = input('file name or path : ').replace('"','')
	file_name_send = None
	if file_name == '-l':
		return 1
	for starts_ in disk_path:
		if file_name.startswith(starts_):
			file_name_send = file_name.split('\\')
			file_name_send = [i for i in file_name_send if '.' in i[-5:-1]]
			file_name_send = file_name_send[0].replace('"','')
			break
	else:
		file_name_send = file_name

	try:
		file_size = os.path.getsize(file_name)

		client.send(f'{file_name_send}+{file_size}'.encode(FORMAT))
	
		print(f'[SENDING] file name: {file_name}')
		sleep(0.4)

		return file_name
	except:
		return 2

def sender_(file_name):

	with open(file_name,'rb') as bin_:
		binary_read = bin_.read(2048)

		while binary_read:
			client.send(binary_read)
			binary_read = bin_.read(2048)
		return True


def receiver_(user, address):
	while True:

		print('[MODE] receiver mode activate')
		try:
			file_name = (user.recv(2048).decode(FORMAT)).split('+')
			print(f'name: {file_name[0]} | size: {file_name[1]}')

			with open('received_' + file_name[0], 'wb') as bin_:
				bytes_recv = 0
				while bytes_recv != int(file_name[1]):
					data = user.recv(2048)
					bin_.write(data)
					bytes_recv += len(bytes(data))
			sleep(0.5)
			return True
		except:
			print('[ERROR] connecting error' + '\n')
			return False

mode = int(input('[MODE] select mode'))
while True:
	if mode == 1:
		print('[MODE] sender mode activate\n')
		try:
			file_name = file_info()
			if file_name == 1:
				print('[CLOSING] closing connection')
				sleep(2)
				break
			elif file_name == 2:
				print('[ERROR] file not found')
				sleep(0.44)
				continue
			try:
				send_flag = sender_(file_name)
				if not send_flag:
					print('[ERROR] file not found')
					continue
			except:
				print('[ERROR] while sending file')
				continue
		except:
			print('[ERROR] something went wrong ')
	elif mode == 2:
		while True:
			pass


