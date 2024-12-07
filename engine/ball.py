from dataclasses import dataclass, field
from typing import Tuple, List
import numpy as np

@dataclass
class Ball:
    radius: float
    # [x, y]
    pos: np.ndarray
    # [vx, vy] velocity - change in position
    vel: np.ndarray
    # [ax, ay] acceleration - change in velocity
    acc: np.ndarray
    # scalar (CONSTANT) jerk - change in acceleration
    # acceleration is constantly decreasing and is incremented when the ball hits a paddle
    jerk: np.float64 = field(default=-1)
    # [r, g, b] color
    color: Tuple[int, int, int]
    
    def __init__(self, radius: float, pos: List[float], vel: List[float], color: Tuple[int, int, int]):
        self.radius = radius
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array([0, 0])
        self.jerk = np.float64(-1)
        self.color = color

    def update_acceleration(self, dt: float):
        self.acc += self.jerk * dt
        if self.acc[0] < 0:
            self.acc[0] = 0
        if self.acc[1] < 0:
            self.acc[1] = 0

    def update_velocity(self, dt: float):
        self.vel += self.acc * dt
        
    def update_position(self, dt: float):
        self.pos += self.vel * dt
        
    def update(self, dt: float):
        self.update_acceleration(dt)
        self.update_velocity(dt)
        self.update_position(dt)