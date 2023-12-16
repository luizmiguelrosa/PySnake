from engine import GameEngine
from scenes import Main

masks = {
    "Snake": ["Snake", "Fruit"],
    "Fruit": ["Snake"]
}

_engine = GameEngine(masks, Main)
_engine.run()