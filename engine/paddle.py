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
        move_incr (np.float64): Amount to increment acc by per move
        decel_rate (float): Deceleration rate
        width (float): Width of the paddle
        height (float): Height of the paddle
        color (Tuple[int, int, int]): RGB color tuple
        max_acc (np.float64): Maximum acceleration
        min_acc (np.float64): Minimum acceleration
        max_vel (np.float64): Maximum velocity
        min_vel (np.float64): Minimum velocity
    """

    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int], max_acc: float, min_acc: float, max_vel: float, min_vel: float, decel_rate: float, move_incr: float):
        """Initialize a paddle with given position and dimensions.

        Args:
            x (float): Initial x position
            y (float): Initial y position
            width (float): Paddle width
            height (float): Paddle height
            color (Tuple[int, int, int]): RGB color tuple
            max_acc (float): Maximum acceleration
            min_acc (float): Minimum acceleration
            max_vel (float): Maximum velocity
            min_vel (float): Minimum velocity
            decel_rate (float): Deceleration rate
            move_incr (float): Amount to increment acc by per move
        """
        self.pos = np.array([x, y])
        self.vel = np.float64(0)
        self.acc = np.float64(0)
        self.max_acc = np.float64(max_acc)
        self.min_acc = np.float64(min_acc)
        self.max_vel = np.float64(max_vel)
        self.min_vel = np.float64(min_vel)
        self.decel_rate = np.abs(np.float64(decel_rate))
        self.move_incr = np.float64(move_incr)
        self.width = width
        self.height = height
        self.color = color

    def update_acceleration(self, dt: float):
        """Update paddle acceleration based on decel_rate.
        
        Args:
            dt (float): Time step delta
        """
        # calc the decel to apply
        decel = np.multiply(self.decel_rate, dt)
        
        # apply the decel to the x and y acc based on the sign of the acc
        self.acc = np.add(self.acc, np.multiply(decel, np.negative(np.sign(self.acc))))
        
        # ensure the acc is within the min and max acc
        self.acc = np.maximum(np.minimum(self.acc, self.max_acc), self.min_acc)
        

    def update_velocity(self, dt: float):
        """Update paddle velocity based on acceleration.
        
        Args:
            dt (float): Time step delta
        """
        # apply the acc to the vel
        self.vel = np.add(self.vel, np.multiply(self.acc, dt))
        
        # ensure the vel is within the min and max vel
        self.vel = np.maximum(np.minimum(self.vel, self.max_vel), self.min_vel)
        
    def update_position(self, dt: float):
        """Update paddle position based on velocity.
        
        Args:
            dt (float): Time step delta
        """
        self.pos[1] = np.add(self.pos[1], np.multiply(self.vel, dt))
        
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

    def move_up(self, dt: float):
        self.acc = np.subtract(self.acc, self.move_incr)
        
    def move_down(self, dt: float):
        self.acc = np.add(self.acc, self.move_incr)
