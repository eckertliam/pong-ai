from typing import Tuple, Optional
import numpy as np
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from enum import Enum, auto

class Side(Enum):
    LEFT = auto()
    RIGHT = auto()

PADDLE_WIDTH_RATIO = 0.02
PADDLE_HEIGHT_RATIO = 0.2

PADDLE_SPEED_RATIO = 0.5
PADDLE_SIDE_BUFFER = 0.05

class Paddle:
    def __init__(self, side: Side, screen_width: int, screen_height: int, color: Tuple[int, int, int], batch: Batch):
        self.width = screen_width * PADDLE_WIDTH_RATIO
        self.height = screen_height * PADDLE_HEIGHT_RATIO
        if side == Side.LEFT:
            x = screen_width * PADDLE_SIDE_BUFFER
        else:
            x = screen_width - (screen_width * PADDLE_SIDE_BUFFER) - self.width
        y = screen_height / 2 - self.height / 2
        self.pos = np.array([x, y])
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.speed = np.float64(screen_height * PADDLE_SPEED_RATIO)
        # direction of the paddle 0 = still, 1 = down, -1 = up
        self.direction = np.float64(0)
        self.boost = np.float64(0)
        self.color = color
        self.shape = Rectangle(x, y, self.width, self.height, color=self.color, batch=batch)
        self.origin = np.array([x, y])
        
    def update_position(self, dt: float):
        self.pos[1] += dt * (self.speed + self.boost) * self.direction
        # decrement boost by dt if it is greater than 0
        if self.boost > 0:
            self.boost -= dt
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.direction = -self.direction
        elif self.pos[1] + self.height > self.screen_height:
            self.pos[1] = self.screen_height - self.height
            self.direction = -self.direction

    def update(self, dt: float):
        self.update_position(dt)
        self.update_shape()
        
    def update_shape(self):
        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]

    def move_up(self):
        self.direction = -1

    def move_down(self):
        self.direction = 1
        
    def stop(self):
        self.direction = 0

    def reset(self):
        self.pos = self.origin
        self.direction = 0
        self.boost = 0



class AiPaddle(Paddle):
    def move_towards(self, ball_pos: np.ndarray):
        # center of the paddle
        center_y = (self.pos[1] + (self.height / 2))
        
        # move the paddle towards the ball
        if ball_pos[1] < center_y:
            self.move_up()
        elif ball_pos[1] > center_y:
            self.move_down()
        else:
            self.stop()

    def update(self, dt: float, ball_pos: np.ndarray):
        self.move_towards(ball_pos)
        super().update(dt)
        
        
class HumanPaddle(Paddle):
    def follow_finger(self, finger_pos: Optional[Tuple[int, int]], dt: float):
        if finger_pos is None:
            return
        
        # paddle center
        center_y = (self.pos[1] + (self.height / 2))
        
        if finger_pos[1] < center_y:
            self.move_up()
        elif finger_pos[1] > center_y:
            self.move_down()
        else:
            # stop moving the paddle
            self.stop()
        
    def update(self, dt: float, finger_pos: Optional[Tuple[int, int]]):
        self.follow_finger(finger_pos, dt)
        super().update(dt)
        