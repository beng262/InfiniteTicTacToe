import socket
import threading

# Constants
HOST = '0.0.0.0'  # Server will bind to all available interfaces
PORT = 5555
GRID_SIZE = 3

# Game state
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
players = ['X', 'O']
current_player = 0


# Client handler function
def client_thread(conn, player):
    global current_player
    conn.sendall(str.encode(players[player]))

    while True:
        try:
            data = conn.recv(2048)
            if not data:
                break

            move = data.decode('utf-8')
            row, col = map(int, move.split(','))

            # Process move
            if board[row][col] == '':
                board[row][col] = players[player]
                current_player = (current_player + 1) % 2
                conn.sendall(str.encode("valid"))
                broadcast(board)
            else:
                conn.sendall(str.encode("invalid"))

        except:
            break

    conn.close()


# Broadcast game state to all clients
def broadcast(game_state):
    game_state_str = ''.join([''.join(row) for row in game_state])
    for conn in connections:
        conn.sendall(str.encode(game_state_str))


# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

connections = []
print(f"Server started on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    connections.append(conn)
    print(f"Connected to {addr}")
    threading.Thread(target=client_thread, args=(conn, current_player)).start()