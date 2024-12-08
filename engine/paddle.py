from typing import Tuple
import numpy as np
from engine.ball import Ball
import math

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
        self.acc += self.jerk * dt
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
        self.vel += self.acc * dt
        
    def update_position(self, dt: float):
        """Update paddle position based on velocity.
        
        Args:
            dt (float): Time step delta
        """
        self.pos += self.vel * dt
        
    def update(self, dt: float):
        """Update paddle physics (acceleration, velocity, position).
        
        Args:
            dt (float): Time step delta
        """
        self.update_acceleration(dt)
        self.update_velocity(dt)
        self.update_position(dt)

    def intersect_bounds(self, width: int):
        """Handle paddle collision with screen boundaries.
        
        When the paddle hits a boundary, it bounces by reversing velocity and acceleration.

        Args:
            width (int): Screen width
        """
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] = -self.vel[0]
            self.acc[0] = -self.acc[0]
        elif self.pos[0] + self.width > width:
            self.pos[0] = width
            self.vel[0] = -self.vel[0]
            self.acc[0] = -self.acc[0]
        
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

    def intersect_ball(self, ball: Ball) -> bool:
        """Check if a ball intersects with the paddle.
        
        Uses a sophisticated collision detection that handles both rectangular
        and circular collision areas. Checks for:
        1. Ball center distance from paddle center on each axis
        2. Direct rectangular overlap
        3. Corner case circular collision
        
        Args:
            ball (Ball): Ball object to check collision with

        Returns:
            bool: True if ball intersects paddle, False otherwise
        """
        half_width: float = self.width / 2
        half_height: float = self.height / 2
        cx: float = math.fabs(ball.pos[0] - self.pos[0])
        x_dist: float = half_width + ball.radius
        if cx > x_dist:
            return False
        cy: float = math.fabs(ball.pos[1] - self.pos[1])
        y_dist: float = half_height + ball.radius
        if cy > y_dist:
            return False
        if cx <= half_width or cy <= half_height:
            return True
        # Handle corner case with circular collision check
        x_corner_dist: float = cx - half_width
        y_corner_dist: float = cy - half_height
        xcd_sqr: float = x_corner_dist * x_corner_dist
        ycd_sqr: float = y_corner_dist * y_corner_dist
        max_corner_dist: float = ball.radius * ball.radius
        return xcd_sqr + ycd_sqr <= max_corner_dist
        
