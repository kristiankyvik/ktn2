import SocketServer
import threading
import time
import random
import json
import re

class TCPHandler(SocketServer.BaseRequestHandler):
    
    @staticmethod
    def sendToAll(data, username):
        JSON_Reply={}
        JSON_Reply['response']='message'
        JSON_Reply['message']=data
        for key in ThreadServer.users:
            if key != username:
                ThreadServer.users[key].request.send(json.dumps(JSON_Reply))
                
    @staticmethod
    def processData(self, JSON_data):
        time_Stamp="said @ <timestamp>: <the message>"
        data_processed=JSON_data["username"]+" said @ "+ str(time.strftime("%H:%M:%S"))+": "+ JSON_data["message"]
        ThreadServer.chatRoom.append(data_processed)
        return data_processed
        
    @staticmethod
    def checkIfEmpty():
        if not ThreadServer.users:
            ThreadServer.chatRoom=[]
            
    @staticmethod
    def checkValidity(str):
		return re.match('^[\w-]+$', str) is not None
    
    @staticmethod
    def checkIfLogged(username):
        if ThreadServer.users.has_key(username):
            return True
        else:
            return False
             
    @staticmethod
    def parser (JSON_data, self):
        print JSON_data
        JSON_Reply={}
        
        if (JSON_data["request"]=="login"):
            username=JSON_data["username"] 
            
            JSON_Reply["response"]="login"
            JSON_Reply["username"]=username
            
            if not TCPHandler.checkValidity(username):
                JSON_Reply["error"]="Invalid Username!"
                self.request.send(json.dumps(JSON_Reply))
                
            elif TCPHandler.checkIfLogged(username):
                JSON_Reply["error"]="Name already taken!"
                self.request.send(json.dumps(JSON_Reply))
            
            elif not TCPHandler.checkIfLogged(username):
                ThreadServer.users[username]=self
                welcome_Message= username + " joined the chat room"
                TCPHandler.sendToAll(welcome_Message, username)
                JSON_Reply['messages']=ThreadServer.chatRoom
                self.request.send(json.dumps(JSON_Reply))
            
                
            else:
                print "parser not understand logg in message from client"              
                      
        elif JSON_data["request"]=="logout" and TCPHandler.checkIfLogged(JSON_data["username"]):
            username=JSON_data["username"]
            del ThreadServer.users[JSON_data["username"]]
            goodbye_Message= username + " has left the conversation"
            TCPHandler.sendToAll(goodbye_Message, JSON_data['username'])
            JSON_Reply["username"]= username            
            JSON_Reply["response"]="logout"
            self.request.send(json.dumps(JSON_Reply))
            TCPHandler.checkIfEmpty()
            self.request.close()
              
            
       
        elif JSON_data["request"]=='message':
            try:
                if 'username' in JSON_data:
                    username=JSON_data["username"]
                    if not TCPHandler.checkIfLogged(username):
                        JSON_Reply["error"]="You are not logged in!"
                        JSON_Reply["response"]="message"
                        self.request.send(json.dumps(JSON_Reply))  
                    else:
                        processed_Data=TCPHandler.processData(self, JSON_data)
                        TCPHandler.sendToAll(processed_Data, username)
            except:
                print "was an error"
        else:
            print "parser did not recognize message"
            
    def handle(self):
        while 1:
            JSON_data= json.loads(self.request.recv(1024))
            TCPHandler.parser(JSON_data, self)

class ThreadServer (SocketServer.ThreadingMixIn, SocketServer.ForkingTCPServer):
    users={} #change to a freaking dicctionary
    chatRoom=[]
    pass

def main():
    host ="78.91.20.191"
    port= 4467
    server = ThreadServer((host,port),TCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    
    print "server is running.."


main()