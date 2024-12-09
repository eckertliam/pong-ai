from typing import Tuple
import numpy as np
from pyglet.shapes import Rectangle

class Paddle:
    """A paddle class representing a movable rectangular paddle in a game.
    
    The paddle has physics-based movement with position, velocity, acceleration, and jerk.
    It can interact with balls and screen boundaries.
    
    Attributes:
        pos (np.ndarray): 2D position vector [x, y]
        vel (np.ndarray): 2D velocity vector [vx, vy]
        acc (np.ndarray): 2D acceleration vector [ax, ay]
        jerk (np.float64): Rate of change of acceleration (negative value causes deceleration)
        width (float): Width of the paddle
        height (float): Height of the paddle
        color (Tuple[int, int, int]): RGB color tuple
    """

    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int]):
        """Initialize a paddle with given position and dimensions.

        Args:
            x (float): Initial x position
            y (float): Initial y position
            width (float): Paddle width
            height (float): Paddle height
            color (Tuple[int, int, int]): RGB color tuple
        """
        self.pos = np.array([x, y])
        self.vel = np.array([0, 0])
        self.acc = np.array([0, 0])
        self.jerk = np.float64(-1)
        self.width = width
        self.height = height
        self.color = color
    
    def update_acceleration(self, dt: float):
        """Update paddle acceleration based on jerk.
        
        Args:
            dt (float): Time step delta
        """
        self.acc = np.add(self.acc, np.multiply(self.jerk, dt))
        # Prevent negative acceleration
        if self.acc[0] < 0:
            self.acc[0] = 0
        if self.acc[1] < 0:
            self.acc[1] = 0

    def update_velocity(self, dt: float):
        """Update paddle velocity based on acceleration.
        
        Args:
            dt (float): Time step delta
        """
        self.vel = np.add(self.vel, np.multiply(self.acc, dt))
        
    def update_position(self, dt: float):
        """Update paddle position based on velocity.
        
        Args:
            dt (float): Time step delta
        """
        self.pos = np.add(self.pos, np.multiply(self.vel, dt))
        
    def update(self, dt: float):
        """Update paddle physics (acceleration, velocity, position).
        
        Args:
            dt (float): Time step delta
        """
        self.update_acceleration(dt)
        self.update_velocity(dt)
        self.update_position(dt)
        
    def _contains(self, point: np.ndarray) -> bool:
        """Check if a point is inside the paddle's rectangle.

        Args:
            point (np.ndarray): 2D point coordinates [x, y]

        Returns:
            bool: True if point is inside paddle, False otherwise
        """
        return (
            point[0] >= self.pos[0] and
            point[0] <= self.pos[0] + self.width and
            point[1] >= self.pos[1] and
            point[1] <= self.pos[1] + self.height
        )
        
    def to_pyglet(self) -> Rectangle:
        return Rectangle(self.pos[0], self.pos[1], self.width, self.height, color=self.color)
