import sys

import pygame
from Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Level import Level
from Menu import Menu

class Game:

    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
        pygame.init()
        pygame.display.set_caption('Flappy Game')
        self.window = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.background = pygame.image.load('./assets/PNG/Bg1/Bg1-all.png').convert() #Carrega a imagem de fundo
        self.ground_img  = pygame.image.load('./assets/PNG/Bg1/ground.png').convert() #Carrega o chão

    def run(self):
        running = True
        while running:
            menu = Menu(self.window)
            menu_return = menu.run()
            if menu_return == MENU_OPTION[0]:
                level = Level()
                level.run()
            elif menu_return == MENU_OPTION[1]:
                pygame.quit()
                sys.exit()