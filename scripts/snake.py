from engine.classes import Entity
from engine import pygame, WIDTH, HEIGHT
from engine.colors import DARK_GREEN, MEDIUM_GREEN
from pygame.locals import K_a, K_d, K_w, K_s


class Snake(Entity):
    def __init__(self, mask: str, x: float, y: float):
        super().__init__(mask, x, y)
        self.hit = pygame.mixer.Sound("Assets/hit.wav")
        self.hit.set_volume(0.6)
        self.w, self.h = WIDTH / 30, HEIGHT / 30
        self.snake_velocity = (self.w + self.h) // 4
        self.init_length = 2
        self.direction = (1, 0)
        self.body = []
    
    def create(self):
        for _ in range(self.init_length):
            self.create_body() 
    
    def create_body(self):
        body = self.parent.create_object("Body", Body, "Snake", self.x, self.y, self.w, self.h, self)
        self.body.insert(0, body)
    
    def hit_fruit(self, body):
        self.x += self.direction[0] * self.w
        self.y += self.direction[1] * self.h
        self.create_body()
        self.hit.play()
    
    def process_input(self):
        if 0 < self.x <= WIDTH - self.w and 0 < self.y <= HEIGHT - self.h:
            keys = pygame.key.get_pressed()            
            if keys[K_a] and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif keys[K_d] and self.direction != (-1, 0):
                self.direction = (1, 0)
            elif keys[K_w] and self.direction != (0, 1):
                self.direction = (0, -1)
            elif keys[K_s] and self.direction != (0, -1):
                self.direction = (0, 1)
    
    def define_limit(self):
        if self.x >= WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH - self.w
        
        if self.y >= HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT - self.h
    
    def update(self):
        if not self.is_paused():
            self.body[-1].destroy()
            self.body.pop()

            self.process_input()

            self.x += self.direction[0] * self.w
            self.y += self.direction[1] * self.h

            self.define_limit()

            if len(self.body) > 1:
                collide = self.body[0].collision["Snake"]
                if collide:
                    self.parent.game_over()

            self.create_body()


class Body(Entity):
    def __init__(self, mask: str, x: float, y: float, w: float, h: float, snake: Snake):
        super().__init__(mask, x, y)
        self.w, self.h = w, h
        self.snake = snake
    
    def update(self):
        color = DARK_GREEN if self.snake.body.index(self) % 2 == 0 else MEDIUM_GREEN
        self.element = pygame.draw.rect(self.screen, color, (self.x, self.y, self.w, self.h), 0, 6)