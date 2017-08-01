import socket
import sys
import os


# put print statements in a file
class client(object):
    _BUFF_SIZE = 4096
    bar_update = -1

    def __init__(self, host, port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self._password = password
        self.files = [file for file in os.listdir(os.getcwd()) if file[-3:]!='.py' and os.path.isfile(file) and file[-4:]!='.bat']

    def connect(self):
        self.s.connect((self.host, self.port))
        self.s.send("Thanks for the connection")
        self.__authenticate()
        self.__transfer()
        self.s.shutdown(socket.SHUT_WR)
        self.s.close()

    def __authenticate(self):
        print self.s.recv(self._BUFF_SIZE)
        self.s.send(self._password)
        msg = self.s.recv(self._BUFF_SIZE)
        print msg
        if msg != 'User authenticated':
            quit()

    def __transfer(self):
        msg = ''
        while True:
            print self.s.recv(self._BUFF_SIZE)
            msg = raw_input()
            self.s.send(msg)
            if msg == 's' or msg == 'r' or msg == 'q':  # use set notation
                break
        if msg == 'r':
            self.__receive_file()
        elif msg == 's':
            self.__send_file()

    def __receive_file(self):
        print self.s.recv(self._BUFF_SIZE)
        self.s.send(raw_input())
        file_name = self.s.recv(self._BUFF_SIZE)
        file_size = self.s.recv(self._BUFF_SIZE)
        self.s.send('handshake')
        if file_name == 'invalid':
            print 'Invalid choice or incorrect spelling'
            quit()
        print '\nfile: {}\nsize: {}'.format(file_name, self.__file_size(file_size))
        f = open(file_name, 'wb')
        l = self.s.recv(self._BUFF_SIZE)
        transfered = sys.getsizeof(l) - 33
        while l:
            self.__progress_bar(transfered, file_size)
            f.write(l)
            l = self.s.recv(self._BUFF_SIZE)
            transfered += sys.getsizeof(l) - 33
        f.close()

    def __send_file(self):
        print self.s.recv(self._BUFF_SIZE)
        print '\n'.join(self.files)
        while True:
            file_name = raw_input()
            if file_name == 'q':
                quit()
            if file_name not in self.files:
                print 'Try again..'
            else:
                self.s.send(file_name)
                file_size = str(int(os.path.getsize(file_name)))
                self.s.send(file_size)
                self.s.recv(self._BUFF_SIZE)
                break
        print '\nfile: {}\nsize: {}'.format(file_name, self.__file_size(file_size))
        f = open(file_name, 'rb')
        l = f.read(self._BUFF_SIZE)
        transfered = sys.getsizeof(l) - 33
        while l:
            self.__progress_bar(transfered, file_size)
            self.s.send(l)
            l = f.read(self._BUFF_SIZE)
            transfered += sys.getsizeof(l) - 33
        f.close()

    def __progress_bar(self, transfered, file_size):
        progress = '#'
        remaining = '-'
        percentage = float("{:0.2f}".format(transfered/float(file_size)*100))
        if self.bar_update != percentage:
            print '\r[{}{}] %{}'.format(progress*int(percentage), remaining*(100-int(percentage)), percentage),
            self.bar_update = percentage

    def __file_size(self, file_size):
        length = len(str(file_size))
        if length > 9:
            return "{:.2f}GB".format(float(file_size)/1000000000)
        elif length > 6:
            return "{:.2f}MB".format(float(file_size)/1000000)
        elif length > 3:
            return "{:.2f}KB".format(float(file_size)/1000)
        else:
            return "{}B".format(file_size)


def __find_host():
    location = ''
    while True:
        location = raw_input('\nConnecting from Pear Street? (y/n)\n')
        if location == 'y':  # computer ip
            return "192.168.0.47"
        elif location == 'n':  # public ip
            return "24.68.115.7"
        else:
            print 'try again'


def main():
    host = __find_host()
    port = 8888
    pw = 'water'

    client(host, port, pw).connect()


if __name__=='__main__':
    main()

