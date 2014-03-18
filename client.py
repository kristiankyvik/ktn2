import socket
import sys
import select
import json




def initUser(sock):
    global username
    print "Welcome!"
    request=raw_input("Please write login to enter the chat: ") 
    username=raw_input("Please write a username: ") 

    JSON_Obj={
        "request":"login"
    }
    JSON_Obj["username"]=username
    
    sock.send(json.dumps(JSON_Obj))  
        
def parserIn(data):
    global status
    response=data["response"]
    if response=="login":
        if data.has_Key("error"):
            print data["error"]
        else:
            print "trying to chnage status"
            status=1 
             
    elif response=="message":
        print data["message"]
        
    elif response=="logout":
        if data.has_Key(error):
            print data["error"]
        else:
            print "you have logged out, status changing"
            status=0  
    else:
        print "parser did not understand"
        
def parserOut(msg, sock):
    global status
    if msg='login':
        if status==0:
            initUser(sock)
        else:
            JSON_Obj={"request":"login"}
            JSON_Obj["username"]=username
            sock.send(json.dumps(JSON_Obj))
    elif msg=="logout":
        JSON_Obj={"request":"login"}
        JSON_Obj["username"]=username
        sock.send(json.dumps(JSON_Obj))
        
                        
def main():
    #json format message
    global status= 0
    global username=None
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
                data = json.loads(sock.recv(1024).strip())
                print data 
                                 
            elif s == sys.stdin: #s == sys.stdin 
                msg = sys.stdin.readline().rstrip() 
                try:
                    sock.send() #what creates newline????
                except:
                    print "error"

            else: 
                # handle all other sockets 
                print "hellll"    
        
    sock.close() 

main()