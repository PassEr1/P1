__author__ = 'Amit'

import socket
import random
import math
import threading
import time
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


expected_key_size = 16
expected_key_size = 16

class sniffer:
    pass


class network():


    def __init__(self, location):
        self.key_gui = str()
        self.key = str()
        self.location = location

        self.cipher_server =str()
        self.cipher_gui = str()


    def enc(self, key_kind, data):
        if key_kind == "key_gui":
            return self.cipher_gui.encrypt(data)


        elif key_kind == "key_server":
            return self.cipher_server.encrypt(data)

    def dec(self, key_kind, data):

        if key_kind == "key_gui":
            return self.cipher_gui.decrypt(data)

        elif key_kind == "key_server":
            return self.cipher_server.decrypt(data)



    def start_session_server(self):
        if self.location == "server":
            server = diffy_hallen(self.location)
            server.send_n()
            self.key=server.key
            self.cipher_server=AESCipher(self.key)


        elif self.location == "client":
            client_diff = diffy_hallen(self.location)
            client_diff.generate_n()
            self.key = client_diff.key
            self.cipher_server=AESCipher(self.key)



    def start_session_gui(self):
        pass


    def padding_for_key(self,key):
        key=str(key)
        return key.zfill(expected_key_size)


    """
    data="hello !!!!!"
    connection_serv = network("server")
    print "1111111111"
    connection_client = network("client")

    th_server=threading.Thread(target=connection_serv.start_session_server)
    th_server.start()


    #connection_serv.start_session_server()
    connection_client.start_session_server()


    datatosend = connection_client.enc("key_server",data)

    print datatosend
    print connection_serv.dec("key_server",datatosend) + "this is the data that came from client!!!"

    """

class AESCipher(object):


    def __init__(self,key):
        self.bs = 32
        #self.key = hashlib.sha256(key.encode()).digest()
        self.key=str(key)


    def encrypt(self, raw):


        raw = self._pad(raw)

        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return str(base64.b64encode(iv + cipher.encrypt(raw)))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



class diffy_hallen():
    def __init__(self, location):


        # super(diffy_hallen, self).__init__()
        self._sock = socket.socket()
        # socket.AF_INET,socket.SOCK_RAW
        self.location = location
        self.g = 206555690
        self.y = int()
        self.n = int()  # the mod number
        # self.other_send=other_send
        self.limit = random.randrange(1000, 1000000)
        self.key = None

    def generate_n(self):

        if self.location == "server":
            count = 2

            while True:
                isprime = True

                for x in range(2, int(math.sqrt(count) + 1)):
                    if count % x == 0:
                        isprime = False
                        break

                if isprime and (count > self.limit):
                    return count

                count += 1
        elif self.location == "client":

            self.ask_n()
            print " success" , self.key

    def generate_y(self):
        n = self.n - 1
        y = random.randrange(1, n)
        return y

    def ask_n(self):
        if self.location == "client":
            self._sock.connect(('localhost', 8820))
            print "connected"
            data = ""
            while not data.split('/')[0] == 'get_the_public_module':
                self._sock.send('send_me_public_module')
                data = self._sock.recv(1024)

            data = data.split('/')[1]
            print data
            self.n = int(data)
            self._sock.send("public_module_OK")
            self.create_key(0)
            """
            self.y = self.generate_y()
            print str((self.g ** self.y) % self.n)
            self._sock.send(str((self.g ** self.y) % self.n))

            key_stage2 = int(self._sock.recv(1024))
            self.create_key(key_stage2)
            print key_stage2  """
            self._sock.close()

    def send_n(self):

        self._sock.bind(('0.0.0.0', 8820))
        self._sock.listen(1)
        (client_socket, client_address) = self._sock.accept()
        print "accept "
        data = ""
        # data = client_socket.recv(1024)
        while data != 'send_me_public_module':
            data = client_socket.recv(1024)

        n = self.generate_n()
        client_socket.send("get_the_public_module/" + str(n))
        self.n = n
        data = client_socket.recv(1024)
        print "recived 222222222"
        while not data =="public_module_OK":
               client_socket.send("get_the_public_module/" + str(n))
        print "   33333333333333"
        self.create_key(client_socket)


        """
        data = self._sock.recv(1024)
        print data+" 111111111"
        if data == "public_module_OK":
            self.y = self.generate_y()
            key_stage2 = int(self._sock.recv(1024))
            self._sock.send(str((self.g ** self.y) % self.n))
            self.create_key(key_stage2)
        print str(n)
        """
        client_socket.close()
        self._sock.close()

    def create_key(self, client_socket):
        self.y = self.generate_y()
        if self.location == "client":
            self._sock.send(str( (self.g**self.y)% self.n  ))

            data = int(self._sock.recv(1024))
            key = (int(data)**self.y)%self.n
            print key , "    original key"
            self.key = self.padding_for_key(key)





        elif self.location=="server":
            data=client_socket.recv(1024)
            key = (int(data)**self.y)%self.n
            self.key = self.padding_for_key(key)

            client_socket.send(str( (self.g**self.y)% self.n  ))


    def getkey(self):
        return str(self.key)



    def padding_for_key(self,key):
        return str(key).zfill(expected_key_size)



    def is_prime(self, n):
        if n == 2 or n == 3: return True
        if n < 2 or n % 2 == 0: return False
        if n < 9: return True
        if n % 3 == 0: return False
        r = int(n ** 0.5)
        f = 5
        while f <= r:
            # print '\t',f
            if n % f == 0: return False
            if n % (f + 2) == 0: return False
            f += 6
        return True


    """
    server = diffy_hallen("server")
    th_server = threading.Thread(target=server.send_n)
    th_server.start()

    client = diffy_hallen("client")
    client.generate_n()


    print str(client.key)+"     444444444444"
    print str(server.key)+"     5555555555555555"

    """
