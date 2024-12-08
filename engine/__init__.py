from engine.paddle import Paddle
from engine.ball import Ball


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
            vel=(0, 1),
            color=BLUE
        )
        self.paddle = Paddle(
            x=width/2,
            y=height-10,
            width=10,
            height=100,
            color=BLACK
        )

    def update(self, dt: float):
        """Update game state.
        
        Args:
            dt (float): Time step delta
        """
        self.ball.update(dt)
        self.paddle.update(dt)
        self.ball.intersect_bounds(self.width)
        self.paddle.intersect_bounds(self.width)
        if self.paddle.intersect_ball(self.ball):
            # Bounce ball off paddle
            self.ball.vel[1] = -self.ball.vel[1]
            # Give ball some of paddle's velocity
            # give ball some spin
            self.ball.jerk = -self.ball.jerk * 0.33
            # take some energy out of paddle
            self.paddle.vel[0] = self.paddle.vel[0] * 0.8
            # add some energy to ball
            self.ball.vel[0] = self.ball.vel[0] * 1.1

    def is_game_over(self):
        """Check if game is over.

        Game is over is ball gets past paddle.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        # TODO: refine this
        return self.ball.pos[1] > self.paddle.pos[1]
