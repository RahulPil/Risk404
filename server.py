import socket
import threading
from _thread import*
import random
import pickle

global gameID

print_lock = threading.Lock()
server_port = 5176
server_name = 'csslab8.uwb.edu'

# begins the creation of the socket, binds it, then waits for
# incomming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen()

def main_event_loop(connectionSocket):
    # ask for username?
    run = True
    while run: 
        connectionSocket.send('Options:\nEnter 1 for creating a new session\nEnter 2 for an existing game session\nEnter 3 to quit'.encode('ascii'))
        action = int(connectionSocket.recv(1024).decode('ascii'))

        if action == 1:
            #create a new gameID
            game_Sess = random.randint(1, 101)
            gameID[game_Sess] = connectionSocket
            connectionSocket.send(f'Game Host: {game_Sess}'.encode('ascii'))
            # must create thread so that client doesnt get bombarded with messages
            
        elif action == 2:
            # join an existing game
            connectionSocket.send(f'Valid game sessions: {gameID.keys()}'.encode('ascii'))
            chosen_game_sess = int(connectionSocket.recv(1024).decode('ascii'))
            host_client_info = pickle.dumps(gameID[chosen_game_sess])
            connectionSocket.send(host_client_info.encode('ascii'))
            # must create thread so that client doesnt get bombarded with messages 

        elif action == 3:
            # break connection and set run = false
            run = False
            
    print_lock.release()

# if there is a connection, a new thread is created
# it will go to the main_event_loop which will interpert the request from the TCP sender
while True:
    connectionSocket, addr = server_socket.accept()
    main_event = threading.tHREAD(target=main_event_loop, args=(connectionSocket,))

    # get's new lock, will be used by threads for a gracefull exits
    print_lock.acquire()
    start_new_thread(main_event_loop, (connectionSocket, ))

# closes connection
server_socket.close()