from typing import Tuple
import numpy as np
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch

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
        shape (pyglet.shapes.Rectangle): Pyglet rectangle shape
    """
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int], max_acc: float, min_acc: float, max_vel: float, min_vel: float, decel_rate: float, move_incr: float, batch: Batch):
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
            batch (pyglet.graphics.Batch): Batch for drawing
        """
        self.pos = np.array([x, y])
        self.vel = np.float64(0)
        self.acc = np.float64(0)
        self.max_acc = np.float64(max_acc)
        self.min_acc = np.float64(min_acc)
        self.max_vel = np.float64(max_vel)
        self.min_vel = np.float64(min_vel)
        self.decel_rate = np.float64(decel_rate)
        self.move_incr = np.float64(move_incr)
        self.width = width
        self.height = height
        self.color = color
        self.shape = Rectangle(x, y, width, height, color=color, batch=batch)

    def update_acceleration(self, dt: float):
        """Update paddle acceleration based on decel_rate.
        
        Args:
            dt (float): Time step delta
        """
        # calc the decel to apply
        decel = np.power(self.decel_rate, dt)
        
        # apply the decel to the acc
        self.acc = np.multiply(self.acc, decel)
        
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
        self.update_shape()
        
    def update_shape(self):
        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]
        self.shape.width = self.width
        self.shape.height = self.height

    def move_up(self, dt: float):
        self.acc = self.acc - (self.move_incr * dt)
        
    def move_down(self, dt: float):
        self.acc = self.acc + (self.move_incr * dt)



class AiPaddle(Paddle):    
    def move_towards(self, target_pos: np.ndarray, target_vel: np.ndarray, dt: float):
        # determine if the ball is moving towards the paddle
        moving_towards = target_vel[0] >= 0
        
        # center of the paddle
        center_y = (self.pos[1] + (self.height / 2))
        
        if not moving_towards:
            # center on the ball
            if target_pos[1] <= center_y:
                self.move_up(dt)
            elif target_pos[1] >= center_y:
                self.move_down(dt)
            return
        
        # determine where the ball will hit on the y axis at the paddle's x
        # y = (vy / vx) * (x - x0) + y0
        hit_y = (target_vel[1] / target_vel[0]) * (self.pos[0] - target_pos[0]) + target_pos[1]
        will_hit = hit_y >= self.pos[1] and hit_y <= self.pos[1] + self.height
        
        if will_hit:
            # if the ball will hit the paddle, do nothing
            return
        elif hit_y < center_y:
            # if the ball is above the center of the paddle, move up
            self.move_up(dt)
        elif hit_y > center_y:
            # if the ball is below the center of the paddle, move down
            self.move_down(dt)
        
    def update(self, dt: float, ball_pos: np.ndarray, ball_vel: np.ndarray):
        super().update(dt)
        # move the paddle towards the ball
        self.move_towards(ball_pos, ball_vel, dt)
        