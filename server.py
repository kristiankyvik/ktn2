import SocketServer
import threading
import time
import random
import json



class TCPHandler(SocketServer.BaseRequestHandler):
    
    @staticmethod
    def sendToAll(data, self):
        for key in ThreadServer.users:
            ThreadServer.users[key].request.send(data)
            

        
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
    def checkIfLoggedIn(self):
        if Thread.users.contains(self):
            return True
        else:
            return False
            
    @staticmethod
    def welcomeUser(self, data):
        username=data["username"]
        ThreadServer.users[username]=self
        welcome_Message= username + " joined the chat room"
        TCPHandler.sendToAll(welcome_Message, self)
        # for key in ThreadServer.users:
        #     ThreadServer.users[key].request.send(welcome_Message)
            
             
    @staticmethod
    def parser (data, self):
        if data["request"]=="login":
            username=TCPHandler.welcomeUser(self, data)
            print ThreadServer.users
       
        elif data=="/logout":
            if TCPHandler.checkIfLoggedIn(self):
                Thread.users.remove(self)
                print ThreadServer.users
            else:
                 "user was no logged in"
        else:
            pass
            
        
    def handle(self):
        data= json.loads(self.request.recv(1024).strip())
        TCPHandler.parser(data, self)

        while 1:
            try:
                data= json.loads(self.request.recv(1024))
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