import socket
import threading 
from _thread import*
import random
import errno
import pickle
import re

usernames = []
gameID = {}

print_lock = threading.Lock()
server_port = 5176
server_name = 'csslab8.uwb.edu'

# begins the creation of the socket, binds it, then waits for
# incomming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_name, server_port))
server_socket.listen()

def gameSession(connectionSocket):
    run = True
    while run:
        try:
            request = connectionSocket.recv(1024).decode()
        except connectionSocket.error:
            err = connectionSocket.error.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                sleep(1)
                print ('No data available')
                continue
            else:
                # a "real" error occurred
                sys.exit(1)
        else:
            if 'SERVER QUIT' in request:
                # parse gameID
                print('Client left game')
                foundGameID = re.search("[0-9]+", request)
                # check to see if its in the gameID global dict if it is then remove
                if foundGameID != None:
                    foundGameID = foundGameID.group()
                    print('Retreived gameID')

                    # game ID found
                    print_lock.acquire()
                    del gameID[int(foundGameID)]
                    print_lock.release()
                run = False                
                    

    return 

def main_event_loop(connectionSocket):
    global usernames
    global gameID
    connectionSocket.send('Please enter a username: '.encode())
    username = connectionSocket.recv(1024).decode()
    
    while username in usernames:
        connectionSocket.send('Username is taken please enter a new one: '.encode())
        username = connectionSocket.recv(1024).decode()
    
    print_lock.acquire()
    usernames.append(username)
    print_lock.release()

    print(username)

    run = True
    while run:
        connectionSocket.send('Options:\nEnter 1 for creating a new session\nEnter 2 for an existing game session\nEnter 3 to quit'.encode())
        action = connectionSocket.recv(1024).decode()
        print(action)
        action = int(action)
        
        if action == 1:
            #create a new gameID
            # do the mutex lock thing here
            game_Sess = random.randint(1, 101)
            while game_Sess in gameID:
                game_Sess = random.randint(1, 101)

            host_client_info = []
            host = []
            connectionSocket.send(f'Game Host: {game_Sess}'.encode())
            host_server_name = connectionSocket.recv(1024).decode()
            host_server_port = connectionSocket.recv(1024).decode()

            host_client_info.append(host_server_name)
            host_client_info.append(host_server_port)
            host.append(host_client_info)
            host.append(connectionSocket)

            print_lock.acquire()
            gameID[game_Sess] = host
            print_lock.release()

            gameSession(connectionSocket)
            
        elif action == 2:
            # join an existing game
            print_lock.acquire()
            gameIds = [key for key in gameID]
            if len(gameIds) == 0:
                connectionSocket.send('no current ongoing game sessions'.encode())
                continue
            connectionSocket.send(f'Valid game sessions: {gameIds}'.encode())
            print_lock.release()
            chosen_game_sess = int(connectionSocket.recv(1024).decode())
            
            #check to see if its a valid game id
            while True:
                print('entering valid gameID check loop')
                print_lock.acquire()
                gameIds = [key for key in gameID]
                print_lock.release()

                if chosen_game_sess not in gameIds:
                    connectionSocket.send(f'Please choose a valid game session: {gameIds}'.encode())
                    chosen_game_sess = int(connectionSocket.recv(1024).decode())
                    print(type(chosen_game_sess))
                else:
                    break
                    
            connectionSocket.send('Thank you'.encode())
            print_lock.acquire()
            host_client = pickle.dumps(gameID[chosen_game_sess][0])
            print_lock.release()
            connectionSocket.send(host_client)
            # send the host client the username of the newly joined client. 
            print_lock.acquire()
            gameID[chosen_game_sess][1].send(username.encode())
            print_lock.release()

            gameSession(connectionSocket)

        elif action == 3:
            # break connection and set run = false
            # actually disconnect the client from the server and end the thread
            # somehow figure out a way to remove the username from array
                # unless i can just remove the username from the array because technically the username variable associated in a thread is the same as the client socket
            # should remove the associated username as well
            print(username, ' is leaving')
            print_lock.acquire()
            usernames.remove(username)
            print_lock.release()
            connectionSocket.close()
            print(usernames)
            run = False
        continue
    return

# if there is a connection, a new thread is created
# it will go to the main_event_loop which will interpert the request from the TCP sender
while True:
    connectionSocket, addr = server_socket.accept()
    print('Client just connected')
    main_event = threading.Thread(target=main_event_loop, args=(connectionSocket, ))

    # get's new lock, will be used by threads for a gracefull exits
    start_new_thread(main_event_loop, (connectionSocket, ))

# closes connection
server_socket.close()