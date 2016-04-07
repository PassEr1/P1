
from socket import socket
import threading
import time
from AESCipher import *
from diffy_hallen import *



class network():

    expected_key_size = 16
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

        """


        """
        print data +"-----print 02"
        if key_kind == "key_gui":

            return self.cipher_gui.decrypt(data)

        elif key_kind == "key_server":
            print self.cipher_server.decrypt(data)+"------------------- print 03"
            return self.cipher_server.decrypt(data)



    def start_session_server(self):
        if self.location == "server":
            server = diffy_hallen(self.location)
            server.send_n()
            self.key=server.key
            print self.key+"   end"
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


    datatosend = connection_client.enc("key_server",data)# for client side

    print datatosend
    print connection_serv.dec("key_server",datatosend) + "this is the data that came from client!!!" # for server side
    """


