__author__ = 'Amit'
import json
import Queue
import hashlib
import socket
from network import *

class protocol:
    """
    transfer, and use the data from the gui for running the proccess of  using PassEr

    """

    def __init__(self):
        self.login_jason_file=str()
        self.url_queue=Queue.Queue()
        self.md5obj=hashlib.md5.new()
        #self.main_data='URLs_login.json'
        self.last_registers=dict()


    def start_use(self):
        return

    def edit_jsonfile(self,data):

        with open('URLs_login.json', 'w') as my_json:
            assert isinstance(my_json, object)
        json.dump(data, my_json)

    def get_login_params(self,url):
        pass

    def add_Last_registers(self,url):
        file1=open("Last_registers.txt","w")
        file1.write(str(url))
        file1.close()


    def read_correct_json(self):

        json1_file = open("URLs_login.json","r")
        json1_str = json1_file.read()
        #print json1_file.read(),"!!!!!!!!"
        json1_data = json.loads(json1_str)

        #print json1_file.read(),"!!!!!!!!"
        json1_file.close()

        return  dict(json1_data)



    def add_data_tojson(self,data):



        """
        add new website to PassEr service
        the data format :
        UrL/number_of_fields/login parameter/ login parameter...

        """

        url=data.split('/')[0]
        if not self.is_url_exists(url):
            data=data.split('/')[1:]


            new_data={}
            present_dict=self.read_correct_json()
            print present_dict
            present_dict[url]=data
            print present_dict
            new_data=present_dict[url]=data
            file1=open("URLs_login.json","w")
            json.dump(present_dict,file1)
            file1.close()
            self.add_Last_registers(url)


    def is_url_exists(self,url):
        corrent_dict=self.read_correct_json()
        for key in corrent_dict:

            if url==key:
                return  True

        return False


    def remove_url(self,url):
        pass




conn = socket.socket()         # Create a socket object
host ='127.0.0.1' #TODO: Get local machine name
port = 12345                # Reserve a port for your service.

conn.connect((host, port))
while True:
    connection_client = network("client")
    connection_client.start_session_server()
    print "+++++++++++++++++++++++++++++++"
    data="register/Admin/AD12345"
    datatosend = connection_client.enc("key_server",data)
    print connection_client.dec("Key_server",datatosend)
    conn.send(datatosend)
    server_reply=connection_client.dec(conn.recv(1024))
    print server_reply
    break
conn.closeI()

#program_worker=protocol()
#program_worker.add_data_tojson("TheBank/3/amit/123/my id!!!")
