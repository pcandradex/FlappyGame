import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from Const import WIN_WIDTH, WIN_HEIGHT, GRAVITY, P_SPAWN, PIPE_HEIGHT, C_YELLOW, P_FLAP


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def load_high_score():
    try:
        with open("score.txt", "r") as file:
            content = file.read().strip()
            return int(content) if content.isdigit() else 0
    except (FileNotFoundError, ValueError):
        return 0


class Level:
    def __init__(self):
        self.score = 0
        self.high_score = load_high_score()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load('./assets/PNG/Bg1/Bg1-all.png').convert()
        self.ground_img = pygame.image.load('./assets/PNG/Bg1/ground.png').convert()
        self.ground_scr = 0

        self.player0 = pygame.image.load('./assets/PNG/Player/Player0.png').convert_alpha()
        self.player1 = pygame.image.load('./assets/PNG/Player/Player1.png').convert_alpha()
        self.player2 = pygame.image.load('./assets/PNG/Player/Player2.png').convert_alpha()
        self.player3 = pygame.image.load('./assets/PNG/Player/Player3.png').convert_alpha()
        self.player4 = pygame.image.load('./assets/PNG/Player/Player4.png').convert_alpha()
        self.player_frames = [self.player0, self.player1, self.player2, self.player3, self.player4]
        self.player_start = 0
        self.player = self.player_frames[self.player_start]
        pygame.time.set_timer(P_FLAP, 200)
        self.player_rect = self.player.get_rect(center=(300, WIN_HEIGHT / 2))

        self.flap_sound = pygame.mixer.Sound('./assets/SOUNDS/sfx_wing.wav')
        self.death_sound = pygame.mixer.Sound('./assets/SOUNDS/sfx_hit.wav')
        self.fall_sound = pygame.mixer.Sound('./assets/SOUNDS/sfx_die.wav')
        self.score_sound = pygame.mixer.Sound('./assets/SOUNDS/sfx_score.wav')
        self.score_count = 100

        self.p_movement = 0
        self.pipe_surf = pygame.image.load('./assets/PNG/Bg1/pipe.png')
        self.pipes_list = []
        pygame.time.set_timer(P_SPAWN, 1500)
        self.game_over = False
        self.gfont = pygame.font.SysFont(name="Lucida Sans Typewriter", size=40)
        self.loss = pygame.image.load('./assets/PNG/Bg1/gameover.png').convert_alpha()
        self.loss_rect = self.loss.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

    def create_pipe(self):
        random_pipe_pos = random.choice(PIPE_HEIGHT)
        bottom_pipe = self.pipe_surf.get_rect(midtop=(900, random_pipe_pos))
        top_pipe = self.pipe_surf.get_rect(midbottom=(900, random_pipe_pos - 150))  # Espaço entre pipes
        return bottom_pipe, top_pipe

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 800:
                self.window.blit(self.pipe_surf, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surf, False, True)
                self.window.blit(flip_pipe, pipe)

    def collision(self, pipes):
        for pipe in pipes:
            if self.player_rect.colliderect(pipe):
                self.death_sound.play()
                return False
        if self.player_rect.top <= 0 or self.player_rect.bottom >= 768:
            self.fall_sound.play()
            return False
        return True

    def rotate_player(self, player):
        return pygame.transform.rotozoom(player, -self.p_movement * 3, 1)

    def score_display(self, game_state):
        if game_state == 'game':
            score_surf = self.gfont.render(str(int(self.score)), True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(WIN_WIDTH / 2, 100))
            self.window.blit(score_surf, score_rect)
        elif game_state == 'game_over':
            score_surf = self.gfont.render(f'Score: {int(self.score)}', True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(WIN_WIDTH / 2, 100))
            self.window.blit(score_surf, score_rect)

            high_score_surf = self.gfont.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_surf.get_rect(center=(WIN_WIDTH / 2, 700))
            self.window.blit(high_score_surf, high_score_rect)

    def save_high_score(self):
        with open("score.txt", "w") as file:
            file.write(str(self.high_score))

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = int(self.score)
            self.save_high_score()

    def reset_game(self):
        self.update_high_score()  # Atualiza antes de reiniciar
        self.game_over = False
        self.pipes_list.clear()
        self.player_rect.center = (300, WIN_HEIGHT / 2)
        self.p_movement = 0
        self.score = 0

    def player_animation(self):
        self.player_start = (self.player_start + 1) % len(self.player_frames)  # Alterna entre os frames
        new_player = self.player_frames[self.player_start]
        new_player_rect = new_player.get_rect(center=self.player_rect.center)  # Mantém a posição central correta
        return new_player, new_player_rect

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.update_high_score()  # Salva o high_score ao sair
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.p_movement = -6
                        self.flap_sound.play()
                    elif event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()  # Reinicia corretamente
                    elif event.key == pygame.K_x:
                        self.update_high_score()
                        running = False
                        pygame.quit()
                        sys.exit()

                if event.type == P_SPAWN:
                    self.pipes_list.extend(self.create_pipe())
                if event.type == P_FLAP:
                    self.player, self.player_rect = self.player_animation()

            self.window.blit(self.background, (0, 0))

            if not self.game_over:
                self.p_movement += GRAVITY
                self.player_rect.centery += self.p_movement
                self.window.blit(self.rotate_player(self.player), self.player_rect)
                self.game_over = not self.collision(self.pipes_list)
                self.pipes_list = move_pipes(self.pipes_list)
                self.draw_pipes(self.pipes_list)
                self.score += 0.01
                self.score_display('game')
                self.score_count -= 1
                if self.score_count <= 0:
                    self.score_sound.play()
                    self.score_count = 100
                self.window.blit(self.ground_img, (self.ground_scr, 768))
                self.window.blit(self.ground_img, (self.ground_scr + WIN_WIDTH, 768))
                self.ground_scr -= 1
                if self.ground_scr <= -431:
                    self.ground_scr = 0

            else:
                self.window.blit(self.loss, self.loss_rect)
                self.lose_text(50, 'APERTE ESPAÇO PARA JOGAR', C_YELLOW, (WIN_WIDTH / 2, 250))
                self.lose_text(50, 'APERTE X PARA SAIR', C_YELLOW, (WIN_WIDTH / 2, 350))
                self.score_display('game_over')

            pygame.display.flip()
            clock.tick(60)

    def lose_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
