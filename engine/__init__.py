import pygame
from pygame.locals import QUIT, KEYDOWN, K_p, K_r
from engine.constants import WIDTH, HEIGHT, FPS
from engine.colors import DARK_BLACK
from engine.managers import CollisionManager, ObjectManager, HudManager
from engine.classes import Scene

class GameEngine:
    def __init__(self, masks, scene: Scene):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.masks = masks

        self.scene = scene(self)

    def reset_engine(self):
        self.hud = HudManager(self.screen, self.scene)
        self.objects = ObjectManager(self.screen, self.scene)
        self.collisions = CollisionManager(self.masks, self.objects)
        self.scene.create()
    
    def change_scene(self, new_scene):
        self.scene = new_scene(self)
        self.reset_engine()
    
    def pause_scene(self, key=True):
        self.scene.paused = not self.scene.paused
        if key:
            self.scene.pause()
        if not self.scene.paused:
            self.hud.delete_object(self.scene.pausedHud.__hash__())
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    self.pause_scene()
                elif event.key == K_r and self.scene.paused:
                    self.reset_engine()

    def update_all(self):
        self.scene.update()
        self.objects.update()
        self.collisions.update()
        self.hud.update()

    def run(self):
        self.reset_engine()
        while True:
            self.clock.tick(FPS)
            self.screen.fill(DARK_BLACK)
            self.handle_events()
            self.update_all()
            pygame.display.flip()