import pygame
import save

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tester sprawności psychomotorycznej")
font = pygame.font.SysFont(None, 30)

test_buttons = []
test_names = ["Test 1", "Test 2", "Test 3","Test 4", "Wyniki"]
for i, name in enumerate(test_names):
    button = pygame.Rect(50, 50 + i*50, 200, 40)
    test_buttons.append(button)

in_game = True
while in_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(test_buttons):
                if button.collidepoint(event.pos):
                    if "Test 3" == test_names[i]:
                        import grasłuchowa
                    elif "Test 2" == test_names[i]:
                        import gar1Trudniejsza
                        in_game = True
                    elif "Test 1" == test_names[i]:
                        import gra1
                        in_game = True
                    elif "Test 4" == test_names[i]:
                        import grasłuchowaTrudniejsza
                    elif "Wyniki"== test_names[i]:
                        try:
                            wyniki1 = save.wczytaj_wyniki_z_pliku("wyniki1.txt")
                            save.wypisz_wyniki(wyniki1)
                            save.rysuj_wykres(wyniki1,1)
                        except:
                            pass
                        try:
                            wyniki2 = save.wczytaj_wyniki_z_pliku("wyniki2.txt")
                            save.wypisz_wyniki(wyniki2)
                            save.rysuj_wykres(wyniki2, 2)
                        except:
                            pass
                        try:
                            wyniki3 = save.wczytaj_wyniki_z_pliku("wyniki3.txt")
                            save.wypisz_wyniki(wyniki3)
                            save.rysuj_wykres(wyniki3, 3)
                        except:
                            pass
                        try:
                            wyniki4 = save.wczytaj_wyniki_z_pliku("wyniki4.txt")
                            save.wypisz_wyniki(wyniki4)
                            save.rysuj_wykres(wyniki4, 4)
                        except:
                            pass



    screen.fill(WHITE)

    for i, button in enumerate(test_buttons):
        pygame.draw.rect(screen, GRAY, button)
        text = font.render(test_names[i], True, BLACK)
        screen.blit(text, (button.x+10, button.y+10))

    pygame.display.flip()

pygame.quit()
