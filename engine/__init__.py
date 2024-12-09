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
        
def paddle_intersect_bounds(paddle: Paddle, width: int) -> None:
    if paddle.pos[0] < 0:
        # collide with left boundary
        paddle.pos[0] = 0
        paddle.vel[0] = -paddle.vel[0]
        paddle.acc[0] = 0
    elif paddle.pos[0] + paddle.width > width:
        # collide with right boundary
        paddle.pos[0] = width - paddle.width
        paddle.vel[0] = -paddle.vel[0]
        paddle.acc[0] = 0
        
def ball_intersect_paddle(ball: Ball, paddle: Paddle) -> None:
    # a buffer to prevent visual overlap
    buffer = 5
    
    # calculate the bottom of the ball and the top of the paddle
    ball_bottom = np.subtract(ball.pos, np.array([0, ball.radius]))
    paddle_top = np.add(paddle.pos[1], paddle.height)
    
    # check if the ball is within the paddle's x bounds
    x_overlap = (ball.pos[0] + ball.radius > paddle.pos[0]) and (ball.pos[0] - ball.radius < paddle.pos[0] + paddle.width)
    
    # check if the ball is within the paddle's y bounds
    y_overlap = ball_bottom[1] < (paddle_top + buffer)
    
    # if the ball is within the paddle's x and y bounds, bounce off the paddle
    if x_overlap and y_overlap:
        ball.vel[1] = -ball.vel[1]
        ball.acc[1] = 0


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

    def __init__(self, width: int, height: int):
        """Initialize game engine with screen dimensions.

        Args:
            width (int): Screen width
            height (int): Screen height
        """
        self.width = width
        self.height = height
        self.ball = Ball(
            radius=10,
            x=width/2,
            y=height/2,
            vel=(0, 400),
            color=BLUE
        )
        self.paddle = Paddle(
            x=width/2,
            y=(height - 200) / 4,
            width=100,
            height=10,
            color=WHITE
        )

    def update(self, dt: float):
        """Update game state.
        
        Args:
            dt (float): Time step delta
        """
        self.ball.update(dt)
        self.paddle.update(dt)
        ball_intersect_bounds(self.ball, self.width, self.height)
        paddle_intersect_bounds(self.paddle, self.width)
        ball_intersect_paddle(self.ball, self.paddle)
        
    def is_game_over(self):
        """Check if game is over.

        Game is over is ball gets past paddle.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        # TODO: refine this
        return self.ball.pos[1] > self.paddle.pos[1]



if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600

    engine = Engine(WIDTH, HEIGHT)

    window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

    @window.event
    def on_draw():
        window.clear()
        ball_shape = engine.ball.to_pyglet()
        paddle_shape = engine.paddle.to_pyglet()
        ball_shape.draw()
        paddle_shape.draw()
    

    def update(dt: float):
        engine.update(dt)
        
    pyglet.clock.schedule_interval(update, 1/60)

    pyglet.app.run()

