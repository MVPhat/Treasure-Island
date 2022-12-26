from hint import Hint
from turtle import Screen, Turtle


class Visualization:
    def __init__(self, width, height, Tx, Ty, map):
        self.map = map
        self.width = width
        self.height = height
        self.FONT_SIZE = 14
        self.SIZE = 40
        self.FONT = ('Arial', self.FONT_SIZE, 'normal')
        self.FONT_BOLD = ('Arial', self.FONT_SIZE, 'bold')
        self.COLORS = [(111, 168, 220), (255, 242, 204), (217, 210, 233),
                       (230, 184, 175), (234, 209, 220), (208, 224, 227), (217, 234, 211)]
        self.hint = Hint(map, width)
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

        self.screen.tracer(False)  # because I have no patience

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
        self.greg.goto(-size * self.height/2, size * self.width/2)
        for i in range(self.height):
            for j in range(self.width):
                area, dump, mark, ratio = map[i][j]
                color = self.COLORS[area] if ratio == 1 else "gray"

                self.square(size, color, mark)

                self.marker.goto(self.greg.xcor() - size/2,
                                 self.greg.ycor() + size/2 - self.FONT_SIZE/2)
    #             self.marker.pencolor("black")
                if (dump == "P" or dump == "T"):
                    self.marker.write(f"{area}{dump}",
                                      align='center', font=self.FONT_BOLD)
                else:
                    self.marker.write(f"{area}{dump}",
                                      align='center', font=self.FONT)
            self.greg.goto(-size * self.height/2, size *
                           self.width/2 - size * (i + 1))

    def save_image(self, filename):
        ts = self.greg.getscreen()
        ts.getcanvas().postscript(file=filename)

    def clear_mark(self):
        for i in range(self.width):
            for j in range(self.height):
                value, dump, mark, ratio = self.map[i][j]
                self.map[i][j] = (value, dump, False, ratio)

    def visualize(self, hint, verify=False):
        if (hint == 'h1'):
            self.hint.hint_1()
        elif (hint == 'h2'):
            self.hint.hint_2()
        elif (hint == 'h3'):
            self.hint.hint_3()
        elif (hint == 'h4'):
            self.hint.hint_4()
        elif (hint == 'h5'):
            self.hint.hint_5()
        elif (hint == 'h6'):
            self.hint.hint_6()
        elif (hint == 'h7'):
            self.hint.hint_7()
        elif (hint == 'h8'):
            self.hint.hint_8()
        elif (hint == 'h9'):
            self.hint.hint_9()
        elif (hint == 'h10'):
            self.hint.hint_10()
        elif (hint == 'h11'):
            self.hint.hint_11()
        elif (hint == 'h12'):
            self.hint.hint_12()
        elif (hint == 'h13'):
            self.hint.hint_13()
        elif (hint == 'h14'):
            self.hint.hint_14()
        elif (hint == 'h15'):
            self.hint.hint_15()

        self.chessboard(self.hint.map, self.SIZE)

        # if (verify):
        #     self.chessboard(self.hint.verify(hint), self.SIZE)

        self.screen.tracer(False)
        self.save_image('hint.eps')
