from paddle import Paddle
from ball import Ball
import numpy as np
import pyglet

def ball_intersect_bounds(ball: Ball, width: int, height: int) -> None:
    if ball.pos[0] - ball.radius < 0:
        # bounce off left boundary
        ball.pos[0] = ball.radius
        ball.vel[0] = -ball.vel[0]
        ball.acc[0] = 0
    elif ball.pos[0] + ball.radius > width:
        # bounce off right boundary
        ball.pos[0] = width - ball.radius
        ball.vel[0] = -ball.vel[0]
        ball.acc[0] = 0
        
    if ball.pos[1] - ball.radius < 0:
        # bounce off top boundary
        ball.pos[1] = ball.radius
        ball.vel[1] = -ball.vel[1]
        ball.acc[1] = 0
    elif ball.pos[1] + ball.radius > height:
        # bounce off bottom boundary
        ball.pos[1] = height - ball.radius
        ball.vel[1] = -ball.vel[1]
        ball.acc[1] = 0
        
def paddle_intersect_bounds(paddle: Paddle, height: int) -> None:
    if paddle.pos[1] < 0:
        # collide with top boundary
        paddle.pos[1] = 0
        paddle.vel[1] = -paddle.vel[1]
        paddle.acc[1] = 0
    elif paddle.pos[1] + paddle.height > height:
        # collide with bottom boundary
        paddle.pos[1] = height - paddle.height
        paddle.vel[1] = -paddle.vel[1]
        paddle.acc[1] = 0
        
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


# Define common colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Engine:
    """Main game engine class that manages game objects and updates.
    
    Attributes:
        width (int): Game screen width
        height (int): Game screen height
        ball (Ball): Game ball object
        paddle (Paddle): Player paddle object
    """

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize game engine with screen dimensions.

        Args:
            width (int): Screen width
            height (int): Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ball = Ball(
            radius=10,
            x=self.screen_width/2,
            y=self.screen_height/2,
            vel=(100, 2),
            color=(255, 105, 180)
        )
        paddle_width = self.screen_width / 25
        paddle_height = self.screen_height / 4
        paddle_x = paddle_width / 2
        paddle_y = self.screen_height / 2 - paddle_height / 2
        self.player_paddle = Paddle(
            x=paddle_x,
            y=paddle_y,
            width=paddle_width,
            height=paddle_height,
            color=WHITE
        )

    def update(self, dt: float):
        """Update game state.
        
        Args:
            dt (float): Time step delta
        """
        self.ball.update(dt)
        self.player_paddle.update(dt)
        ball_intersect_bounds(self.ball, self.screen_width, self.screen_height)
        paddle_intersect_bounds(self.player_paddle, self.screen_width)
        ball_intersect_paddle(self.ball, self.player_paddle)
        
    def is_game_over(self):
        """Check if game is over.

        Game is over is ball gets past paddle.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        # TODO: refine this
        return self.ball.pos[1] > self.player_paddle.pos[1]



if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600

    engine = Engine(WIDTH, HEIGHT)

    window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

    @window.event
    def on_draw():
        window.clear()
        ball_shape = engine.ball.to_pyglet()
        paddle_shape = engine.player_paddle.to_pyglet()
        ball_shape.draw()
        paddle_shape.draw()
    

    def update(dt: float):
        engine.update(dt)
        
    pyglet.clock.schedule_interval(update, 1/60)

    pyglet.app.run()

