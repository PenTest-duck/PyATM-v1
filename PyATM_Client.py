#PyATM Client
import socket
import sys

SRV_ADDR = input('PyATM Server IP address: ')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SRV_ADDR, 4777))

count = 0

while count != 3:
    username = input('Enter username: ')
    s.sendall(username.encode())
    pwd = input('Enter password: ')
    cred = username + ':' + pwd
    s.sendall(cred.encode())
    rcv = s.recv(1024)
    derecv = rcv.decode('utf-8')
    print(derecv)
    if 'accepted' in derecv:
        break
    else:
        rcv = s.recv(1024)
        print(rcv.decode('utf-8'))
        sys.exit()
            

def menu():
    print('Menu:')
    print('1: New credentials registration')
    print('2: View credentials')
    print('3: View balance')
    print('4: Exit')

while 1:
    menu()
    opt = input('Option: ')
    if opt == '1':
        s.sendall(opt.encode())
        
        while 1:
            newuser = input('New username: ')
            s.sendall(newuser.encode())
            newpwd = input('New password: ')
            s.sendall(newpwd.encode())
            pwdconfirm = input('Confirm password: ')
            s.sendall(pwdconfirm.encode())
            rcv = s.recv(1024)
            derecv = rcv.decode('utf-8')
            print(derecv)
            if 'match' in derecv:
                continue
            else:
                break
    if opt == '2':
        s.sendall(opt.encode())
        rcv = s.recv(2048)
        print(rcv.decode('utf-8'))
    if opt == '3':
        s.sendall(opt.encode())
        rcv = s.recv(2048)
        print(rcv.decode('utf-8'))
    if opt == '4':
        s.close()
        sys.exit()
    else:
        continue
