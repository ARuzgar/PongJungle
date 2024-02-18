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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


objects_to_send = [
    Player(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT,WHITE),
    Player(WIDTH-10-PADDLE_WIDTH, (HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT,WHITE),
    Player(WIDTH//2 - PADDLE_HEIGHT//2, 10, PADDLE_HEIGHT, PADDLE_WIDTH, WHITE),
    Player(WIDTH//2 - PADDLE_HEIGHT//2, HEIGHT - 10 - PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH,WHITE),
    Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
]

def score(player):
    match player:
        case "left":
            objects_to_send[0].score += 1
        case "right":
            objects_to_send[1].score += 1
        case "up":
            objects_to_send[2].score += 1
        case "down":
            objects_to_send[3].score += 1

def handle_collision(ball, left_paddle, right_paddle, upper_paddle, lower_paddle):
    global scorer
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
                ball = objects_to_send[4]
                if player < 2:
                    if data[0] == "up":
                        objects_to_send[player].move(-1)
                    if data[0] == "down":
                        objects_to_send[player].move(1)
                else:
                    if data[0] == "left":
                        objects_to_send[player].move_sideways(-1)
                    if data[0] == "right":
                        objects_to_send[player].move_sideways(1)
                objects_to_send[4].move()
                handle_collision(objects_to_send[4],objects_to_send[0],objects_to_send[1],objects_to_send[2],objects_to_send[3])
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

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

