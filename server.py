import socket 
from time import sleep
import os


# constants
ip,port = 'localhost',9999
FORMAT = 'utf-8'
flag = True
file_name_send = None
disk_path = ['A:','B:','C:','E:','F:','D:']


# creating socket | socket bind | activating listen mode
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()



# receive function

def sender_(user, address):
    print('[MODE] sender mode activate')
    def file_info():

        file_name = input('file name or path : ').replace('"', '')
        file_name_send = None
        if file_name == '-l':
            return 1
        for starts_ in disk_path:
            if file_name.startswith(starts_):
                file_name_send = file_name.split('\\')
                file_name_send = [i for i in file_name_send if '.' in i[-5:-1]]
                file_name_send = file_name_send[0].replace('"', '')
                break
        else:
            file_name_send = file_name

        try:
            file_size = os.path.getsize(file_name)

            user.send(f'{file_name_send}+{file_size}'.encode(FORMAT))

            print(f'[SENDING] file name: {file_name}')
            sleep(0.4)

            return file_name
        except:
            return 2

    def send(file_name):
        while True:

            with open(file_name, 'rb') as bin_:
                binary_read = bin_.read(2048)
                try:
                    while binary_read:
                        user.send(binary_read)
                        binary_read = bin_.read(2048)
                except:
                    print('[ERROR] error while sending file')


                    
    try:
        while True:

            file_name = file_info()
            if file_name == 1:
                print('[CLOSING] closing sender mode')
                sleep(2)
                break
            elif file_name == 2:
                print('[ERROR] file not found')
                sleep(0.44)
                continue

            send(file_name)
    except:
        print('[ERROR] connecting error' + '\n')
        return False



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
            print('[ERROR] connecting error'+'\n')
            return False

    
# main loop
print('[WAIT] waiting for connection')
user, address = server.accept()
while True:
    if user == None:
        print('[WAIT] waiting for connection')
        user, address = server.accept()
    try:
        print('[MODE] choose mode')
        sleep(0.5)
        mode = int(input('[MODE] receiver mode 1 | sender mode 2 | : '))
        # mode = 1
        if not user:
            print('[ERROR] connecting error 303'+'\n')
            break
        if mode == 1:
            while True:
                            
                    #print('[MODE] receiver mode leave')
                                
                try:
                    flag = receiver_(user, address)
                    if not flag:
                        user,address = None, None
                        break
                    print('[SUCCESS] receiving success'+'\n')
                except:
                    print('[ERROR] while receiving file'+'\n')

                    break
        elif mode == 2:
            while True:
                sender_(user,address)
    except:
        print('[ERROR] invalid mode'+'\n')


server.close()


