from typing import Tuple
import numpy as np
from pyglet.shapes import Circle
from pyglet.graphics import Batch
class Ball:
    """A ball class representing a moving circular object in a game.
    
    The ball has physics-based movement with position, velocity, acceleration, and jerk.
    
    Attributes:
        radius (float): Radius of the ball
        pos (np.ndarray): 2D position vector [x, y]
        vel (np.ndarray): 2D velocity vector [vx, vy]
        acc (np.ndarray): 2D acceleration vector [ax, ay]
        decel_rate (float): Deceleration rate
        color (Tuple[int, int, int]): RGB color tuple
        max_acc (np.ndarray): Maximum acceleration
        min_acc (np.ndarray): Minimum acceleration
        max_vel (np.ndarray): Maximum velocity
        min_vel (np.ndarray): Minimum velocity
        shape (pyglet.shapes.Circle): Pyglet circle shape
    """

    def __init__(self, radius: float, x: float, y: float, vel: Tuple[float, float], color: Tuple[int, int, int], max_acc: float, min_acc: float, max_vel: float, min_vel: float, decel_rate: float, batch: Batch):
        """Initialize a ball with given position, velocity, and appearance.

        Args:
            radius (float): Ball radius
            x (float): Initial x position
            y (float): Initial y position
            vel (Tuple[float, float]): Initial velocity vector (vx, vy)
            color (Tuple[int, int, int]): RGB color tuple
            max_acc (float): Maximum acceleration
            min_acc (float): Minimum acceleration
            max_vel (float): Maximum velocity
            min_vel (float): Minimum velocity
            decel_rate (float): Deceleration rate
            batch (pyglet.graphics.Batch): Batch for drawing
        """
        self.radius = radius
        self.pos = np.array([x, y])
        self.vel = np.array(vel)
        self.acc = np.array([0, 0])
        self.color = color
        self.max_acc = np.array([max_acc, max_acc])
        self.min_acc = np.array([min_acc, min_acc])
        self.max_vel = np.array([max_vel, max_vel])
        self.min_vel = np.array([min_vel, min_vel])
        self.decel_rate = np.abs(np.float64(decel_rate))
        self.shape = Circle(x, y, radius, color=color, batch=batch)
    def update_acceleration(self, dt: float):
        """Update ball acceleration based on decel_rate.
        
        Args:
            dt (float): Time step delta
        """
        # calc the decel to apply
        decel = np.power(self.decel_rate, dt)
        
        # apply the decel to the x and y acc
        self.acc = np.multiply(self.acc, decel)
        
        # ensure the acc is within the min and max acc
        self.acc = np.maximum(np.minimum(self.acc, self.max_acc), self.min_acc)
        
    def update_velocity(self, dt: float):
        """Update ball velocity based on acceleration.
        
        Args:
            dt (float): Time step delta
        """
        # apply the acc to the vel
        self.vel = np.add(self.vel, np.multiply(self.acc, dt))
        
        # ensure the vel is within the min and max vel
        self.vel = np.maximum(np.minimum(self.vel, self.max_vel), self.min_vel)
        
    def update_position(self, dt: float):
        """Update ball position based on velocity.
        
        Args:
            dt (float): Time step delta
        """
        self.pos = np.add(self.pos, np.multiply(self.vel, dt))
        
    def update_shape(self):
        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]
        self.shape.radius = self.radius
        self.shape.color = self.color
        
    def update(self, dt: float):
        """Update ball physics (acceleration, velocity, position).
        
        Args:
            dt (float): Time step delta
        """
        self.update_acceleration(dt)
        self.update_velocity(dt)
        self.update_position(dt)
        self.update_shape()
