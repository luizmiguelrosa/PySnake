from engine import Scene, WIDTH, HEIGHT, pygame
from scripts import *
from time import perf_counter
from random import randint

class Main(Scene):
    def __init__(self, parent):
        super().__init__(parent)
    
    def create(self):
        self.paused = False
        self.snake = self.create_object("Snake", Snake, "Snake",WIDTH / 2, HEIGHT / 2)
        self.snake.create()
    
    def create_fruit(self):
        x, y = randint(round(self.snake.w), WIDTH - round(self.snake.w)), randint(round(self.snake.h), HEIGHT - round(self.snake.h))
        if self.get_total_objects_by_mask("Fruit") == 0 and not self.snake_in_position(x, y):
            self.create_object("Fruit", Fruit, "Fruit", x, y, self.snake.w, self.snake.h)
    
    def snake_in_position(self, x, y):
        for body in self.snake.body:
            if x - self.snake.w <= body.x <= x + self.snake.w and y - self.snake.h <= body.y <= y + self.snake.h:
                return True
        return False
    
    def update(self):
        self.create_fruit()
    
    def pause(self):
        if self.paused:
            self.pausedHud = self.create_hud_object("Paused", PausedMenu, 0, 0, 1)
    
    def game_over(self):
        self.parent.pause_scene(False)
        if self.paused:
            self.pausedHud = self.create_hud_object("Paused", GameOverMenu, 0, 0, 1)