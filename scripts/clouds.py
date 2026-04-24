import random

import pygame

class Cloud:
    def __init__(self, pos: tuple[float, float], img: pygame.Surface, speed: float, depth: float) -> None:
        self.pos: list[float] = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self) -> None:
        self.pos[0] += self.speed

    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (
            render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(),
            render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()
        ))


class Clouds:
    def __init__(self, cloud_images: list[pygame.Surface], count: int = 20) -> None:
        self.clouds: list[Cloud] = []

        for i in range(count):
            self.clouds.append(Cloud(
                (random.random() * 99999, random.random() * 99999),
                random.choice(cloud_images),
                random.random() * 0.02 + 0.02,
                random.random() * 0.4 + 0.2
            ))

        self.clouds.sort(key=lambda x: x.depth)

    def update(self) -> None:
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
