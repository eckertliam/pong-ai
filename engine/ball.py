from typing import Tuple
import numpy as np
from pyglet.shapes import Circle
from pyglet.graphics import Batch

class Ball:
    def __init__(self, radius: float, x: float, y: float, speed: float, color: Tuple[int, int, int], batch: Batch):
        self.radius = radius
        self.pos = np.array([x, y])
        self.direction = np.array([np.random.choice([-1, 1]), np.random.choice([-1, 1])])
        self.speed = np.float64(0)
        self.boost = np.array([0, 0])
        self.color = color
        self.shape = Circle(x, y, radius, color=color, batch=batch)
        
    def update_position(self, dt: float):
        self.pos = np.add(self.pos, np.multiply(self.direction, (self.speed + self.boost) * dt))
        if self.boost[0] > 0:
            self.boost[0] -= dt
        if self.boost[1] > 0:
            self.boost[1] -= dt
        
    def update_shape(self):
        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]
        self.shape.radius = self.radius
        self.shape.color = self.color
        
    def update(self, dt: float):
        self.update_position(dt)
        self.update_shape()
