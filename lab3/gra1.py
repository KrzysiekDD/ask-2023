import pygame
import random
import save


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONT = pygame.font.SysFont(None, 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prosta gra reakcji")

def create_ball():
    ball = pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50), 50, 50)
    return ball

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

tutorial=0
balls = []
clicked_balls = []
start_time = None
game_time = None
table = []
BALLS_PER_TURN = 1

runningg = True
while runningg:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningg = False
            import main
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if ball.collidepoint(event.pos):
                    clicked_balls.append(ball)
                    balls.remove(ball)
                    # Obliczenie czasu reakcji
                    if len(clicked_balls) == BALLS_PER_TURN:
                        game_time = pygame.time.get_ticks() - start_time
                        if tutorial>3:
                            table.append(game_time)
                            save.zapisz_wynik_do_pliku("wyniki1.txt", game_time)
                    break

    screen.fill(WHITE)

    for ball in balls:
        pygame.draw.circle(screen, BLACK, ball.center, ball.width//2)

    for ball in clicked_balls:
        pygame.draw.circle(screen, RED, ball.center, ball.width//2)

    if 0 ==len(balls):
        tutorial=tutorial+1
        for i in range(BALLS_PER_TURN):
            balls.append(create_ball())
        start_time = pygame.time.get_ticks()
        clicked_balls = []

    if tutorial>3:
        draw_text("Wyniki:", FONT, BLACK, screen, 10, 10)
        for i, result in enumerate(table):
            draw_text(f"{i+1}. {result} ms", FONT, BLACK, screen, 10, 40 + i*30)


    else:
        draw_text("Gra polega na kliknięciu w jak najkrótszym czasie kropek", FONT, BLACK, screen, 10, 10)


    pygame.display.flip()
    if game_time is not None and pygame.time.get_ticks() - start_time > 2000:
        start_time = pygame.time.get_ticks()

pygame.quit()
