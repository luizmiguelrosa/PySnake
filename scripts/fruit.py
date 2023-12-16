from engine.classes import Entity
from engine import pygame, WIDTH, HEIGHT
from engine.colors import LIGHT_RED

class Fruit(Entity):
    def __init__(self, mask: str, x: float, y: float, w: float, h: float):
        super().__init__(mask, x, y)
        self.w, self.h = w, h
    
    def update(self):
        collide = self.collision["Snake"]
        if collide:
            collide.snake.hit_fruit(collide)
            self.destroy()

        self.element = pygame.draw.rect(self.screen, LIGHT_RED, (self.x, self.y, self.w, self.h), 0, 10)