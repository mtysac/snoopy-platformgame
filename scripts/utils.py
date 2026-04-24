import os
from typing import Optional

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))  # makes black transparent
    return img

def load_images(path: str) -> list[pygame.Surface]:
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images: list[pygame.Surface], img_dur: float = 5, loop: bool = True) -> None:
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame: float = 0

    def copy(self) -> 'Animation':
        return Animation(self.images, self.img_duration, self.loop)

    def update(self) -> None:
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self) -> pygame.Surface:
        return self.images[int(self.frame / self.img_duration)]
