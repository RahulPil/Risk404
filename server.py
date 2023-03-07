import socket
import threading
from _thread import*
import random
import pickle

global gameID
global usernames

print_lock = threading.Lock()
server_port = 5176
server_name = 'csslab8.uwb.edu'

# begins the creation of the socket, binds it, then waits for
# incomming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen()

def gameSession(connectionSocket, game_sess):
    # check for quit message in a while loop
    # make sure to use the read blocking call and when the client does want to quit we can grind that 

    # if the player is a reg client 
    
    # if the player is the host client

    print_lock.release()

# implement somehting where if the host client tells u its full then tell other people its full too
def main_event_loop(connectionSocket):
    # ask for username?
    connectionSocket.send('Username? '.encode('ascii'))
    username = connectionSocket.recv(1024).decode('ascii')
    check = True

    while check:
        if username in usernames:
            connectionSocket.send('invalid username, please enter it again'.encode('ascii'))
            username = connectionSocket.recv(1024).decode('ascii')
        else:
            usernames.append(username)
            check = False
    
    run = True
    while run: 
        connectionSocket.send('Options:\nEnter 1 for creating a new session\nEnter 2 for an existing game session\nEnter 3 to quit'.encode('ascii'))
        action = int(connectionSocket.recv(1024).decode('ascii'))

        if action == 1:
            #create a new gameID
            game_Sess = random.randint(1, 101)
            # make sure that the game session is unique
            while game_Sess in gameID:
                game_Sess = random.randint(1, 101)

            connections = []
            connections.append(connectionSocket)
            gameID[game_Sess] = connections
            
            # gameID[game_Sess] = connectionSocket

            connectionSocket.send(f'Game Host: {game_Sess}'.encode('ascii'))
            connectionSocket.send(username.encode('ascii'))
            
            # must create thread so that client doesnt get bombarded with messages
            gameSession = threading.Thread(target=gameSession, args=(connectionSocket, game_Sess))
            print_lock.acquire()
            start_new_thread(gameSession, (connectionSocket))

        elif action == 2:
            # join an existing game
            connectionSocket.send(f'Valid game sessions: {gameID.keys()}'.encode('ascii'))
            chosen_game_sess = int(connectionSocket.recv(1024).decode('ascii'))
            gameID[game_Sess].append(connectionSocket)
            host_client_info = pickle.dumps(gameID[chosen_game_sess][0])
            connectionSocket.send(host_client_info.encode('ascii'))
            gameID[chosen_game_sess][0].send(username.encode('ascii'))
            # must create thread so that client doesnt get bombarded with messages
            gameSession = threading.Thread(target=gameSession, args=(connectionSocket, chosen_game_sess))
            print_lock.acquire()
            start_new_thread(gameSession, (connectionSocket, chosen_game_sess))

        elif action == 3:
            # break connection and set run = false
            run = False
            
    print_lock.release()

# if there is a connection, a new thread is created
# it will go to the main_event_loop which will interpert the request from the TCP sender
while True:
    connectionSocket, addr = server_socket.accept()
    main_event = threading.Thread(target=main_event_loop, args=(connectionSocket))

    # get's new lock, will be used by threads for a gracefull exits
    print_lock.acquire()
    start_new_thread(main_event_loop, (connectionSocket))

# closes connection
server_socket.close()