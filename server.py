import SocketServer
import threading
import time
import random



class TCPHandler(SocketServer.BaseRequestHandler):
    
    @staticmethod
    def sendToAll(data):
        for i in range(len(ThreadServer.users)):
            if ThreadServer.users[i]==self:
                continue
            ThreadServer.users[i].request.send(data)
            
    @staticmethod
    def welcomeUser(self):
        userID=random.randint(10000, 90000)
        userName="user_"+str(userID)
        ThreadServer.users.append((userName,self))
        welcome_Message= userName + " joined the chat room"
        for i in range(len(ThreadServer.users)):
            ThreadServer.users[i][1].request.send(welcome_Message)
        return userName
        
    @staticmethod    
    def getUserName(self):
        for i in range(len(ThreadServer.users)):
            if ThreadServer.users[i][1]==self:
                return ThreadServer.users[i][0]
                
    @staticmethod
    def processData(self, data):
        time_Stamp="said @ <timestamp>: <the message>"
        userName=TCPHandler.getUserName(self)
        data_processed=userName+" said @ "+ str(time.strftime("%H:%M:%S"))+": "+data
        ThreadServer.chatRoom.append(data_processed)
        return data_processed
	
	def Parse(data):
	if data.startswith('/nick'):
            oldpeer = UserName
            UserName = data.replace('/nick', '', 1).strip()
            if len(UserName):
                data("%s now goes by %s\r\n" \
                                % (str(oldpeer), str(UserName)))
            else: UserName = oldpeer

			elif data_processed.startswith('/logout'):
                data= "logout"

        return data

    
    def handle(self):
        userName=TCPHandler.welcomeUser(self)
        while 1:
            try:
                data= self.request.recv(1024)
				TCPHandler.Parse(data)
                data_processed= TCPHandler.processData(self, data)
                
                #TCPHandler.sendToAll(data) #why the fuckkkkkkk
                #print data_processed
                print  ThreadServer.chatRoom
                for i in range(len(ThreadServer.users)):
                    if ThreadServer.users[i][1]==self:
                        continue
                    ThreadServer.users[i][1].request.send(data_processed) 
            except:
                print "there was an error"

class ThreadServer (SocketServer.ThreadingMixIn, SocketServer.ForkingTCPServer):
    users=[] #change to a freaking dicctionary
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