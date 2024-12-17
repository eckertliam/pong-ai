from paddle import AiPaddle, HumanPaddle, Paddle, Side
from ball import Ball
from camera import Camera, CameraFrame
import numpy as np
import pyglet
from typing import Tuple, Optional

PADDLE_BOUNCE_BOOST = 10

def ball_intersect_paddle(ball: Ball, paddle: Paddle) -> None:
    # calculate the ball left and right bounds
    ball_left = ball.pos[0] - ball.radius
    ball_right = ball.pos[0] + ball.radius
    
    # calc the ball top and bottom bounds
    ball_top = ball.pos[1] - ball.radius
    ball_bottom = ball.pos[1] + ball.radius
    
    # calc the paddles y range
    paddle_top = paddle.pos[1]
    paddle_bottom = paddle.pos[1] + paddle.height
    
    # calc the paddle left and right bounds
    paddle_left = paddle.pos[0]
    paddle_right = paddle.pos[0] + paddle.width
    
    # ball is within the paddle's y range
    in_y_range = ball_top < paddle_bottom and ball_bottom > paddle_top
    
    # ball is within the paddle's x range
    in_x_range = ball_left < paddle_right and ball_right > paddle_left
    
    # ball is within the paddle's y range and x range
    if in_y_range and in_x_range:
        ball.direction = np.negative(ball.direction)
        ball.boost = np.array([PADDLE_BOUNCE_BOOST, PADDLE_BOUNCE_BOOST])
        # if paddle is to the left of the ball, bounce off the left side of the paddle
        if paddle.pos[0] > ball.pos[0]:
            ball.pos[0] = paddle.pos[0] - paddle.width - ball.radius
        # if paddle is to the right of the ball, bounce off the right side of the paddle
        else:
            ball.pos[0] = paddle.pos[0] + paddle.width + ball.radius


# Define common colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def make_paddles(screen_width: int, screen_height: int, batch: pyglet.graphics.Batch) -> Tuple[Paddle, AiPaddle]:
    player_paddle = HumanPaddle(
        Side.LEFT,
        screen_width,
        screen_height,
        WHITE,
        batch
    )
    ai_paddle = AiPaddle(
        Side.RIGHT,
        screen_width,
        screen_height,
        WHITE,
        batch
    )
    return player_paddle, ai_paddle


FINGER_SENSITIVITY = 10

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
        batch (pyglet.graphics.Batch): Batch object for rendering
        key_handler (pyglet.window.key.KeyStateHandler): Key handler object
        camera (Camera): Camera object
        finger_circle (pyglet.shapes.Circle): Finger circle object
        finger_history (list[Tuple[int, int]]): Past 5 finger positions
    """

    def __init__(self, screen_width: int, screen_height: int, batch: pyglet.graphics.Batch, key_handler: pyglet.window.key.KeyStateHandler):
        """Initialize game engine with screen dimensions.

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
            batch (pyglet.graphics.Batch): Batch object for rendering
            key_handler (pyglet.window.key.KeyStateHandler): Key handler object
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.in_game = True
        self.player_score = 0
        self.ai_score = 0
        self.batch = batch
        self.key_handler = key_handler
        self.ball = Ball(self.screen_width, self.screen_height, batch)
        self.ball_origin = self.ball.pos
        self.player_paddle, self.ai_paddle = make_paddles(self.screen_width, self.screen_height, batch)
        self.player_paddle_origin = self.player_paddle.pos
        self.ai_paddle_origin = self.ai_paddle.pos
        self.camera = Camera(self.screen_width, self.screen_height)
        self.finger_circle = pyglet.shapes.Circle(0, 0, 10, color=RED, batch=batch)
        # past 5 finger positions
        self.finger_history = []
        self.last_finger_pos = None
    
    def handle_camera(self) -> Optional[Tuple[int, int]]:
        # get the camera frame
        camera_frame = self.camera.capture()
        # get the finger position
        finger_pos = camera_frame.finger_coordinates
        if finger_pos:
            # add the finger position to the history
            self.finger_history.append(finger_pos)
            # keep the history to 5 positions
            if len(self.finger_history) > 5:
                self.finger_history.pop(0)
            # calculate a smoothed finger position
            self.last_finger_pos = np.mean(self.finger_history, axis=0)
            # update the finger circle position
            self.finger_circle.x = self.last_finger_pos[0]
            self.finger_circle.y = self.last_finger_pos[1]
            # return the smoothed finger position for the player paddle
            return self.last_finger_pos
        else:
            return None

    def update(self, dt: float):
        """Update game state.
        
        Args:
            dt (float): Time step delta
        """
        # escape if game is not in progress
        if not self.in_game:
            return
        finger_pos = self.handle_camera()
        # check if either player scored
        scored = self.ball.check_scored(self.screen_width)
        if scored != 0:
            return self.start_scored(scored)
        # update the ball, ai paddle, and player paddle
        self.ball.update(dt)
        self.ai_paddle.update(dt, self.ball.pos)
        self.player_paddle.update(dt, finger_pos, FINGER_SENSITIVITY)
        # check for collisions with the bounds and paddles
        ball_intersect_paddle(self.ball, self.player_paddle)
        ball_intersect_paddle(self.ball, self.ai_paddle)
    
    def start_scored(self, scored: int):
        self.in_game = False
        if scored == 1:
            self.ai_score += 1
        else:
            self.player_score += 1
        self.player_paddle.reset()
        self.ai_paddle.reset()
        self.ball.reset()
        scored_txt = "Player scored" if scored == -1 else "AI scored"
        score_txt = f"{self.player_score} - {self.ai_score}"
        scored_label = pyglet.text.Label(
            scored_txt,
            font_name="Arial",
            font_size=24,
            x=self.screen_width / 2,
            y=self.screen_height / 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch
        )
        score_label = pyglet.text.Label(
            score_txt,
            font_name="Arial",
            font_size=24,
            x=self.screen_width / 2,
            y=self.screen_height / 2 - 24,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch
        )
        self.batch.draw()
        
        # check if space is pressed to start next round
        def check_space(dt: float):
            if self.key_handler[pyglet.window.key.SPACE]:
                scored_label.delete()
                score_label.delete()
                self.in_game = True
                pyglet.clock.unschedule(check_space)
                
        pyglet.clock.schedule_interval(check_space, 1/60)
        
    
    
        
        
def run(width: int, height: int, fps: int = 60) -> None:
    # define the window
    window = pyglet.window.Window(width=width, height=height, caption="Pong AI")
    key_handler = pyglet.window.key.KeyStateHandler()
    window.push_handlers(key_handler)
    # define the batch  
    batch = pyglet.graphics.Batch()
    # define the engine
    engine = Engine(width, height, batch, key_handler)
    
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


if __name__ == "__main__":
    run(640, 480)