import socket
import sys
import select

def main():    
    host, port = "localhost" , 9999
    sock= socket.socket()
    sock.connect((host,port))
    
    input = [sys.stdin, sock]  
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