from paddle import AiPaddle, Paddle
from ball import Ball
import numpy as np
import pyglet
from random import randint
from typing import Tuple

BOUND_SLOWDOWN_FACTOR = 0.6

def ball_intersect_bounds(ball: Ball, width: int, height: int) -> None:
    if ball.pos[0] - ball.radius < 0:
        # bounce off left boundary
        ball.pos[0] = ball.radius + 1
        ball.vel[0] = -ball.vel[0] * BOUND_SLOWDOWN_FACTOR
        ball.acc[0] = 0
    elif ball.pos[0] + ball.radius > width:
        # bounce off right boundary
        ball.pos[0] = width - ball.radius - 1
        ball.vel[0] = -ball.vel[0] * BOUND_SLOWDOWN_FACTOR
        ball.acc[0] = 0
        
    if ball.pos[1] - ball.radius < 0:
        # bounce off top boundary
        ball.pos[1] = ball.radius + 1
        ball.vel[1] = -ball.vel[1] * BOUND_SLOWDOWN_FACTOR
        ball.acc[1] = 0
    elif ball.pos[1] + ball.radius > height:
        # bounce off bottom boundary
        ball.pos[1] = height - ball.radius - 1
        ball.vel[1] = -ball.vel[1] * BOUND_SLOWDOWN_FACTOR
        ball.acc[1] = 0
        
def paddle_intersect_bounds(paddle: Paddle, height: int) -> None:
    if paddle.pos[1] < 0:
        # collide with top boundary
        paddle.pos[1] = 0
        paddle.vel = -paddle.vel * BOUND_SLOWDOWN_FACTOR
        paddle.acc = 0
    elif paddle.pos[1] + paddle.height > height:
        # collide with bottom boundary
        paddle.pos[1] = height - paddle.height
        paddle.vel = -paddle.vel * BOUND_SLOWDOWN_FACTOR
        paddle.acc = 0
        
def ball_intersect_paddle(ball: Ball, paddle: Paddle) -> None:
    # a buffer to prevent visual overlap
    buffer = 2
    
    # calculate the ball left and right bounds
    ball_left = ball.pos[0] - ball.radius
    ball_right = ball.pos[0] + ball.radius
    
    # calc the ball top and bottom bounds
    ball_top = ball.pos[1] - ball.radius
    ball_bottom = ball.pos[1] + ball.radius
    
    # calc the paddles y range
    paddle_top = paddle.pos[1] - buffer
    paddle_bottom = paddle.pos[1] + paddle.height + buffer
    
    # calc the paddle left and right bounds
    paddle_left = paddle.pos[0] - buffer
    paddle_right = paddle.pos[0] + paddle.width + buffer
    
    # ball is within the paddle's y range
    in_y_range = ball_top < paddle_bottom and ball_bottom > paddle_top
    
    # ball is within the paddle's x range
    in_x_range = ball_left < paddle_right and ball_right > paddle_left
    
    # ball is within the paddle's y range and x range
    if in_y_range and in_x_range:
        ball.vel = np.negative(ball.vel)
        ball.acc = np.negative(ball.acc)
        # if paddle is to the left of the ball, bounce off the left side of the paddle
        if paddle.pos[0] > ball.pos[0]:
            ball.pos[0] = paddle.pos[0] - paddle.width - ball.radius
        # if paddle is to the right of the ball, bounce off the right side of the paddle
        else:
            ball.pos[0] = paddle.pos[0] + paddle.width + ball.radius
            
def check_scored(ball: Ball, screen_width: int) -> int:
    # returns 1 if player scored, 2 if ai scored, 0 if no score
    ball_left = ball.pos[0] - ball.radius - 1
    ball_right = ball.pos[0] + ball.radius + 1
    if ball_left <= 0:
        return 2
    elif ball_right >= screen_width:
        return 1
    else:
        return 0


# Define common colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PADDLE_WIDTH_RATIO = 25
PADDLE_HEIGHT_RATIO = 4

PADDLE_MOVE_INCR = 100
PADDLE_MAX_ACC = 100
PADDLE_MIN_ACC = -100
PADDLE_MAX_VEL = 1000
PADDLE_MIN_VEL = -1000
PADDLE_DECEL_RATE = 0.01

def make_paddles(screen_width: int, screen_height: int, batch: pyglet.graphics.Batch) -> Tuple[Paddle, AiPaddle]:
    paddle_width = screen_width / PADDLE_WIDTH_RATIO
    paddle_height = screen_height / PADDLE_HEIGHT_RATIO
    paddle_x = paddle_width / 2
    paddle_y = screen_height / 2 - paddle_height / 2
    player_paddle = Paddle(
        x=paddle_x,
        y=paddle_y,
        width=paddle_width,
        height=paddle_height,
        color=WHITE,
        max_acc=PADDLE_MAX_ACC,
        min_acc=PADDLE_MIN_ACC,
        max_vel=PADDLE_MAX_VEL,
        min_vel=PADDLE_MIN_VEL,
        decel_rate=PADDLE_DECEL_RATE,
        move_incr=PADDLE_MOVE_INCR,
        batch=batch
    )
    paddle_x = screen_width - paddle_width - paddle_width / 2
    ai_paddle = AiPaddle(
        x=paddle_x,
        y=paddle_y,
        width=paddle_width,
        height=paddle_height,
        color=WHITE,
        max_acc=PADDLE_MAX_ACC,
        min_acc=PADDLE_MIN_ACC,
        max_vel=PADDLE_MAX_VEL,
        min_vel=PADDLE_MIN_VEL,
        decel_rate=PADDLE_DECEL_RATE,
        move_incr=PADDLE_MOVE_INCR,
        batch=batch
    )
    return player_paddle, ai_paddle

def paddle_reset(paddle: Paddle, paddle_origin: np.ndarray):
    paddle.pos = paddle_origin
    paddle.vel = 0
    paddle.acc = 0

BALL_RADIUS_RATIO = 100

BALL_MAX_VEL = 1000
BALL_MIN_VEL = -1000
BALL_MAX_ACC = 500
BALL_MIN_ACC = -500
BALL_DECEL_RATE = 0.01
BALL_COLOR = (255, 105, 180)

def ball_reset(ball: Ball, ball_origin: np.ndarray):
    ball.pos = ball_origin
    ball.vel = (randint(BALL_MIN_VEL, BALL_MAX_VEL), randint(BALL_MIN_VEL, BALL_MAX_VEL))

def make_ball(screen_width: int, screen_height: int, batch: pyglet.graphics.Batch) -> Ball:
    ball_radius = screen_width / 25
    ball_x = screen_width / 2
    ball_y = screen_height / 2
    ball_vel = (randint(BALL_MIN_VEL, BALL_MAX_VEL), randint(BALL_MIN_VEL, BALL_MAX_VEL))
    ball = Ball(
        radius=ball_radius,
        x=ball_x,
        y=ball_y,
        vel=ball_vel,
        color=BALL_COLOR,
        max_acc=BALL_MAX_ACC,
        min_acc=BALL_MIN_ACC,
        max_vel=BALL_MAX_VEL,
        min_vel=BALL_MIN_VEL,
        decel_rate=BALL_DECEL_RATE,
        batch=batch
    )
    return ball


class Engine:
    """Main game engine class that manages game objects and updates.
    
    Attributes:
        screen_width (int): Game screen width
        screen_height (int): Game screen height
        ball (Ball): Game ball object
        player_paddle (Paddle): Player paddle object
        ai_paddle (AiPaddle): AI paddle object
        player_score (int): Player score
        ai_score (int): AI score
        in_game (bool): True if game is in progress, False otherwise used to pause game for between rounds and game over
        ball_origin (np.ndarray): Ball starting position
        player_paddle_origin (np.ndarray): Player paddle starting position
        ai_paddle_origin (np.ndarray): AI paddle starting position
    """

    def __init__(self, screen_width: int, screen_height: int, batch: pyglet.graphics.Batch):
        """Initialize game engine with screen dimensions.

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
            batch (pyglet.graphics.Batch): Batch object for rendering
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.in_game = True
        self.player_score = 0
        self.ai_score = 0
        self.ball = make_ball(self.screen_width, self.screen_height, batch)
        self.ball_origin = self.ball.pos
        self.player_paddle, self.ai_paddle = make_paddles(self.screen_width, self.screen_height, batch)
        self.player_paddle_origin = self.player_paddle.pos
        self.ai_paddle_origin = self.ai_paddle.pos
        

    def update(self, dt: float):
        """Update game state.
        
        Args:
            dt (float): Time step delta
        """
        # escape if game is not in progress
        if not self.in_game:
            return
        # check if either player scored
        scored = check_scored(self.ball, self.screen_width)
        if scored > 0:
            if scored == 1:
                self.player_score += 1
            else:
                self.ai_score += 1
            self.end_round()
            return
        # update the ball, ai paddle, and player paddle
        self.ball.update(dt)
        self.ai_paddle.update(dt, self.ball.pos, self.ball.vel)
        self.player_paddle.update(dt)
        # check for collisions with the bounds and paddles
        ball_intersect_bounds(self.ball, self.screen_width, self.screen_height)
        paddle_intersect_bounds(self.player_paddle, self.screen_height)
        paddle_intersect_bounds(self.ai_paddle, self.screen_height)
        ball_intersect_paddle(self.ball, self.player_paddle)
        ball_intersect_paddle(self.ball, self.ai_paddle)
    
    def end_round(self):
        self.in_game = False
        ball_reset(self.ball, self.ball_origin)
        paddle_reset(self.player_paddle, self.player_paddle_origin)
        paddle_reset(self.ai_paddle, self.ai_paddle_origin)

    def start_round(self):
        self.in_game = True
        
        
def run(width: int, height: int, fps: int = 60) -> None:
    # define the window
    window = pyglet.window.Window(width=width, height=height, caption="Pong AI")
    # define the batch  
    batch = pyglet.graphics.Batch()
    # define the engine
    engine = Engine(width, height, batch)
    
    # define the update function
    def update(dt: float):
        engine.update(dt)
        
    # define the draw function
    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    # schedule the update function
    pyglet.clock.schedule_interval(update, 1/fps)
    # run the window
    pyglet.app.run()
