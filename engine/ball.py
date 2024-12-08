from typing import Tuple, List
import numpy as np

class Ball:
    """A ball class representing a moving circular object in a game.
    
    The ball has physics-based movement with position, velocity, acceleration, and jerk.
    
    Attributes:
        radius (float): Radius of the ball
        pos (np.ndarray): 2D position vector [x, y]
        vel (np.ndarray): 2D velocity vector [vx, vy]
        acc (np.ndarray): 2D acceleration vector [ax, ay]
        jerk (np.float64): Rate of change of acceleration (negative value causes deceleration)
        color (Tuple[int, int, int]): RGB color tuple
    """

    def __init__(self, radius: float, x: float, y: float, vel: Tuple[float, float], color: Tuple[int, int, int]):
        """Initialize a ball with given position, velocity, and appearance.

        Args:
            radius (float): Ball radius
            x (float): Initial x position
            y (float): Initial y position
            vel (Tuple[float, float]): Initial velocity vector (vx, vy)
            color (Tuple[int, int, int]): RGB color tuple
        """
        self.radius = radius
        self.pos = np.array([x, y])
        self.vel = np.array(vel)
        self.acc = np.array([0, 0])
        self.jerk = np.float64(-1)
        self.color = color

    def update_acceleration(self, dt: float):
        """Update ball acceleration based on jerk.
        
        Args:
            dt (float): Time step delta
        """
        self.acc += self.jerk * dt
        # Prevent negative acceleration
        if self.acc[0] < 0:
            self.acc[0] = 0
        if self.acc[1] < 0:
            self.acc[1] = 0

    def update_velocity(self, dt: float):
        """Update ball velocity based on acceleration.
        
        Args:
            dt (float): Time step delta
        """
        self.vel += self.acc * dt
        
    def update_position(self, dt: float):
        """Update ball position based on velocity.
        
        Args:
            dt (float): Time step delta
        """
        self.pos += self.vel * dt
        
    def update(self, dt: float):
        """Update ball physics (acceleration, velocity, position).
        
        Args:
            dt (float): Time step delta
        """
        self.update_acceleration(dt)
        self.update_velocity(dt)
        self.update_position(dt)

    def intersect_bounds(self, width: int):
        """Handle ball collision with screen boundaries.
        
        When the ball hits a boundary, it bounces by reversing velocity.

        Args:
            width (int): Screen width
        """
        if self.pos[0] < 0 or self.pos[0] > width:
            self.vel[0] = -self.vel[0]
            self.acc[0] = 0
        if self.pos[1] < 0:
            self.vel[1] = -self.vel[1]
            self.acc[1] = 0
