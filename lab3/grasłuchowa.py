import pygame
import random
import time
import save

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra na reakcję słuchową")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.font.init()
FONT = pygame.font.SysFont(None, 48)

tutorial=0
def play_sound():
    pygame.mixer.Sound('beep.wav').play()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

score = 0
sound_played = False
spacja = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            import main
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not sound_played:
                sound_played = True
                delay = random.uniform(1, 5)
                start_time = time.time() + delay
                spacja =1
            elif event.key == pygame.K_SPACE and sound_played:
                tutorial = tutorial + 1
                spacja = 0
                end_time = time.time()
                reaction_time = end_time - start_time
                score = int(reaction_time * 1000)
                sound_played = False
                if score>0:
                    save.zapisz_wynik_do_pliku("wyniki3.txt", score)

    if sound_played and time.time() >= start_time:
        play_sound()
    print(tutorial)
    screen.fill(WHITE)

    if score<0:
        draw_text(f"Za szybko", FONT, BLACK, screen, 20, 100)
    else:
        draw_text(f"Twój wynik: {score} ms", FONT, BLACK, screen, 20, 100)

    if spacja ==0:
        draw_text("Wciśnij spację, by usłyszeć dźwięk", FONT, BLACK, screen, 20, 40)
    else:
        draw_text("Wciśnij spację, gdy usłyszysz dźwięk", FONT, BLACK, screen, 20, 40)

    pygame.display.update()

pygame.quit()
