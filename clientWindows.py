import socket
import sys
import select
import json
import threading

 
        
def parserServer(data):
    global status
    response=data["response"]
    if response=="login":
        if "error" in data:
            print data["error"]
        else:
            status=1
            print "=============You have succesfully logged in===========\n==========you can now chat with other members!=============" 
            messages=data["messages"]
            length= len(messages)
            for i in range(0,length):
                    print(messages[i])
            
    elif response=="logout":
        if "error" in data:
            print data["error"]
        else:
            print "You have succesfully logged out!"
            status=0
                    
    elif response=="message":
        if "error" in data:
            print data["error"]+ " Write login to retry!"
        else:
            print data["message"]
        
    else:
        print "parser did not understand"
        
def parserClient(msg, sock):
    global status, username
    JSON_Obj={}
    if msg=='login':
        JSON_Obj["request"]="login"
        
        if status==0:
            username=raw_input("Please write a username: ").strip() 
            JSON_Obj['username']=username
            sock.send(json.dumps(JSON_Obj))
        else:
            JSON_Obj["username"]=username
            sock.send(json.dumps(JSON_Obj))
        
    elif msg=="logout":
        print "logout message being sent to server"
        JSON_Obj["request"]="logout"
        JSON_Obj["username"]=username
        status=0
        sock.send(json.dumps(JSON_Obj))
        sock.close()
        
        
    
    else:
        JSON_Obj["username"]=username
        JSON_Obj["request"]="message"
        JSON_Obj["message"]=msg
        sock.send(json.dumps(JSON_Obj)) 
         

class Client(threading.Thread):
    global sock
    

    def __init__(self):
        
        global status, username, sock
        status=1
        username=None
        host, port = "78.91.20.191" , 4467
        sock= socket.socket()
        sock.connect((host,port))
        print "Welcome, write login to join"

        t = threading.Thread(target = self.read)
        t.start()

        t2 = threading.Thread(target = self.write)
        t2.start()

    def read(self):
        global sock, status
        while status:
            data = json.loads(sock.recv(1024))
            parserServer(data)

    def write(self):
        global sock
        while True:
            msg = sys.stdin.readline().strip() 
            parserClient(msg, sock)


client = Client()



