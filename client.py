import socket,os

ip,port = 'localhost',1235
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))


def file_info():
	try:
		file_name = input('file name: ')
		if 'disconnect' in file_name:
			client.close()

		file_size = os.path.getsize(file_name)
		client.send(f'{file_name}+{file_size}'.encode(FORMAT))
		print(f'[SENDING] file : {file_name}')
		return file_name
	except:
		print('[ERROR] file not found')



while True:

	try:
		file_name = file_info()

		#print('[ERROR] sending file info error')



		file = open(file_name,'rb')
		data = file.read(2048)

		while data:
			client.send(data)
			data = file.read(2048)

		file.close()
	except:
		print('[ERROR] file not found')


