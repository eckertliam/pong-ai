from dataclasses import dataclass
from typing import Tuple
import numpy as np

@dataclass
class Paddle:
    pos: np.ndarray
    vel: np.ndarray
    acc: np.ndarray
    jerk: np.float64
    width: float
    height: float
    color: Tuple[int, int, int]
    
    def move(self, delta_time: float):
        self.x += self.speed * delta_time
        
    
        
    