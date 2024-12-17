from typing import Tuple, Optional
import numpy as np
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch

class Paddle:
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int], speed: float, batch: Batch):
        self.pos = np.array([x, y])
        # direction of the paddle 0 = still, 1 = down, -1 = up
        self.direction = np.float64(1)
        # speed of the paddle
        self.speed = np.float64(speed)
        # boost of the paddle
        self.boost = np.float64(0)
        self.width = width
        self.height = height
        self.color = color
        self.shape = Rectangle(x, y, width, height, color=color, batch=batch)
        
    def update_position(self, dt: float):
        self.pos[1] += dt * (self.speed + self.boost) * self.direction
        if self.boost > 0:
            self.boost -= dt
        
    def update(self, dt: float):
        self.update_position(dt)
        self.update_shape()
        
    def update_shape(self):
        self.shape.x = self.pos[0]
        self.shape.y = self.pos[1]

    def move_up(self):
        self.direction = -1

    def move_down(self):
        self.direction = 1
        
    def stop(self):
        self.direction = 0



class AiPaddle(Paddle):
    # TODO: reimplement this once ball physics are simplified
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
        
        
class HumanPaddle(Paddle):
    def follow_finger(self, finger_pos: Optional[Tuple[int, int]], dt: float, sensitivity: float):
        if finger_pos is None:
            return
        
        # paddle center
        center_y = (self.pos[1] + (self.height / 2))
        
        if finger_pos[1] < center_y - sensitivity:
            self.move_up(dt)
        elif finger_pos[1] > center_y + sensitivity:
            self.move_down(dt)
        else:
            # stop moving the paddle
            self.stop()
        
    def update(self, dt: float, finger_pos: Optional[Tuple[int, int]], sensitivity: float):
        super().update(dt)
        self.follow_finger(finger_pos, dt, sensitivity)