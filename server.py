import socket

ip,port = 'localhost',9999
FORMAT = 'utf-8'
flag = True
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()
while True:
    try:
        user, address = server.accept()

        while True:

            file_name = (user.recv(2048).decode(FORMAT)).split('+')
            print(f'name: {file_name[0]} | size: {file_name[1]}')
            file = open('received_' + file_name[0], 'wb')
            bytes_recv = 0
            while bytes_recv != int(file_name[1]):
                data = user.recv(2048)
                file.write(data)
                bytes_recv += len(bytes(data))

            file.close()
    except:
        print('[ERROR] connecting error')
        break

server.close()