#PyATM Server
import sys
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 4777))
s.listen(1)
connection, address = s.accept()

f = open('pins.txt', 'r')
pins = f.read()

count = 0

while count != 3:
    username = connection.recv(1024)
    cred = connection.recv(1024)
    if cred.decode('utf-8') in pins:
        msg = 'Credentials accepted\n'
        connection.sendall(msg.encode())
        break
    else:
        msg = 'Credentials incorrect'
        connection.sendall(msg.encode())
        count += 1
        if count == 3:
            msg = 'Too many tries'
            connection.sendall(msg.encode())
            time.sleep(3)
            connection.close()

f.close()

################### AUTH_COMPLETE

while 1:
    try:
        data = connection.recv(1024)
    except:
        continue
    if data.decode('utf-8') == '1':
        f = open('pins.txt', 'a')
        while 1:
            newuser = connection.recv(1024)
            newpwd = connection.recv(1024)
            pwdconfirm = connection.recv(1024)
            if newpwd.decode('utf-8') != pwdconfirm.decode('utf-8'):
                msg = 'Passwords do not match'
                connection.sendall(msg.encode())
            else:
                f.write(newuser.decode('utf-8') + ':' + newpwd.decode('utf-8') + '\n')
                f.close()
                f = open('accbal.txt', 'a')
                f.write(newuser.decode('utf-8') + ':$0')
                f.close()
                print('Credentials added - ' + newuser.decode('utf-8') + ':' + newpwd.decode('utf-8'))
                msg = 'Credentials added'
                connection.sendall(msg.encode())
                break
    elif data.decode('utf-8') == '2':
        f = open('pins.txt', 'r')
        msg = '\n' + f.read()
        connection.sendall(msg.encode())
        f.close()
    elif data.decode('utf-8') == '3':
        f = open('accbal.txt', 'r')
        for line in f:
            line = line.rstrip()
            if username.decode('utf-8') + ':' in line:
                lst = line.split(':')
                msg = 'Your account balance is: ' + lst[1]
                connection.sendall(msg.encode())
        f.close()
        






