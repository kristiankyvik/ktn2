import socket
import sys
import select
import json

#bla is the same as raw user input
# 
# global JSON_LOG={
#     "request"="",
# }
# 
# global JSON_CHAT={
#     "request"="",
#     "username"="",
#     "messages"=None
# }


def initUser(sock):
    print "Welcome!"
    request=raw_input("Please write login to enter the chat: ") 
    username=raw_input("Please write a username: ") 

    JSON_Obj={
        "request":"login"
    }
    JSON_Obj["username"]=username
    
    sock.send(json.dumps(JSON_Obj))      
    
# def parser(bla):
#     
#     
#     
#     if bla=="/login":
#         status=1 #logged in
#         
#         
#         
#     elif bla=="/logout":
#         
#     else:
#         pass
#     

def main():
    #json format message
    status=0       
    host, port = "localhost" , 9999
    sock= socket.socket()
    sock.connect((host,port))
    input = [sys.stdin, sock] 
    
    print "Welcome, write login to join" 
    initUser(sock)
    while 1: 
        inputready,outputready,exceptready = select.select(input,[],[])  
        for s in inputready: 
            if s == sock: 
                # handle the server socket 
                data = sock.recv(1024) 
                print(data)   
                                 
            elif s == sys.stdin: #s == sys.stdin 
                # handle standard input
                print "user_you:",
                msg = sys.stdin.readline() 
                try:
                    sock.send(msg.rstrip()) #what creates newline????
                except:
                    print "error"

            else: 
                # handle all other sockets 
                print "hellll"    
        
    sock.close() 

main()