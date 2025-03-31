import sys

import pygame

from Const import WIN_WIDTH, WIN_HEIGHT

class Score:

    def __init__(self):
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load('./assets/PNG/Bg1/Bg1-all.png').convert()  # Carrega a imagem de fundo
        self.ground_img = pygame.image.load('./assets/PNG/Bg1/ground.png').convert()  # Carrega o chão
        self.ground_scr = 0
        self.window.blit(self.ground_img, (self.ground_scr, 768))

    def save(self, high_score):
        pass

    def show(self):
        self.window.blit(self.background, (0, 0))

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()