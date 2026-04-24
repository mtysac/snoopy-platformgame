import sys, os

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.button import Button

pygame.init()

new_icon = pygame.image.load('data/images/icon.png')
pygame.display.set_icon(new_icon)

SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

BG = pygame.image.load("assets/Background.png")
#add other bgs here

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play(num_players=1):

    while True:

        class Game:

            def __init__(self):
                pygame.display.set_caption("Snoopy!!!! Gameplay")
                self.screen = SCREEN
                self.display = pygame.Surface((512, 340))

                self.clock = pygame.time.Clock()

                self.movement = [False, False]
                self.movement2 = [False, False]
                self.num_players = num_players

                self.assets = {
                    'grass' : load_images('tiles/grass'),
                    'cement' : load_images('tiles/cement'),
                    'food' : load_images('food'),
                    'back' : load_images('back'),
                    'clouds': load_images('clouds'),
                    # Player 1 assets
                    'p1' : load_image('entities/player/player p1.png'),
                    'p1/idle' : Animation(load_images('entities/player/idle p1'), img_dur=1.5),
                    'p1/run' : Animation(load_images('entities/player/run p1'), img_dur=1.5),
                    'p1/jump' : Animation(load_images('entities/player/jump p1'), img_dur=2),
                    # Player 2 assets
                    'p2' : load_image('entities/player/player p2.png'),
                    'p2/idle' : Animation(load_images('entities/player/idle p2'), img_dur=1.5),
                    'p2/run' : Animation(load_images('entities/player/run p2'), img_dur=1.5),
                    'p2/jump' : Animation(load_images('entities/player/jump p2'), img_dur=2),
                }

                self.clouds = Clouds(self.assets['clouds'], count=20)

                self.player = Player(self, (80, 70), (32, 32), e_type='p1')
                self.player2 = Player(self, (150, 70), (32, 32), e_type='p2')

                self.tilemap = Tilemap(self, tile_size=32)
                self.tilemap.load('map.json')

                self.scroll = [0, 0]

            def run(self):
                pygame.mixer.music.load('data/gametime.mp3')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)

                while True:
                    self.display.fill((195, 220, 255))

                    if self.num_players == 2:
                        target_x = (self.player.rect().centerx + self.player2.rect().centerx) / 2
                        target_y = (self.player.rect().centery + self.player2.rect().centery) / 2
                    else:
                        target_x = self.player.rect().centerx
                        target_y = self.player.rect().centery

                    self.scroll[0] += (target_x - self.display.get_width() / 2 - self.scroll[0]) / 30
                    self.scroll[1] += (target_y - self.display.get_height() / 2 - self.scroll[1]) / 30
                    render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                    self.clouds.update()
                    self.clouds.render(self.display, offset=render_scroll)

                    self.tilemap.render(self.display, offset=render_scroll)

                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)

                    if self.num_players == 2:
                        self.player2.update(self.tilemap, (self.movement2[1] - self.movement2[0], 0))
                        self.player2.render(self.display, offset=render_scroll)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            # Player 1
                            if event.key == pygame.K_a:
                                self.movement[0] = True
                            if event.key == pygame.K_d:
                                self.movement[1] = True
                            if event.key == pygame.K_w:
                                self.player.velocity[1] = -4
                            # Player 2
                            if self.num_players == 2:
                                if event.key == pygame.K_LEFT:
                                    self.movement2[0] = True
                                if event.key == pygame.K_RIGHT:
                                    self.movement2[1] = True
                                if event.key == pygame.K_UP:
                                    self.player2.velocity[1] = -4
                            if event.key == pygame.K_ESCAPE:
                                main()
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_a:
                                self.movement[0] = False
                            if event.key == pygame.K_d:
                                self.movement[1] = False
                            if self.num_players == 2:
                                if event.key == pygame.K_LEFT:
                                    self.movement2[0] = False
                                if event.key == pygame.K_RIGHT:
                                    self.movement2[1] = False

                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                    pygame.display.update()
                    self.clock.tick(60)

        Game().run()

def player_select():

    while True:

        pygame.display.set_caption("Snoopy!!!! - Select Mode")
        SCREEN.fill((91, 92, 94))

        MOUSE_POS = pygame.mouse.get_pos()

        TITLE = get_font(60).render("SELECT MODE", True, "#ffffff")
        TITLE_RECT = TITLE.get_rect(center=(640, 200))
        SCREEN.blit(TITLE, TITLE_RECT)

        ONE_PLAYER = Button(image=None, pos=(640, 360),
                            text_input="1 PLAYER", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")
        TWO_PLAYER = Button(image=None, pos=(640, 490),
                            text_input="2 PLAYERS", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")
        BACK_BUTTON = Button(image=None, pos=(640, 620),
                            text_input="BACK", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")

        for button in [ONE_PLAYER, TWO_PLAYER, BACK_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONE_PLAYER.checkForInput(MOUSE_POS):
                    play(num_players=1)
                if TWO_PLAYER.checkForInput(MOUSE_POS):
                    play(num_players=2)
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    main()

        pygame.display.update()

def options():

    while True:

        pygame.display.set_caption("Controls")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((112, 161, 151))

        OPTIONS_TEXT = get_font(35).render("P1: W jump  A left  D right", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 220))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT2 = get_font(35).render("P2: ↑ jump  ← left  → right", True, "#ffaaaa")
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(640, 300))
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)

        OPTIONS_BACK = Button(image=None, pos=(1150, 90),
                            text_input="ESC", font=get_font(34), base_color="White", hovering_color="#a35c6a")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()

        pygame.display.update()

def main():

    pygame.mixer.music.load('data/startup.mp3')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

    while True:
        pygame.display.set_caption("Snoopy!!!!")
        SCREEN.fill((91, 92, 94))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(115).render("SNOOPY!!!!", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 170))

        PLAY_BUTTON = Button(image=None, pos=(640, 350),
                            text_input="START", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 480),
                            text_input="CONTROLS", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")
        QUIT_BUTTON = Button(image=None, pos=(640, 600),
                            text_input="EXIT", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_select()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()
