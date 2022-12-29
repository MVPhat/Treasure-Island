from turtle import Screen, Turtle
import turtle
import os

from PIL import Image


class Visualization:
    def __init__(self, width, height, map):
        self.map = map
        self.width = width
        self.height = height
        self.FONT_SIZE = 14 if width == 16 else 8
        self.SIZE = 40 if width == 16 else 24
        self.FONT = ('Arial', self.FONT_SIZE, 'normal')
        self.FONT_BOLD = ('Arial', self.FONT_SIZE, 'bold')
        self.COLORS = [(111, 168, 220), (255, 242, 204), (217, 210, 233),
                       (230, 184, 175), (234, 209, 220), (208, 224, 227), (217, 234, 211)]
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

        # self.greg.goto(-size * (self.width/2), size * (self.height/2 + 1))
        # for i in range(self.width):
        #     color = 'white'
        #     self.square(size, color, False)
        #     self.marker.goto(self.greg.xcor() - size/2,
        #                      self.greg.ycor() - size/2 - self.FONT_SIZE/2)
        #     self.marker.write(i, align='center', font=self.FONT_BOLD)
        # self.greg.goto(-size * (self.width/2+1), size * (self.height/2))

        # for i in range(self.height):
        #     color = 'white'
        #     self.square(size, color, False)
        #     self.marker.goto(self.greg.xcor() - size/2,
        #                      self.greg.ycor() - size/2 - self.FONT_SIZE/2)
        #     self.marker.write(i, align='center', font=self.FONT_BOLD)
        #     self.greg.goto(-size * (self.height/2+1), size *
        #                    self.width/2 - size * (i + 1))

        self.greg.goto(-size * self.width/2, size * self.height/2)
        for i in range(self.height):
            for j in range(self.width):
                area, dump, mark, ratio = map[i][j]
                color = self.COLORS[area] if ratio == 1 else "gray"

                if (f"{area}{dump}" == 'Tp'):
                    color = 'red'
                elif (f"{area}{mark}" == 'TA'):
                    color = 'orange'

                self.square(size, color, mark)

                self.marker.goto(self.greg.xcor() - size/2,
                                 self.greg.ycor() + size/2 - self.FONT_SIZE/2)
    #             self.marker.pencolor("black")
                if (dump == "P" or dump == "T"):
                    self.marker.write(f"{area}{dump}",
                                      align='center', font=self.FONT_BOLD)
                elif 'p' in dump and dump != " ":
                    self.marker.pencolor('red')
                    self.marker.write(f"{area}{dump}",
                                      align='center', font=self.FONT_BOLD)
                    self.marker.pencolor('black')
                else:
                    self.marker.write(f"{area}{dump}",
                                      align='center', font=self.FONT)
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
        # img.show()

    def clear_mark(self):
        self.map['mark'] = False

    def visualize(self, filename):
        self.chessboard(self.map, self.SIZE)
        # self.screen.tracer(False)
        self.save_image(filename)
