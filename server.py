import socket
import os
import time
import sys

    
class server(object):
    _BUFF_SIZE = 4096
    _password = 'water'

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = "192.168.0.47"
        self.port = 8888
        self.s.bind((self.host, self.port))
        self.files = self.files_to_view()

    def files_to_view(self): #add a proper path
        files = []
        # return [file if file[-3:]!='.py' for file in os.listdir(os.getcwd())]
        for file in os.listdir(os.getcwd()): # this will need to change
            if file == 'server.py':
                continue
            if os.path.isfile(file):
                files.append(file)
        return files

    def wait_for_connection(self):
        self.s.listen(5)
        count = 5
        while count:
            st = time.time()
            c, addr = self.s.accept()
            print c.recv(self._BUFF_SIZE)
            print "Incoming connection from {}".format(addr)
            if self.__authentication(c):
                c.close()
                continue
            while True:
                c.send('Sending (s) or Receiving (r) file? q to quit')  # client perspective
                msg = c.recv(self._BUFF_SIZE)
                if msg == 's' or msg == 'r' or msg == 'q':
                    break
                else:
                    c.send('Try again..\n')
            if msg == 's':
                self.__incoming_file(c)
            elif msg == 'r':
                self.__outgoing_file(c)
            c.close()
            count -= 1
            print ''.format(time.time() - st)

    def __authentication(self, c):
        c.send("Welcome to Dylan's file share server.\nPassword authentication required..")
        auth = c.recv(self._BUFF_SIZE)
        if auth != self._password:
            print 'Received incorrect password'
            c.send('Incorrect password, terminating connection.')
            return 1
        else:
            c.send('User authenticated')
            print 'User authenticated'
            # print c.recv(self._BUFF_SIZE)
            return 0
            
    def __incoming_file(self, c):
        print 'Receiving file...\n'
        c.send('\nWhich file do you want to send?')
        file_name = c.recv(self._BUFF_SIZE)
        
        file_size = c.recv(self._BUFF_SIZE)
        f = open(file_name, 'wb')  # add some sort of file type check for sketchy things
        l = c.recv(self._BUFF_SIZE)
        
        print 'the file is: {}\nthe size is: {}'.format(file_name, file_size)
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
            f.write(l)
            l = c.recv(self._BUFF_SIZE)
            transfered += sys.getsizeof(l) - 33
        f.close()
    
    def __outgoing_file(self, c):
        print "Sending file...\n"
        c.send('\nWhich file do you want?\n{}'.format('\n'.join(self.files)))
        file_name = c.recv(self._BUFF_SIZE)
        file_size = str(int(os.path.getsize(file_name)))
        if not os.path.isfile(file_name):
            c.send('invalid')
            print "lol they can't spell"
            return
        c.send(file_name)
        c.send(file_size)
        f = open(file_name, 'rb')
        print 'the file is: {}\nthe size is: {}'.format(file_name, file_size)
        l = f.read(self._BUFF_SIZE)
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
            transfered += sys.getsizeof(l) - 33
            c.send(l)
            l = f.read(self._BUFF_SIZE)
        f.close()
        print "Sending file..."


def main():
    serv = server()
    serv.wait_for_connection()

if __name__=='__main__':
    main()

