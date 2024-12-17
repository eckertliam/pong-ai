from typing import Tuple
import numpy as np
from pyglet.shapes import Circle
from pyglet.graphics import Batch

BALL_RADIUS_RATIO = 0.05

BALL_SPEED_RATIO = 0.1
BALL_COLOR = (255, 105, 180)

class Ball:
    def __init__(self, screen_width: int, screen_height: int, batch: Batch):
        x = screen_width / 2
        y = screen_height / 2
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.radius = screen_width * BALL_RADIUS_RATIO
        self.pos = np.array([x, y])
        self.direction = np.array([np.random.choice([-1, 1]), np.random.choice([-1, 1])])
        self.speed = np.float64(screen_width * BALL_SPEED_RATIO)
        self.boost = np.array([0, 0])
        self.color = BALL_COLOR
        self.shape = Circle(x, y, self.radius, color=self.color, batch=batch)
        
    def update_position(self, dt: float):
        self.pos += self.direction * (self.speed + self.boost) * dt
        if self.boost[0] > 0:
            self.boost[0] -= dt
        if self.boost[1] > 0:
            self.boost[1] -= dt
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.direction[0] = -self.direction[0]
        elif self.pos[0] > self.screen_width:
            self.pos[0] = self.screen_width
            self.direction[0] = -self.direction[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.direction[1] = -self.direction[1]
        elif self.pos[1] > self.screen_height:
            self.pos[1] = self.screen_height
            self.direction[1] = -self.direction[1]
        
    def update_shape(self):
        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]
        self.shape.radius = self.radius
        self.shape.color = self.color
        
    def update(self, dt: float):
        self.update_position(dt)
        self.update_shape()

    def reset(self):
        self.pos = np.array([self.screen_width / 2, self.screen_height / 2])
        self.direction = np.array([np.random.choice([-1, 1]), np.random.choice([-1, 1])])
        self.boost = np.array([0, 0])
        self.update_shape()

    def check_scored(self, screen_width: int) -> int:
        # left wins -1, right wins 1, no score 0
        ball_left = self.pos[0] - self.radius
        ball_right = self.pos[0] + self.radius
        if ball_left <= 0:
            return 1
        elif ball_right >= screen_width:
            return -1
        else:
            return 0
