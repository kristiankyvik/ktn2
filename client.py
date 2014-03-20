import socket
import sys
import select
import json
 
        
def parserServer(data):
    global status
    response=data["response"]
    if response=="login":
        if "error" in data:
            print data["error"]
        else:
            status=1 
            messages=data["messages"]
            length= len(messages)
            for i in range(0,length):
                    print(messages[i])
            print "You have succesfully logged in, you can now chat with otgher members!"
                
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
    
    else:
        JSON_Obj["username"]=username
        JSON_Obj["request"]="message"
        JSON_Obj["message"]=msg
        sock.send(json.dumps(JSON_Obj))       
                        
def main():
    global status, username
    status =0
    username=None
    host, port = "78.91.20.191" , 4467
    sock= socket.socket()
    sock.connect((host,port))
    input = [sys.stdin, sock] 
    #syinput = [server, sock] 
    print "Welcome, write login to join" 
    while 1: 
        inputready,outputready,exceptready = select.select(input,[],[])
        for s in inputready: 
            if s == sock: 
                # handle the server socket 
                data = json.loads(sock.recv(1024))
                parserServer(data)
                                 
            elif s == sys.stdin: #s == sys.stdin 
                msg = sys.stdin.readline().strip() 
                parserClient(msg, sock)

            else: 
                # handle all other sockets 
                print "hellll"    
        
    sock.close() 

main()