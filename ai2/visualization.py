from turtle import Screen, Turtle
import turtle
import os
import random
import numpy as np
from PIL import Image
from const import *

from init_2 import *


class Visualization:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = {}
        self.map['region'] = game.MAP['region']
        self.map['entity'] = game.MAP['entity']
        self.map['mark'] = np.zeros((height, width), dtype=np.bool_)
        self.map['ratio'] = np.ones((height, width), dtype=np.bool_)
        self.FONT_SIZE = 14 if width <= 16 else 8
        self.SIZE = 40 if width <= 16 else 24
        self.FONT = ('Arial', self.FONT_SIZE, 'normal')
        self.FONT_BOLD = ('Arial', self.FONT_SIZE, 'bold')
        self.COLORS = [(111, 168, 220), (255, 242, 204), (217, 210, 233),
                       (230, 184, 175), (234, 209, 220), (208, 224, 227), (217, 234, 211)]
        while len(self.COLORS) < game.NUM_OF_REGION:
            self.COLORS.append(
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
       # set screen characteristics
        self.screen = Screen()
        self.screen.title('Visualization')
        self.screen.bgcolor('lightblue')
        self.screen.colormode(255)

        # set turtle characteristics
        self.greg = Turtle()
        self.greg.hideturtle()

        # set marker characteristics
        self.marker = Turtle()
        self.marker.penup()
        self.marker.hideturtle()

        self.screen.tracer(0)  # because I have no patience
        turtle.speed('fastest')

    def square(self, size, color, mark):
        ''' draw and fill one square '''
        self.greg.goto(self.greg.xcor() + 1, self.greg.ycor())
        self.greg.fillcolor(color)
        if (mark):
            self.greg.pencolor('red')
            self.greg.pensize(3)
        else:
            self.greg.pencolor('black')
            self.greg.pensize(1)
        self.greg.pendown()
        self.greg.begin_fill()
        for _ in range(4):
            self.greg.forward(size)
            self.greg.left(90)

        self.greg.end_fill()

        self.greg.penup()
        self.greg.forward(size)

    def chessboard(self, map, size):
        ''' draw the whole chessboard '''
        self.greg.penup()

        self.greg.goto(-size * self.width/2, size * self.height/2)
        for i in range(self.height):
            for j in range(self.width):
                region = map['region'][i][j]
                entity = ENTITIES[map['entity'][i][j]]
                mark = map['mark'][i][j]
                ratio = map['ratio'][i][j]

                if (i, j) == game.TREASURE:
                    self.marker.pencolor('yellow')
                if (i, j) == agent.get_position():
                    entity += 'a'
                    self.marker.pencolor('green')
                if (i, j) == pirate.get_position():
                    entity += 'p'
                    self.marker.pencolor('red')

                text = f"{region}{entity}"
                color = self.COLORS[region] if ratio == 1 else "gray"

                self.square(size, color, mark)

                self.marker.goto(self.greg.xcor() - size/2,
                                 self.greg.ycor() + size/2 - self.FONT_SIZE/2)

                self.marker.write(text, align='center', font=self.FONT_BOLD)

                self.marker.pencolor("black")
            self.greg.goto(-size * self.height/2, size *
                           self.width/2 - size * (i + 1))
        self.screen.update()

    def save_image(self, filename):
        if not os.path.exists('./png'):
            os.mkdir('./png')
        if not os.path.exists('./eps'):
            os.mkdir('./eps')
        ts = self.greg.getscreen()
        ts.getcanvas().postscript(file=f'./eps/{filename}.eps')
        img = Image.open(f'./eps/{filename}.eps')
        img.save(f'./png/{filename}.png', 'png')

    def clear_mark(self):
        self.map['mark'] = False

    def visualize(self, filename=None):
        self.chessboard(self.map, self.SIZE)
        if filename != None:
            self.save_image(filename)
