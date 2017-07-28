import socket
import sys
import os


# os.chdir("..") # for exe
BUFF_SIZE = 4096
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
    print 'Receiving File...\n'
    print s.recv(BUFF_SIZE)
    s.send(raw_input())
    file_name = s.recv(BUFF_SIZE) # add while True loop for retries
    
    
    if file_name == 'invalid':
        print "Invalid choice or incorrect spelling"
        quit()
    file_size = s.recv(BUFF_SIZE)
    f = open(file_name, 'wb')
    l = s.recv(BUFF_SIZE)
    print 'the file is: {}\nthe size is: {}'.format(file_name, file_size)
    transfered = sys.getsizeof(l) - 33
    t = -1
    while(l):
        progress = '#'
        remaining = '-'
        percentage = float("{:0.2f}".format(transfered/float(file_size)*100))
        if t != percentage:
            print '\r[{}{}] %{}'.format(progress*int(percentage), remaining*(100-int(percentage)), percentage),
            t = percentage
        else:
            pass
        # print "=>[{}] bytes transfered: {}".format(file_name, file_size)
        f.write(l)
        l = s.recv(BUFF_SIZE)
        transfered += sys.getsizeof(l) - 33
    f.close()

# send
elif msg == 's':
    print s.recv(BUFF_SIZE)
    files = [file for file in os.listdir(os.getcwd()) if os.path.isfile(file)]
    print '\n'.join(files)
    while True:
        file_name = raw_input()
        if file_name == 'q':
            quit()
        if file_name not in files:
            print 'Try again..'
        else:
            s.send(file_name)
            file_size = str(int(os.path.getsize(file_name)))
            s.send(file_size)
            break
    f = open(file_name, 'rb')
    print 'the file is: {}\nthe size is: {}'.format(file_name, file_size)
    print 'Sending file...\n'
    l = f.read(BUFF_SIZE)
    t = -1
    transfered = sys.getsizeof(l) - 33
    while(l):
        progress = '#'
        remaining = '-'
        percentage = float("{:0.2f}".format(transfered/float(file_size)*100))
        if t != percentage:
            print '\r[{}{}] %{}'.format(progress*int(percentage), remaining*(100-int(percentage)), percentage),
            t = percentage
        else:
            pass
        # print "=>[{}] bytes transfered: {}".format(file_name, file_size)
        s.send(l)
        l = f.read(BUFF_SIZE)
        transfered += sys.getsizeof(l) - 33
    f.close()
print '\nBYE BYE'
s.shutdown(socket.SHUT_WR)
s.close()

