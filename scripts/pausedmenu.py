from engine.classes import Hud
from engine import WIDTH, HEIGHT
from engine.colors import WHITE
from engine.fonts import ARIAL

class PausedMenu(Hud):
    def __init__(self, x: float, y: float, z_index: int):
        super().__init__(x, y, z_index)
        
    def update(self):
        self.drawStart()

    def drawStart(self):
        start_label = ARIAL.render(f"Paused (Press P)", True, WHITE)
        rect_label = start_label.get_rect()
        rect_label.center = (WIDTH/2, HEIGHT/2)
        
        self.screen.blit(start_label, rect_label)