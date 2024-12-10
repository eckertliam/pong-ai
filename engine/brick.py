import numpy as np
from typing import Tuple

class BaseBrick:
    """Base class for all bricks.

    Attributes:
        pos (np.ndarray): Position of the brick
        width (float): Width of the brick
        height (float): Height of the brick
        color (Tuple[int, int, int]): Color of the brick
    """
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int]):
        self.pos = np.array([x, y])
        self.width = width
        self.height = height
        self.color = color


class Brick(BaseBrick):
    """Breakable brick.
    Can be destroyed by the ball and bounces the ball back.

    Attributes:
        is_broken (bool): Whether the brick is broken
    """
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int]):
        super().__init__(x, y, width, height, color)
        self.is_broken = False


class MetalBrick(BaseBrick):
    """Unbreakable brick.
    Cannot be destroyed by the ball.
    """
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int]):
        super().__init__(x, y, width, height, color)


class GlassBrick(BaseBrick):
    """Glass brick.
    Can be destroyed by the ball but does not bounce the ball back.
    
    Attributes:
        is_broken (bool): Whether the brick is broken
    """
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int]):
        super().__init__(x, y, width, height, color)
        self.is_broken = False


