import SocketServer
import threading
import time
import random
import json
import re
valid = re.match('^[\w-]+$', ) is not None



class TCPHandler(SocketServer.BaseRequestHandler):
    
    @staticmethod
    def sendToAll(data, username):
        JSON_Obj={}
        JSON_Obj['response']='message'
        JSON_Obj['message']=data
        for key in ThreadServer.users:
            ThreadServer.users[key].request.send(json.dumps(JSON_Obj))
                    
    @staticmethod    
    def getUserName(self):
        for i in range(len(ThreadServer.users)):
            if ThreadServer.users[i][1]==self:
                return ThreadServer.users[i][0]
                
    @staticmethod
    def processData(self, data):
        time_Stamp="said @ <timestamp>: <the message>"
        username=TCPHandler.getUserName(self)
        data_processed=username+" said @ "+ str(time.strftime("%H:%M:%S"))+": "+data
        ThreadServer.chatRoom.append(data_processed)
        return data_processed
	
    
    @staticmethod
    def checkIfLoggedIn(data):
        if ThreadServer.users.has_key(data["username"]):
            return True
        else:
            return False
            
    @staticmethod
    def welcomeUser(self, data):
        username=data["username"]
        ThreadServer.users[username]=self
        welcome_Message= username + " joined the chat room"
        TCPHandler.sendToAll(welcome_Message, username)
        JSON_Reply= {
            'response': 'login'
        }
        JSON_Reply['username']=username
        JSON_Reply['messages']=ThreadServer.chatRoom
        
        self.request.send(json.dumps(JSON_Reply))

             
    @staticmethod
    def parser (data, self):
        #JSON_Obj={"response":"logout"}
        #JSON_Obj["username"]=username
         
         
         
        if (data["request"]=="login"):
            
            if not TCPHandler.checkIfLoggedIn(data):
                TCPHandler.welcomeUser(self, data)
                
            elif TCPHandler.checkIfLoggedIn(data):
                
            
                
       elif data["request"]=="logout" and TCPHandler.checkIfLoggedIn(data):
           del ThreadServer.users[data["username"]]
                
        else:
            print "prser just managed o print out this"
            
            
        
    def handle(self):
        data= json.loads(self.request.recv(1024).strip())
        TCPHandler.parser(data, self)

        while 1:
            try:
                data= json.loads(self.request.recv(1024))
                TCPHandler.parser(data, self)
                data_processed= TCPHandler.processData(self, data)
                print  ThreadServer.chatRoom
                TCPHandler.sendToAll(data, self)
                

            except:
                print "there was an error"

class ThreadServer (SocketServer.ThreadingMixIn, SocketServer.ForkingTCPServer):
    users={} #change to a freaking dicctionary
    chatRoom=[]    
    pass

def main():
    host ="localhost"
    port= 9999
    server = ThreadServer((host,port),TCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    
    print "server is running.."


main()