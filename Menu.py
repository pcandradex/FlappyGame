import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Const import WIN_WIDTH, WIN_HEIGHT, C_YELLOW, MENU_OPTION, C_WHITE, C_ORANGE


class Menu:

    def __init__(self, window):
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load('./assets/PNG/Bg1/Bg1-all.png').convert()  # Carrega a imagem de fundo
        self.ground_img = pygame.image.load('./assets/PNG/Bg1/ground.png').convert()  # Carrega o chão
        self.ground_scr = 0
        self.window.blit(self.ground_img, (self.ground_scr, 768))

    def run(self):
        menu_option = 0
        running = True
        while running:
            self.window.blit(self.background, (0,0))
            self.menu_text(50, 'FLAPPY GAME', C_YELLOW,(WIN_WIDTH / 2, 250))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(50, MENU_OPTION[i], C_ORANGE, (WIN_WIDTH / 2, 600 + 50 * i))
                else:
                    self.menu_text(50, MENU_OPTION[i], C_WHITE, (WIN_WIDTH / 2, 600 + 50 * i))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) -1
                    if event.key == pygame.K_RETURN: #ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

