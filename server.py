import socket
import threading 
from _thread import*
import random
import errno
import pickle
global usernames
global gameID

print_lock = threading.Lock()
server_port = 5176
server_name = 'csslab8.uwb.edu'

# begins the creation of the socket, binds it, then waits for
# incomming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen()

def gameSession(connectionSocket):
    run = True
    while run:
        try:
            request = connectionSocket.recv(1024).decode('ascii')
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
            if request == 'SERVER QUIT':
                run = False

    print_lock.release()
    return 

def main_event_loop(connectionSocket):
    connectionSocket.send('Please enter a username: '.encode('ascii'))
    username = connectionSocket.recv(1024).decode('ascii')
    while username not in usernames:
        connectionSocket.send('Username is taken please enter a new one: ')
        username = connectionSocket.recv(1024).decode('ascii')
    
    usernames.append(username)

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
            game_session = threading.Thread(target=gameSession, args=(connectionSocket))
            print_lock.acquire()
            start_new_thread(gameSession, (connectionSocket))
            
        elif action == 2:
            # join an existing game
            connectionSocket.send(f'Valid game sessions: {gameID.keys()}'.encode('ascii'))
            chosen_game_sess = int(connectionSocket.recv(1024).decode('ascii'))
            host_client_info = pickle.dumps(gameID[chosen_game_sess])
            connectionSocket.send(host_client_info.encode('ascii'))
            # send the host client the username of the newly joined client. 
            gameID[chosen_game_sess].send(username.encode('ascii'))
            # must create thread so that client doesnt get bombarded with messages 
            game_session = threading.Thread(target=gameSession, args=(connectionSocket))
            print_lock.acquire()
            start_new_thread(gameSession, (connectionSocket))

        elif action == 3:
            # break connection and set run = false
            # actually disconnect the client from the server and end the thread
            # somehow figure out a way to remove the username from array
                # unless i can just remove the username from the array because technically the username variable associated in a thread is the same as the client socket
            # should remove the associated username as well
            usernames.remove(username)
            connectionSocket.close()
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