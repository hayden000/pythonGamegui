#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import required modules

from tkinter import *
import csv
import operator
import tkinter
from tkinter import messagebox

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import time
import random

# Initialise, define and set global variables

bounce = False
xBack = 0
IMG = \
    simplegui.load_image('http://personal.rhul.ac.uk/ZJAC/113/paddle.png'
                         )
IMG_CENTRE = (128.5, 26.5)
IMG_DIMS = (257, 53)
CANVAS_DIMS = 600
STEP = 0.5
img_dest_dim = (100, 20)
img_pos = [CANVAS_DIMS / 2, 2 * CANVAS_DIMS / 3]
img_rot = 0
WIDTH = 500
HEIGHT = 500
y = 335
score = 0
endGame = False
name = ''
score = 0


# Create class for background GUI attributes

class BACKGROUND:

    def __init__(self):
        BACKGROUND = \
            simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/background_clouds.png'
                                 )

    COLOUR_BACKGROUND = 'Light Grey'


# Write a class for the menus

class Application(Frame):

    def __init__(self, master):  # Init is a magic method and a constructor for the class
        super(Application, self).__init__(master)
        self.grid()
        root.geometry('700x700')
        self.create_widgets()
        root.configure(background=BACKGROUND.COLOUR_BACKGROUND)

    def create_widgets(self):  # Method for putting the widgets onscreen like buttons ect...
        Label(self, text='Do you want to Play?').grid(row=0, column=0,
                                                      sticky=W)
        self.selection = StringVar()  # Variables to store if the buttons have been pressed
        self.selection2 = StringVar()
        self.selection3 = StringVar()
        self.selection.set(None)  # Set to depressed
        self.selection2.set(None)
        self.selection3.set(None)

        # Display buttons onscreen

        Radiobutton(self, text='Play game', variable=self.selection,
                    value='play', command=self.update_text).grid(row=2,
                                                                 column=0, sticky=W)

        Radiobutton(self, text='Instructions',
                    variable=self.selection2, value='instructions',
                    command=self.update_text).grid(row=4, column=0,
                                                   sticky=W)
        Label(self, text='Enter Name:').grid(row=1, column=0, sticky=W)

        Radiobutton(self, text='Leaderboard', variable=self.selection3,
                    value='leaderboard',
                    command=self.update_text).grid(row=7, column=0,
                                                   sticky=W)
        Radiobutton(self, text='Quit', variable=self.selection,
                    value='Quit', command=root.destroy).grid(column=0,
                                                             sticky=W)
        self.item = Entry(self)
        self.item.grid(row=1, column=1, sticky=W)

    # When buttons are clicked use this function

    def update_text(self):
        nameValue = self.item.get()
        play = self.selection.get()
        instruction = self.selection2.get()
        leaderboard = self.selection3.get()
        if play == 'play':  # If the user clicks the play option on the menu

            class Vector:  # Define vector class

                def __init__(self, x=0, y=0):
                    self.x = x
                    self.y = y

                def __str__(self):
                    return '(' + str(self.x) + ',' + str(self.y) + ')'

                def __eq__(self, other):
                    return self.x == other.x and self.y == other.y

                def __ne__(self, other):
                    return not self.__eq__(other)

                def get_p(self):
                    return (self.x, self.y)

                def copy(self):
                    return Vector(self.x, self.y)

                def add(self, other):
                    self.x += other.x
                    self.y += other.y
                    return self

                def __add__(self, other):
                    return self.copy().add(other)

                def negate(self):
                    return self.multiply(-1)

                def __neg__(self):
                    return self.copy().negate()

                def subtract(self, other):
                    return self.add(-other)

                def __sub__(self, other):
                    return self.copy().subtract(other)

                def multiply(self, k):
                    self.x *= k
                    self.y *= k
                    return self

                def __mul__(self, k):
                    return self.copy().multiply(k)

                def __rmul__(self, k):
                    return self.copy().multiply(k)

                def divide(self, k):
                    return self.multiply(1 / k)

                def __truediv__(self, k):
                    return self.copy().divide(k)

                def normalize(self):
                    return self.divide(self.length())

                def get_normalized(self):
                    return self.copy().normalize()

                def dot(self, other):
                    return self.x * other.x + self.y * other.y

                def length(self):
                    return math.sqrt(self.x ** 2 + self.y ** 2)

                def length_squared(self):
                    return self.x ** 2 + self.y ** 2

                def reflect(self, normal):
                    n = normal.copy()
                    n.multiply(2 * self.dot(normal))
                    self.subtract(n)
                    return self

                def angle(self, other):
                    return math.acos(self.dot(other) / (self.length()
                                                        * other.length()))

                def rotate_anti(self):
                    (self.x, self.y) = (-self.y, self.x)
                    return self

                def rotate_rad(self, theta):
                    rx = self.x * math.cos(theta) - self.y \
                         * math.sin(theta)
                    ry = self.x * math.sin(theta) + self.y \
                         * math.cos(theta)
                    (self.x, self.y) = (rx, ry)
                    return self

                def rotate(self, theta):
                    theta_rad = theta / 180 * math.pi
                    return self.rotate_rad(theta_rad)

                def get_proj(self, vec):
                    unit = vec.get_normalized()
                    return unit.multiply(self.dot(unit))

            # Pull global variables

            global endGame, InstructionPane
            global bounce
            global xBack
            global CANVAS_DIMS
            bounce = False
            xBack = 0
            CANVAS_DIMS = 600
            endGame = False

            # Class for game over screen

            class gameOver:

                over = \
                    simplegui.load_image('http://personal.rhul.ac.uk/ZJAC/113/gameover.png'
                                         )

            # Class that initialises sounds by getting them from the web

            class sound:

                brickBreak = \
                    simplegui.load_sound('http://personal.rhul.ac.uk/ZJAC/113/break.mp3'
                                         )
                bounceBall = \
                    simplegui.load_sound('http://personal.rhul.ac.uk/ZJAC/113/bounce.mp3'
                                         )

            # Get the sprites from the web

            webList = ['http://personal.rhul.ac.uk/ZJAC/113/red.png',
                       'http://personal.rhul.ac.uk/ZJAC/113/blue.png',
                       'http://personal.rhul.ac.uk/ZJAC/113/yellow.png'
                ,
                       'http://personal.rhul.ac.uk/ZJAC/113/orange.png'
                , 'http://personal.rhul.ac.uk/ZJAC/113/green.png'
                       ]
            brickList = []
            bricks = []
            for i in webList:  # Loop through all sprites' web addresses
                brickList.append(simplegui.load_image(i))  # Load each image and add to list
            brickPosition = []
            for i in range(100, 700, 200):
                for j in range(100, 400, 100):
                    brickPosition.append((i, j))
            brickBoundary = []  # Calculate boundaries for all the bricks onscreen and add to list
            for i in brickPosition:
                brickBoundary.append([i, (i[0] - 56.5, i[1] - 17.5),
                                      (i[0] + 56.5, i[1] + 17.5)])
            for i in range(0, len(brickPosition)):
                bricks.append(brickList[random.randint(0,
                                                       len(brickList)) - 1])
            global IMG
            global IMG_CENTRE
            global IMG_DIMS
            global STEP
            global img_dest_dim
            global img_pos
            global img_rot
            global WIDTH
            global HEIGHT
            global Y
            global score
            IMG = \
                simplegui.load_image('http://personal.rhul.ac.uk/ZJAC/113/paddle.png'
                                     )  # Get paddle sprite from web
            IMG_CENTRE = (128.5, 26.5)
            IMG_DIMS = (257, 53)
            STEP = 0.5
            img_dest_dim = (100, 20)
            img_pos = [CANVAS_DIMS / 2, 2 * CANVAS_DIMS / 3]
            img_rot = 0
            WIDTH = 500
            HEIGHT = 500
            y = 335

            def draw(canvas):  # Initial drawing of canvas along with sprites using loop
                global img_rot
                img_rot += STEP
                canvas.draw_image(
                    IMG,
                    IMG_CENTRE,
                    IMG_DIMS,
                    img_pos,
                    img_dest_dim,
                    img_rot,
                )
                for i in range(0, len(brickPosition)):
                    canvas.draw_image(
                        brickList[random.randint(0, len(brickList))],
                        (56.5, 17.5),
                        (113, 35),
                        brickPosition[i],
                        (113, 35),
                        img_rot,
                    )

            def onGround():  # If ball hits ground
                global y
                if y < 335:
                    return False
                return True

            class Paddle:  # Control user interaction with paddle

                def __init__(self, pos, radius=2):
                    self.pos = pos
                    self.vel = Vector()
                    self.radius = max(radius, 2)
                    self.colour = 'White'
                    self.normal = Vector(0, -1)
                    self.in_range = False

                # Draw paddle and bricks here:

                def draw(self, canvas):
                    global CANVAS_DIMS
                    global IMG
                    global IMG_CENTRE
                    global IMG_DIMS
                    global STEP
                    global img_dest_dim
                    global img_pos
                    global y
                    global img_rot
                    global xBack
                    x = self.pos.x + 70
                    y = self.pos.y - 125

                    # Draw paddle on canvas

                    canvas.draw_image(IMG, [128.5, 26.5], IMG_DIMS, [x,
                                                                     435], img_dest_dim)
                    for i in range(0, len(brickPosition)):
                        # Draw all bricks in brickPosition list on canvas

                        canvas.draw_image(bricks[i], (56.5, 17.5),
                                          (113, 35), brickPosition[i - 1], (113,
                                                                            35))

                    # Display GameOver screen

                    global endGame
                    if endGame:
                        canvas.draw_image(gameOver.over, [350, 350],
                                          [700, 700], [350, 350], [700, 700])
                        global score
                        scoreOutput = str('Score: ' + str(score))
                        canvas.draw_text(scoreOutput, (150, 540), 80,
                                         'White', 'serif')
                    xBack = xBack + 1
                    if xBack > 600:
                        xBack = 0

                # Paddle move with certain velocity and show on the other side when move across the canvas

                def update(self):
                    self.pos.add(self.vel)
                    self.vel.multiply(0.85)
                    if self.pos.x >= 690:
                        self.pos.x = -150
                    elif self.pos.x <= -150:
                        self.pos.x = 690

                # Get the upper side of paddle, where the ball would bounce with it

                def offset_u(self):
                    return self.pos.y - 30

                # Check if the ball hits the paddle by detecting the y coordinate and x coordinate

                def hit_up(self, ball):
                    h = False
                    self.range(ball)
                    if self.in_range:
                        h = self.offset_u() <= ball.offset_d() <= 460
                    return h

                # In case the ball bounces outside the range of paddle, the x coordinate of ball should be in the width of paddle

                def range(self, ball):

                    # As the brick disappeared in this method, the score variable should be introduced

                    global score
                    self.update()
                    x_r = self.pos.x + 50
                    x_l = self.pos.x - 50
                    if ball.pos.x < x_r and ball.pos.x > x_l:
                        self.in_range = True
                    else:
                        self.in_range = False

                    # when ball hits the brick, the brick is removed.

                    for i in brickBoundary:
                        if ball.pos.x > i[1][0] and ball.pos.y \
                                > i[1][1] and ball.pos.x < i[2][0] \
                                and ball.pos.y < i[2][1]:
                            brickPosition.remove(i[0])
                            brickBoundary.remove(i)

                            # Score added up by one once a brick is broken

                            score += 1

                            # play the cound when a brick broken

                            sound.brickBreak.play()

                    # Game over when all bricks are broken/ball goes off without bouncing with paddle

                    if len(brickBoundary) == 0 or self.pos.y > 600:
                        global endGame
                        endGame = True
                        sound.brickBreak.play()

                        # Add the score to leaderboard file

                        addScore(nameValue, score)

            keyPressed = False

            class Keyboard:

                global keyPressed

                def __init__(self):
                    self.right = False
                    self.left = False
                    self.up = False

                def keyDown(self, key):  # Calling this function to read the keyboard actions
                    if key == simplegui.KEY_MAP['right']:
                        if onGround():
                            self.right = True
                    if key == simplegui.KEY_MAP['left']:
                        if onGround():
                            self.left = True
                    if key == simplegui.KEY_MAP['space']:
                        if onGround():
                            self.up = True

                def keyUp(self, key):  # Calling this function to read the keyboard actions
                    if key == simplegui.KEY_MAP['right']:
                        self.right = False
                    if key == simplegui.KEY_MAP['left']:
                        self.left = False
                    if key == simplegui.KEY_MAP['space']:
                        self.up = False
                    if wheel.pos.y == 0:
                        self.up = False

            bounceHeight = 7

            class Ball:

                def __init__(
                        self,
                        pos,
                        vel,
                        radius,
                        border,
                        color,
                ):
                    type = random.randint(1, 2)

                    # Get a random initial vector of the ball

                    if type == 1:
                        x = random.randint(-2, -1)
                        y = random.randint(-2, -1)
                    else:
                        x = random.randint(1, 2)
                        y = random.randint(1, 2)
                    self.pos = pos
                    self.vel = Vector(x, y)
                    self.radius = radius
                    self.border = 1
                    self.color = color

                def update(self):  # Calling this function to make the ball move with random vector produced
                    self.pos.add(self.vel)

                def draw(self, canvas):  # Draw a ball
                    self.update()
                    canvas.draw_circle(self.pos.get_p(), self.radius,
                                       self.border, self.color, 'red')

                # Get four 'edges' of the ball

                def offset_d(self):
                    return self.pos.y + self.radius

                def offset_r(self):
                    return self.pos.x + self.radius

                def offset_l(self):
                    return self.pos.x - self.radius

                def offset_u(self):
                    return self.pos.y - self.radius

                def bounce(self, normal):  # Calling this function to change the vector of the ball
                    self.vel.reflect(normal)
                    sound.bounceBall.play()

            class Wall:

                def __init__(
                        self,
                        x,
                        border,
                        color,
                ):
                    self.x = x
                    self.border = border
                    self.color = color
                    self.normal = Vector(1, 0)
                    self.topNormal = Vector(0, 1)
                    self.edge_r = x + self.border
                    self.edge_l = 600 - self.border
                    self.edge_t = 0 + self.border

                def draw(self, canvas):
                    canvas.draw_line((self.x + CANVAS_DIMS, 0), (self.x
                                                                 + CANVAS_DIMS, CANVAS_DIMS), self.border
                                     * 2 + 1, self.color)
                    canvas.draw_line((self.x, 0), (self.x,
                                                   CANVAS_DIMS), self.border * 2 + 1,
                                     self.color)
                    canvas.draw_line((self.x, 0), (self.x
                                                   + CANVAS_DIMS, 0), self.border * 2 + 1,
                                     self.color)

                def hitTop(self, ball):  # Calling this function to check if ball hit left or right side of canvas
                    h = ball.offset_l() <= self.edge_r \
                        or ball.offset_r() >= self.edge_l
                    return h

                def hit(self, ball):
                    if self.hitTop(ball):
                        return True
                    return False

                def topHit(self, ball):
                    if ball.pos.y <= self.edge_t:
                        return True
                    return False

            class Interaction:  # Iterate the objects

                global y
                global bounceHeight

                def __init__(  # wheel is paddle
                        self,
                        wheel,
                        keyboard,
                        ball,
                        wall,
                ):
                    self.wheel = wheel
                    self.keyboard = keyboard
                    self.ball = ball
                    self.wall = wall
                    self.in_collision = False

                def update(self):  # Calling this function to check if ball bounces with bricks or paddle or wall
                    global img_rot
                    global y
                    global bounce
                    if self.wall.hit(self.ball):  # if ball hits left or right wall
                        if not self.in_collision:
                            self.ball.bounce(self.wall.normal)
                            self.in_collision = True
                    elif self.wall.topHit(self.ball):

                        # If ball hits ceiling. A different vector is reflected from bouncing with side walls.

                        if not self.in_collision:
                            self.ball.bounce(self.wall.topNormal)
                            self.in_collision = True
                    else:
                        self.in_collision = False
                        self.ball.update()
                    if bounce:
                        self.wheel.vel.add(Vector(0, -0.5
                                                  * bounceHeight))
                        bounce = False
                    if self.keyboard.right:
                        self.wheel.vel.add(Vector(1, 0))
                        img_rot += STEP
                    if self.keyboard.left:
                        self.wheel.vel.add(Vector(-1, 0))
                        img_rot -= STEP
                    if self.keyboard.up:
                        self.wheel.vel.add(Vector(0, -bounceHeight))
                        bounce = True
                    if not self.keyboard.up:
                        if y < 335:
                            wheel.pos.y = wheel.pos.y + 10
                    if self.wheel.hit_up(self.ball):
                        if not self.in_collision:
                            self.ball.bounce(self.wheel.normal)
                            self.in_collision = True
                    self.ball.update()

                def draw(self, canvas):
                    self.update()

                    # Draw paddle, ball and walls

                    self.wheel.draw(canvas)
                    self.ball.draw(canvas)
                    self.wall.draw(canvas)

                    # Show score of current round and player

                    global score
                    player_score = 'Your score is: '
                    canvas.draw_text(player_score, (30, 30), 30, 'Red')
                    canvas.draw_text(str(score), (200, 30), 30, 'Blue')

            kbd = Keyboard()
            wheel = Paddle(Vector(WIDTH / 2, HEIGHT - 40), 40)
            ball = Ball(Vector(WIDTH / 2, HEIGHT / 2), Vector(-0.2,
                                                              0.2), 5, 1, 'black')
            w = Wall(1, 5, 'black')
            inter = Interaction(wheel, kbd, ball, w)

            def draw(canvas):
                inter.update()
                wheel.update()
                inter.draw(canvas)
                global img_rot

            frame = simplegui.create_frame('Brick Breaker',
                                           CANVAS_DIMS, CANVAS_DIMS)
            frame.set_canvas_background('#2C6A6A')
            frame.set_draw_handler(draw)
            frame.set_keydown_handler(kbd.keyDown)
            frame.set_keyup_handler(kbd.keyUp)
            frame.start()
            root = Tk()
            root.title('Game instructions')
            app = InstructionPane(root)
            root.mainloop()
        if leaderboard == 'leaderboard':

            def addScore(name, score):  # Calling this function adds items scores to the leaderboard
                name = str(name)
                score = str(int(score))
                with open('scores.csv', 'a') as file:
                    scoreWriter = csv.writer(file)
                    scoreWriter.writerow([name, score])

            def getScores():  # Calling this function returns a list of scores in descending order
                output = []
                result = []
                with open('scores.csv', 'r+') as file:
                    file = file.read()
                    file = file.split('\n')
                    for i in file:
                        i = i.split(',')
                        output.append(i)
                for i in range(0, len(output) - 1):
                    output[i][1] = int(output[i][1])
                for i in range(0, len(output)):
                    for j in range(0, len(output[i])):
                        if output[i][j] == '':
                            output.pop(i)
                output = sorted(output, key=operator.itemgetter(1))
                for i in range(len(output) - 1, 0, -1):
                    result.append(output[i])
                return result

            def showLeaderboard():  # Call this function to display the leaderboard and create a new window
                output = getScores()

                class Application(Frame):

                    def __init__(self, master):
                        super(Application, self).__init__(master)
                        self.grid()
                        root.geometry('500x740')
                        self.create_widgets()
                        root.configure(background='Light Grey')

                    def create_widgets(self):  # Buttons for leaderboard
                        Radiobutton(self, text='Close leaderboard',
                                    value='Quit',
                                    command=root.destroy).grid(column=2,
                                                               sticky=W)
                        Label(self, text='Leaderboard:').grid(row=0,
                                                              column=0, sticky=W)
                        if len(output) <= 30:  # Break text to lines
                            top = len(output)
                        else:
                            top = 30
                        for i in range(0, top):
                            stringOutput = ''
                            stringOutput = str('Place: ' + str(i + 1)
                                               + ' Name: ' + str(output[i][0])
                                               + ' Score: ' + str(output[i][1]))
                            Label(self, text=stringOutput).grid(row=i,
                                                                column=0, sticky=E)

                root = Tk()  # Set window running
                root.title('Leaderboard')
                app = Application(root)
                root.mainloop()

            def clearLeaderboard():  # Overwrite file with new blank file
                if tkinter.messagebox.askyesno('Verify',
                                               'Do you really want to clear the leaderboard?'):
                    with open('scores.csv', 'w') as file:
                        tkinter.messagebox.showerror('Reset',
                                                     'Cleared leaderboard')

            showLeaderboard()
        if instruction == 'instructions':
            instructions = \
                str(
                    'To play the game press the left and right keyboard arrow keys to control the paddle. Hit the ball and then try to eliminate all of the blocks.'
                    )
            screenLength = 40
            lines = []
            for j in range(0, len(instructions) // screenLength + 0):  # Split string based on screen length
                lower = j * screenLength
                upper = (j + 1) * screenLength
                line = ''
                for i in range(lower, upper):
                    line = line + instructions[i]
                lines.append(line)
            last = ''
            lower = len(instructions) // screenLength * screenLength + 0
            upper = len(instructions)
            for i in range(lower, upper):
                last = last + instructions[i]
            lines.append(last)

            class InstructionPane(Frame):

                def __init__(self, master):  # Creating a GUI window
                    super(InstructionPane, self).__init__(master)
                    self.grid()
                    root.geometry('300x300')  # Set GUI size
                    self.create_widgets()

                def create_widgets(self):  # Put buttons onscreen
                    for i in range(0, len(lines)):
                        Label(self, text=lines[i]).grid(row=i,
                                                        column=0, sticky=W)

            root = Tk()
            root.title('Game instructions')  # GUI title
            app = InstructionPane(root)
            root.mainloop()  # Set the frame running


root = Tk()
root.title('Main Menu')  # Main menu title
app = Application(root)
root.mainloop()  # Start the game
