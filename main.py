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

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():

    while True:

        class Game:

            def __init__(self):
                pygame.display.set_caption("Snoopy!!!! Gameplay")
                self.screen = SCREEN # used to be pygame.display.set_mode((1280, 720), pygame.RESIZABLE) # og coords is 640, 480
                self.display = pygame.Surface((512, 340)) # converted

                self.clock = pygame.time.Clock()

                self.movement = [False, False]

                self.assets = { # add all pngs used here !!! btw check if images or image is typed
                    'grass' : load_images('tiles/grass'),
                    'cement' : load_images('tiles/cement'),
                    'food' : load_images('food'),
                    'back' : load_images('back'),
                    'player' : load_image('entities/player/player.png'),
                    'clouds': load_images('clouds'),
                    'player/idle' : Animation(load_images('entities/player/idle'), img_dur=1.5),
                    'player/run' : Animation(load_images('entities/player/run'), img_dur=1.5),
                    'player/jump' : Animation(load_images('entities/player/jump'), img_dur=2),
                }

                self.clouds = Clouds(self.assets['clouds'], count=20)

                self.player = Player(self, (80, 70), (32, 32)) #2nd x y og was 8,15 // 2nd x and y must be able to divide the x and y of display

                self.tilemap = Tilemap(self, tile_size = 32)
                self.tilemap.load('map.json')

                self.scroll = [0, 0]

            def run(self):
                pygame.mixer.music.load('data/gametime.mp3')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1) # -1 means loop forever

                while True:
                    self.display.fill((195, 220, 255)) # rgb colour coordinates

                    self.scroll[0] +=(self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                    self.scroll[1] +=(self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                    render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                    self.clouds.update()
                    self.clouds.render(self.display, offset=render_scroll)
                    
                    
                    self.tilemap.render(self.display, offset=render_scroll)

                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a:
                                self.movement[0] = True
                            if event.key == pygame.K_d:
                                self.movement[1] = True
                            if event.key == pygame.K_w:  # JUMP NOT WORKING GRAVITY NOT WORKING NOOOO
                                self.player.velocity[1] = -4
                            if event.key == pygame.K_ESCAPE:
                                main()
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_a:
                                self.movement[0] = False
                            if event.key == pygame.K_d:
                                self.movement[1] = False
                            if event.key == pygame:
                                self.player.velocity[1] = False
                        
                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                    pygame.display.update()
                    self.clock.tick(60)

        Game().run()

def options():

    while True:

        pygame.display.set_caption("Controls")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((112, 161, 151))#for image bg use SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(50).render("W jump, A left, D right", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

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
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()

def main():

    pygame.mixer.music.load('data/startup.mp3')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1) # -1 means loop forever

    while True:
        pygame.display.set_caption("Snoopy!!!!")
        SCREEN.fill((91, 92, 94))
        #SCREEN.blit(BG, (0, 0)) was this originally

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(115).render("SNOOPY!!!!", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 170))

        PLAY_BUTTON = Button(image=None, pos=(245, 350), #used to be y480, switched w options
                            text_input="START", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")
        OPTIONS_BUTTON = Button(image=None, pos=(330, 480), #used to be y350
                            text_input="CONTROLS", font=get_font(60), base_color="#e7e4e4", hovering_color="#a35c6a")
        QUIT_BUTTON = Button(image=None, pos=(217, 600), 
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
                    pygame.quit
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
if __name__ == "__main__":
    main()