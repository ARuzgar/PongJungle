import socket
from _thread import *
from player import Player
from ball import Ball
import pickle


server = socket.gethostbyname('localhost')
scorer = "none"
port = 5556

WIDTH, HEIGHT = 700, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
WINNING_SCORE = 11

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
remote = input("Press 'r' for remote and 'l' for local: ")
while remote not in ('r', 'l'):
    print("Invalid input. Please enter 'r' or 'l'.")
    remote = input("Press 'r' for remote and 'l' for local: ")
print(f"You selected: {remote}")

if remote == "r":
    player_count = 0
    valid_inputs = ["2", "4"]
    player_count = input("2 players or 4 players: ")
    while player_count not in valid_inputs:
        print("Invalid input. Please enter '2' or '4'.")
        player_count = input("2 players or 4 players: ")
    player_count = int(player_count)
else:
    player_count = 2
print("Waiting for a connection, Server Started")

two_player_objects = [
    Player(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE),
    Player(WIDTH - 10 - PADDLE_WIDTH, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT, WHITE),
    Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
]

four_player_objects = [
    Player(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT,WHITE),
    Player(WIDTH-10-PADDLE_WIDTH, (HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT,WHITE),
    Player(WIDTH//2 - PADDLE_HEIGHT//2, 10, PADDLE_HEIGHT, PADDLE_WIDTH, WHITE),
    Player(WIDTH//2 - PADDLE_HEIGHT//2, HEIGHT - 10 - PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH,WHITE),
    Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
]

if player_count == 2:
    objects_to_send = two_player_objects
else:
    objects_to_send = four_player_objects

def score(player):
    if player == "left":
        objects_to_send[0].score += 1
        if objects_to_send[0].score >= WINNING_SCORE:
            objects_to_send[player_count].winner = 1
    elif player == "right":
        objects_to_send[1].score += 1
        if objects_to_send[1].score >= WINNING_SCORE:
            objects_to_send[player_count].winner = 2
    elif player == "up":
        objects_to_send[2].score += 1
        if objects_to_send[2].score >= WINNING_SCORE:
            objects_to_send[player_count].winner = 3
    elif player == "down":
        objects_to_send[3].score += 1
        if objects_to_send[3].score >= WINNING_SCORE:
            objects_to_send[player_count].winner = 4


def handle_collision(ball, left_paddle, right_paddle, upper_paddle=None, lower_paddle=None):
    global scorer
    if upper_paddle is not None:
        if ball.y_vel < 0:
            if ball.x >= upper_paddle.x and ball.x <= upper_paddle.x + upper_paddle.width:
                if ball.y - ball.radius <= upper_paddle.y + upper_paddle.height:
                    scorer = "up"
                    ball.y_vel *= -1
                    if ball.y_vel <= 20:
                        ball.y_vel += 0.5
                    middle_x = upper_paddle.x + upper_paddle.width / 2
                    difference_in_x = middle_x - ball.x
                    reduction_factor = (upper_paddle.width / 2) / ball.VEL
                    x_vel = difference_in_x / reduction_factor
                    ball.x_vel = -1 * x_vel
        else:
            if ball.x >= lower_paddle.x and ball.x <= lower_paddle.x + lower_paddle.width:
                if ball.y + ball.radius >= lower_paddle.y:
                    scorer = "down"
                    if ball.x_vel <= 20:
                        ball.x_vel += 0.5
                    ball.y_vel *= -1
                    middle_x = lower_paddle.x + lower_paddle.width / 2
                    difference_in_x = middle_x - ball.x
                    reduction_factor = (lower_paddle.width / 2) / ball.VEL
                    x_vel = difference_in_x / reduction_factor
                    ball.x_vel = -1 * x_vel
    else:
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                scorer = "left"
                ball.x_vel *= -1
                if ball.x_vel <= 20:
                    ball.x_vel += 0.5
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                scorer = "right"
                if ball.x_vel <= 20:
                    ball.x_vel += 0.5
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def threaded_client(conn, player):
    conn.send(pickle.dumps(objects_to_send))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print("Disconnected")
                break
            else:
                ball = objects_to_send[player_count]
                if remote == "l":
                    for key in data:
                        if key == "up":
                            objects_to_send[1].move(-1)
                        elif key == "down":
                            objects_to_send[1].move(1)
                        if key == "w":
                            objects_to_send[0].move(-1)
                        elif key == "s":
                            objects_to_send[0].move(1)
                else:
                    if player < 2:
                        for key in data:
                            if key == "up":
                                objects_to_send[player].move(-1)
                            elif key == "down":
                                objects_to_send[player].move(1)
                    else:
                        for key in data:
                            if key == "left":
                                objects_to_send[player].move_sideways(-1)
                            elif key == "right":
                                objects_to_send[player].move_sideways(1)
                ball.move()
                if player_count == 4:
                    handle_collision(ball,objects_to_send[0],objects_to_send[1],objects_to_send[2],objects_to_send[3])
                else:
                    handle_collision(ball,objects_to_send[0],objects_to_send[1])
                if ball.x < 0:
                    ball.reset("left")
                    score(scorer)
                elif ball.x > WIDTH:
                    ball.reset("right")
                    score(scorer)
                elif ball.y < 0:
                    ball.reset("up")
                    score(scorer)
                elif ball.y > HEIGHT:
                    ball.reset("down")
                    score(scorer)

                print("Received: ", data)
                print("Sending : ", objects_to_send)
            conn.sendall(pickle.dumps(objects_to_send))
        except Exception as error:
            print("oopsi", error)
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if (remote == "r" and currentPlayer < player_count) or (remote == "l" and currentPlayer < 1):
        start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

