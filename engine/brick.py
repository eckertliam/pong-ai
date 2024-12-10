from enum import Enum
import numpy as np
from typing import Dict, List, Optional, Tuple

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

class BrickType(Enum):
    BRICK = 0
    METAL_BRICK = 1
    GLASS_BRICK = 2

class BrickFactory:
    # brick distribution
    brick_types = [BrickType.BRICK, BrickType.METAL_BRICK, BrickType.GLASS_BRICK]
    brick_distribution = [0.8, 0.1, 0.1]

    def __init__(self, x_range: Tuple[float, float], y_range: Tuple[float, float]) -> None:
        # which position is occupied by a brick
        self.brick_map: np.ndarray = np.zeros((x_range[1], y_range[1]), dtype=bool)
        # the x range in which the bricks are created
        self.x_range: Tuple[float, float] = x_range
        # the y range in which the bricks are created
        self.y_range: Tuple[float, float] = y_range
        # brick width
        self.brick_width: float = 10
        # brick height
        self.brick_height: float = 10
        # space between bricks
        self.space: float = 1

    def next_position(self) -> Optional[Tuple[float, float]]:
        for i in range(self.brick_map.shape[0]):
            for j in range(self.brick_map.shape[1]):
                if not self.brick_map[i, j]:
                    self.brick_map[i, j] = True
                    return (i, j)
        return None

    def create_brick(self, brick_type: BrickType, x: float, y: float, color: Tuple[int, int, int]) -> BaseBrick:
        match brick_type:
            case BrickType.BRICK:
                return Brick(x, y, self.brick_width, self.brick_height, color)
            case BrickType.METAL_BRICK:
                return MetalBrick(x, y, self.brick_width, self.brick_height, color)
            case BrickType.GLASS_BRICK:
                return GlassBrick(x, y, self.brick_width, self.brick_height, color)
            
    def create_bricks(self, n_bricks: int) -> List[BaseBrick]:
        bricks = []
        for _ in range(n_bricks):
            brick_type = np.random.choice(self.brick_types, p=self.brick_distribution)
