__author__ = 'Amit'
import os
import socket
import sys
from thread import *
import hashlib
from network import *

def answer(data):
    """
    data= request/data

    """
    data= data.split("/")
    print data +"----print 01"
    if data[0] is "pass_confirm":
        pass
    if data[0] is "register":
        register(data[1],data[2],check_idies())


    if data[0] is "startSession":
        pass
    if data[0] is "get_login":
        pass
    if data[0] is "post_web":
        pass

def register(username,password,id):
    """
    password and usernae wouldnt include: ' _'
    """

    name="user:"+str(id)+":id.json"
    f=open(name,'w')

    edit_jsonfile('{}',name)
    add_data_tojson("User"+"2"+"/"+username+"/"+password)
    f.close

def check_idies(self):
    """user:num:id.json"""
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    bigest=0
    for f in files:
        name=str(f)
        if name.startswith("user:"):
            number=name.split(":")[1]


            if int(number) > bigest:
                bigest=int(number)

    return int(bigest)+1
"""
-----------------------------communication with client-----------------------------------------
"""

def clientthread(conn):
    #Sending message to connected client
    connection_serv = network("server")
    connection_serv.start_session_server()
    print "------------------------------------"

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data=conn.recv(1024)
        print data
        client_request=connection_serv.dec("Key_server",data)
        print str(client_request) +"this is the client req"
        reply = answer(client_request)
        if not client_request:
            print "data is empty!!!"
            break

        conn.sendall(reply)

    #came out of loop
    conn.close()
"""
-----------------------------------------------------------------------------------------------
"""

def edit_jsonfile(data,dirf):

    with open(dirf, 'w') as my_json:
        assert isinstance(my_json, object)
        json.dump(data, my_json)


def get_login_params(url,dirf):
    pass

def add_Last_registers(url):
    file1=open("Last_registers.txt","w")
    file1.write(str(url))
    file1.close()

def read_correct_json(dirf):

    json1_file = open(dirf,"r")
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






HOST = ''   # Symbolic name meaning all available interfaces
PORT = 12345 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads



while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
