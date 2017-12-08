import socket
import os
import sys
import threading


class server(object):
    _BUFF_SIZE = 4096

    def __init__(self, host, port, password):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._password = password
        self.host = host
        self.port = port
        self.s.bind((self.host, self.port))

    def listening(self):
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            c.settimeout(60)
            threading.Thread(target = self.__transfer, args = (c, addr)).start()

    def __transfer(self, c, addr):
        print c.recv(self._BUFF_SIZE)
        print "Incoming connection from {}".format(addr)
        if self.__authentication(c):
            c.close()
            return
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
        print '\n{} disconnected'.format(addr)

    def __authentication(self, c):
        c.send("\nAuthentication required..")
        auth = c.recv(self._BUFF_SIZE)
        if auth != self._password:
            c.send('Incorrect password, terminating connection.')
            print 'Received incorrect password'
            return 1
        else:
            c.send('User authenticated')
            print 'User authenticated'
            return 0

    def __incoming_file(self, c):
        c.send('\nWhich file do you want to send?\n')
        file_name = c.recv(self._BUFF_SIZE)
        file_size = c.recv(self._BUFF_SIZE)
        c.send('handshake')
        
        print '\nfile: {}\nsize: {}'.format(file_name, self.__file_size(file_size))
        f = open(file_name, 'wb')  # add some sort of file type check for sketchy things
        l = c.recv(self._BUFF_SIZE)
        transfered = sys.getsizeof(l) - 33
        bar_update = -1
        while l:
            bar_update = self.__progress_bar(transfered, file_size, bar_update)
            f.write(l)
            l = c.recv(self._BUFF_SIZE)
            transfered += sys.getsizeof(l) - 33
        f.close()

    def __outgoing_file(self, c):
        files = [file for file in os.listdir(os.getcwd()) if file[-3:]!='.py' and os.path.isfile(file) and file[-4:]!='.bat']
        c.send('\nWhich file do you want?\n{}\n'.format('\n'.join(files)))
        file_name = c.recv(self._BUFF_SIZE)
        if file_name not in files:
            c.send('invalid')
            return
        file_size = str(int(os.path.getsize(file_name)))
        c.send(file_name)
        c.send(file_size)
        c.recv(self._BUFF_SIZE)
        print '\nfile: {}\nsize: {}'.format(file_name, self.__file_size(file_size))
        f = open(file_name, 'rb')
        l = f.read(self._BUFF_SIZE)
        transfered = sys.getsizeof(l) - 33
        bar_update = -1
        while l:
            bar_update = self.__progress_bar(transfered, file_size, bar_update)
            c.send(l)
            l = f.read(self._BUFF_SIZE)
            transfered += sys.getsizeof(l) - 33
        f.close()

    def __progress_bar(self, transfered, file_size, bar_update):
        progress = '#'
        remaining = '-'
        percentage = float("{:0.2f}".format(transfered/float(file_size)*100))
        if bar_update != percentage:
            print '\r[{}{}] %{}'.format(progress*int(percentage), remaining*(100-int(percentage)), percentage),
            return percentage
        return bar_update

    def __file_size(self, file_size):  # I don't like this.. gotta make it.. cooler?
        length = len(str(file_size))
        if length > 9:
            return "{:.2f}GB".format(float(file_size)/1000000000)
        elif length > 6:
            return "{:.2f}MB".format(float(file_size)/1000000)
        elif length > 3:
            return "{:.2f}KB".format(float(file_size)/1000)
        else:
            return "{}B".format(file_size)


def main():
    host = ""  # ENTER IP
    # host = socket.gethostname()
    port = 8000
    pw = ""  # ENTER PASSWORD

    server(host, port, pw).listening()


if __name__=='__main__':
    main()

