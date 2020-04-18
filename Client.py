import socket
import select
import sys
from time import *


s = socket.socket()                                                   # Creating the socket.
print("Enter the system ip address of host:")                         # Asking the user system ip address of host and port number.
host = input()
print("Enter the port number:")
port = int(input())
s.connect((host, port))                                               # Connecting with the host.

# Time to receive the data from server
entrycongo = str(s.recv(1024), "utf-8")                                 # The bellow print statements will print the instructions.
print(entrycongo)
instructions1 = str(s.recv(1024), "utf-8")
print(instructions1)
instructions2 = str(s.recv(1024), "utf-8")
print(instructions2)

termination = 1
while termination<21:                                               # The main while loop in client file it stops after all the questions are done but as our questions are large in number the game comes to end.
    data = str(s.recv(1024), "utf-8")
    if data == "Won":
        break
    print(data)
    c, c1, c2 = select.select([sys.stdin, s], [], [], 20)           # This line helps us to get the input from user and it is linked with respone in the server file.
    if len(c) > 0:
        if c[0] == sys.stdin:
            start = time()
            y = input()
            end = time()
            if end-start <= 10:                                     # This is for checking if the buzzer is pressed in time or not..
                # print(y)
                s.send(str.encode(y))
                if y != "yes":                                      # Checking if 'yes' is pressed or anything else.. is presses.
                     termination += 1
                     continue
                else:
                    data2 = str(s.recv(1024), "utf-8")
            else:
                s.send(str.encode("hi"))
        else:                                                       # If anyone of the user pressed buzzer, this is for other users.
            nobuzzer = str(s.recv(1024), "utf-8")
            termination += 1
            print(nobuzzer)
            continue
    else:
        none_pressed = str(s.recv(1024), "utf-8")                   # If noone presses the buzzer..
        termination+=1
        print(none_pressed)
        continue
    # data2 = str(s.recv(1024), "utf-8")
    if data2 == "Answer the question:":
        print(data2)
        time1 = time()
        answer = input()
        time2 = time()
        if time2-time1 <= 10:                                       # Checking if the user answered in < 10 secs or not.
            # print(answer)
            s.send(str.encode(answer))
        # termination += 1
        else:
            s.send(str.encode("time exceeded........"))
        # time.sleep(1)
        reply = str(s.recv(1024), "utf-8")
        print(reply)

        termination += 1


data3 = str(s.recv(1024), "utf-8")                                   # Prints the win message or as we couldnt accomadate infinite number of questions
                                                                     # if no player wins then it prints draw message.
print(data3)