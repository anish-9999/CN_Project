import socket
import time
# import system
import select
import random
connections = []
addresses = []

questions = [".Holes in a standard round of golf?",".The MS Windows computer operating system version that succeeded Vista?",".Greek 'monos'?",".Total dots on a die?",".Square root of 576?",".Total of the sides on a pentagon and a heptagon?",".Days of the average human menstrual cycle?",".Lines traditionally in a sonnet?",".Whole miles in a marathon running event?",".The number followed by .14159, fully known as pi, used to calculate the circumference and area of a circle?",
             ".The first Apollo moon landing?",".The Lord is My Shepherd... psalm number?",".Planets in our solar system?",".American Presidents assassinated in office?",".Old Chinese method of counting on one hand, up to this number, using the thumb to touch the tip and three joints of each finger?",".The curse of Scotland' diamonds playing card?",".The age that Brian Jones, Janis Joplin, Jimmy Hendrix, Jim Morrison and Kurt Kobain all died?",".A bronze desk (anagram)?",
             ".A Nebuchadnezzar wine/champagne bottle equates to how many normal bottles?",".he average age of a US combat soldier in the Vietnam war (also a 1985 Paul Hardcastle No1 hit song)?"]
answers = [18,7,1,21,24,12,28,14,26,3,11,23,8,4,16,9,27,13,20,19]
points = []

def create_socket():                                            # Function for the creation of socket with.
    try:
        global host
        global port
        global s
        host = ""
        s = socket.socket()
        port = int(input("Enter the port number: "))
    except socket.error as msg:
        print("Error while creating the socket:"+" msg")

def bind_socket():                                              # This helps in binding the host the port.
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(100)
    except socket.error as msg:
        print("Error while binding the socket:"+" msg")

def accepting_connections():                                    # This function accepts the connections it removes all the old connections when we are again running the file.
    for c in connections:
        c.close()
    del connections[:]
    del addresses[:]
    del points[:]

    j = 0
    while True:                                                 # The main loop which enables us to perform multiple operations.
        while j < 3:                                            # Restricting the number of connections to specified number(You can change it to any value.).
            conn, add = s.accept()
            connections.append(conn)
            addresses.append(add)
            points.append(0)
            print("Connection is established with player " + str(j+1) + str(add[0]))
            conn.send(str.encode("Congrats you have entered the game, you are player "+str(j+1)))
            time.sleep(1)
            conn.send(str.encode("1.You will be given 10s to press the buzzer after the display of question\n2.After pressing the buzzer you again have 10s to answer the question\n3.Buzzer is pressing 'yes' only, for anything else -0.5.\n"
                                 "4.If your response is correct 1 point is awarded else -0.5 is awarded.\n"))
            time.sleep(1.25)
            conn.send(str.encode("Win Critieria: The player who gets 5 points first is considered as winner!!!"))

            j = j+1
            if j==3:
                print("Maximum number of clients connected...")
        thread()                                                      # Calling the function which links the user and clients.
        break

def thread():
    i = 0
    q_no=0
    for j in questions:                                               # Restoring the questions after everytime we use it.
        if j == -1:
            j = questions.index(j)+1

    while i < len(questions)+10000:
        q = random.randint(0, len(questions)-1)                       # Randomly generating the the question.
        if questions[q] != "-1":                                      # Making sure that questions are not repeated.
            q_no += 1
            for p in connections:
                p.send(str.encode(str(q_no) + questions[q]+" Type yes if you know the answer "))
            response1 = select.select(connections, [], [], 20)        # Collecting responses from the client.
            if len(response1[0]) > 0:
                conn_name = response1[0][0]
                response1 = ()
                c_index = connections.index(conn_name)
                # b = str(conn_name.recv(1024, "utf-8"))
                # #Written in two lines....
                b = conn_name.recv(1024)
                b = b.decode("utf-8")
                for c in connections:
                    if c != conn_name:
                        c.send(str.encode("Be quick player " + str(c_index+1)+"has pressed the buzzer"))
                print("b = " + b)
                if b == "yes":

                    time.sleep(0.25)
                    conn_name.send(str.encode("Answer the question:"))
                    answer = conn_name.recv(1024)
                    answer = answer.decode("utf-8")
                    if answer == str(answers[q]):                   # Checking if participants answer was right or wrong.
                        time.sleep(1)
                        conn_name.send(str.encode("Correct answer you will receive 1 point...."))
                        points[c_index] = points[c_index]+1
                        if points[c_index] >= 5:                    # Checking the winner everytime someone wins a point.
                             for c in connections:
                                 c.send(str.encode("Won"))
                             break

                    elif answer == "time exceeded........":
                        conn_name.send(str.encode("You need to answer before 10 secs."))
                    else:
                        points[c_index]=points[c_index]-0.5
                        time.sleep(1)
                        conn_name.send(str.encode("Wrong answer!! -0.5"))
                elif b == "hi":
                    conn_name.send(str.encode("Time up"))
                else:
                    points[c_index] = points[c_index] - 0.5
            else:
                for c in connections:
                    c.send(str.encode("No one pressed the buzzer moving to next question..."))
            questions[q] = "-1"
        i += 1



def main():
    create_socket()
    bind_socket()
    accepting_connections()
    y=0
    d=0
    for i in range(len(points)):                                        # Checking the winner and sending appropriate messages.
       if points[i]> y:
           y=points[i]
           d=i
    if y>=5:
        connections[d].send(str.encode("Congrats you won the game.."))
        for i in range(len(connections)):
            if i!=d:
                connections[i].send(str.encode("player "+str(d+1)+" Won the game"))
    else:
        for c in connections:
            c.send(str.encode("Set of questions completed, it is a draw...."))


main()





