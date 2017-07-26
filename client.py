import socket
import sys
import os


os.chdir("..")
BUFF_SIZE = 1024
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "192.168.0.47"
port = 8888
s.connect((host, port))
s.send("Thanks for the connection")

# authentication
print s.recv(BUFF_SIZE)
s.send(raw_input())
msg = s.recv(BUFF_SIZE)
print msg
if msg != 'User authenticated':
    quit()

# type of data transfer
while True:
    print s.recv(BUFF_SIZE)
    msg = raw_input()
    s.send(msg)
    if msg == 's' or msg == 'r' or msg == 'q':
        break

#receive
if msg == 'r':
    print s.recv(BUFF_SIZE)
    s.send(raw_input())
    file_name = s.recv(BUFF_SIZE) # add while True loop for retries
    if file_name == 'invalid':
        print "Invalid choice or incorrect spelling"
        quit()
    f = open(file_name, 'wb')
    l = s.recv(BUFF_SIZE)
    print 'Receiving File...'
    file_size = sys.getsizeof(l) - 33
    while(l):
        print "=>[{}] bytes transfered: {}".format(file_name, file_size)
        f.write(l)
        l = s.recv(BUFF_SIZE)
        file_size += sys.getsizeof(l) - 33
    f.close()

# send
elif msg == 's':
    print s.recv(BUFF_SIZE)
    files = [file for file in os.listdir(os.getcwd())]
    files.remove('client')
    print '\n'.join(files)
    while True:
        file_name = raw_input()
        if file_name == 'q':
            quit()
        if file_name not in files:
            print 'Try again..'
        else:
            s.send(file_name)
            break
    f = open(file_name, 'rb')
    print 'Sending file...'
    l = f.read(BUFF_SIZE)
    file_size = sys.getsizeof(l) -33
    while(l):
        print "=>[{}] bytes transfered: {}".format(file_name, file_size)
        s.send(l)
        l = f.read(BUFF_SIZE)
        file_size += sys.getsizeof(l) - 33
    f.close()

s.shutdown(socket.SHUT_WR)
s.close()

