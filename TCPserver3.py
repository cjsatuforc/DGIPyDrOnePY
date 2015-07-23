__author__ = 'Dylan'

from socket import *
import threading

host = '127.0.0.1'
port = 5005

#Creating socket object
sockServer = socket()
#Binding socket to a address. bind() takes tuple of host and port.
sockServer.bind((host, port))
#Listening at the address
sockServer.listen(5) #5 denotes the number of clients can queue

lastCommand = "waiting"
lastProperties = "0|0|0|0|0|0|0|0|0|12|0|0|0"

def clientthread(connection):
    global lastProperties
    global lastCommand

    while True:
        data = connection.recv(1024)

        command = data.decode()
        commandSplit = command.split()

        if len(commandSplit) > 0:
            print(commandSplit)

            if commandSplit[0] == "C":
                print("CONTROLLER")

                lastCommand = command[1] + " " + command[2]

                connection.send(lastProperties.encode())
            elif commandSplit[0] == "D":
                print("DRONE")

                if commandSplit[1] != "SEND":
                    lastProperties = command[1]

                    connection.send(lastCommand.encode())
            else:
                print("NOT FOUND")

while True:
    print("new connection")

    connection, clientAddress = sockServer.accept()

    th1 = threading.Thread(target=clientthread, args=[connection])
    th1.start()

sockServer.close()