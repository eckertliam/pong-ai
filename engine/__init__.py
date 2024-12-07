from engine.paddle import Paddle
from engine.ball import Ball


class Engine:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.ball = Ball(x=width/2, y=height/2, radius=10, speed=100, color=(255, 255, 255), direction=(0, 1))
        
        
        
        
        