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


def redrawWindow(win,player, player2,player3,player4,ball):
    win.fill((0, 0, 0))
    player.draw(win)
    player3.draw(win)
    player4.draw(win)
    player2.draw(win)
    ball.draw(win)
    left_score_text = SCORE_FONT.render(f"{player.score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{player2.score}", 1, WHITE)
    up_score_text = SCORE_FONT.render(f"{player3.score}", 1, WHITE)
    down_score_text = SCORE_FONT.render(f"{player4.score}", 1, WHITE)
    win.blit(left_score_text, (45, height//2 - 50+left_score_text.get_height()//2))
    win.blit(right_score_text, (width-45-20-right_score_text.get_width()//2, height//2 - 50+right_score_text.get_height()//2))
    win.blit(up_score_text, (width//2-up_score_text.get_width()//2, 45))
    win.blit(down_score_text, (width//2-down_score_text.get_width()//2, height - 45-20-down_score_text.get_height()//2))
    print(player.score, player2.score, player3.score, player4.score)
    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        tosend = ["none"]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            tosend = ["none"]
        elif keys[pygame.K_UP]:
            tosend = ["up"]
        elif keys[pygame.K_DOWN]:
            tosend = ["down"]
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            tosend = ["none"]
        elif keys[pygame.K_LEFT]:
            tosend = ["left"]
        elif keys[pygame.K_RIGHT]:
            tosend = ["right"]
        print(tosend)
        data = n.send(tosend)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(win, data[0], data[1], data[2], data[3], data[4])

main()
