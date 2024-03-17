import pygame
from network import Network
from player import Player
from ball import Ball

pygame.init()

width = 700
height = 500
WHITE = (255, 255, 255)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
SCORE_FONT = pygame.font.SysFont("timesnewroman", 50)


def redrawWindow(win,ball,player, player2,player3=None,player4=None):
    if ball.winner == -1:
        win.fill((0, 0, 0))
        player.draw(win)
        player2.draw(win)
        ball.draw(win)
        left_score_text = SCORE_FONT.render(f"{player.score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{player2.score}", 1, WHITE)
        win.blit(left_score_text, (45, height//2 - 50+left_score_text.get_height()//2))
        win.blit(right_score_text, (width-45-20-right_score_text.get_width()//2, height//2 - 50+right_score_text.get_height()//2))
        if player3 is not None:
            player3.draw(win)
            player4.draw(win)
            up_score_text = SCORE_FONT.render(f"{player3.score}", 1, WHITE)
            down_score_text = SCORE_FONT.render(f"{player4.score}", 1, WHITE)
            win.blit(up_score_text, (width//2-up_score_text.get_width()//2, 45))
            win.blit(down_score_text, (width//2-down_score_text.get_width()//2, height - 45-20-down_score_text.get_height()//2))
    else:
        win.fill((0, 0, 0))
        game_over_text = SCORE_FONT.render(f"game over winner is player {ball.winner}", 1, WHITE)
        win.blit(game_over_text, (width//2-game_over_text.get_width()//2,height//2-game_over_text.get_height()//2))
    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player_count = len(n.pnb) - 1
    while run:
        clock.tick(60)
        tosend = [] 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            tosend.append("up")
        if keys[pygame.K_DOWN]:
            tosend.append("down")
        if keys[pygame.K_LEFT]:
            tosend.append("left")
        if keys[pygame.K_RIGHT]:
            tosend.append("right")
        if keys[pygame.K_w]:
            tosend.append("w")
        if keys[pygame.K_s]:
            tosend.append("s")
        if not tosend:
            tosend = ["none"]

        print(tosend)
        data = n.send(tosend)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if player_count == 2:
            redrawWindow(win, data[2], data[0], data[1])
        else:
            redrawWindow(win, data[4], data[0], data[1], data[2], data[3])

main()
