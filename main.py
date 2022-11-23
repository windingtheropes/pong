# DON'T FORGET TO INCLUDE COMMENTS AND DESCRIPTIVE VARIABLE NAMES TO MAKE YOUR CODE MORE READABLE
import turtle
import time
import random
import asyncio

screenWidth = 800
screenHeight = 500
wn = turtle.Screen()

running = False

# ui
title = None

# game
o = None
b = None
p1s = None
p2s = None
p1score = None
p2score = None

speed = 3;
# variables
umove = [0, 0]
bpos = [0, 0]
p1y = 0
score1 = 0
score2 = 0

## USER INTERFACE ELEMENTS

def initMenu():
    global title
    title = turtle.Turtle()
    title.hideturtle()
    title.penup()
    title.goto(-75, 300)
    title.write("Pong", move=False, align="left", font=("Arial", 48, "normal"))

## END USER INTERFACE ELEMENTS

def initScreen():
  global wn
  wn.clear()
  wn.bgcolor("black")
  wn.screensize(screenWidth, screenHeight)
  wn.title("Pong")
  wn.tracer(0, 0)

# outline the game boundaries
def initGameBounds():
  global o
  o = turtle.Turtle()
  o.width(5)
  o.pencolor("white")
  o.penup()
  o.goto(-400, 250)
  
  o.pendown()
  o.forward(800)
  o.right(90)
  o.forward(500)
  o.right(90)
  o.forward(800)
  o.right(90)
  o.forward(500)
  
  o.hideturtle()

# ball
def initBall():
  global b
  b = turtle.Turtle()
  b.pencolor("white")
  b.color("white")
  b.speed(0)
  b.shape("square")
  b.shapesize(stretch_wid=1, stretch_len=1)
  b.penup()

# paddle 1
def initPaddles():
  # set listeners for key presses
  wn.onkeypress(lambda: p1stagey(-1), "Down")
  wn.onkeypress(lambda: p1stagey(1), "Up")
  
  wn.listen()

  global p1s
  global p2s
  p1s = turtle.Turtle()
  p1s.shape("square")
  p1s.color("white")
  p1s.shapesize(stretch_wid=6, stretch_len=1)
  p1s.penup()
  p1s.goto(screenWidth * 0.4, 0)
  # paddle 2
  p2s = turtle.Turtle()
  p2s.shape("square")
  p2s.color("white")
  p2s.shapesize(stretch_wid=6, stretch_len=1)  # 10x60
  p2s.penup()
  p2s.goto(screenWidth * 0.4, 0)

def initScoreboard():
  global p1score
  global p2score
  # p1score
  p1score = turtle.Turtle()
  p1score.color("white")
  p1score.hideturtle()
  p1score.penup()
  p1score.goto(-75, 300)
  p1score.write("0", move=False, align="left", font=("Arial", 48, "normal"))
  
  # p2score
  p2score = turtle.Turtle()
  p2score.color("white")
  p2score.hideturtle()
  p2score.penup()
  p2score.goto(75, 300)
  p2score.write("0", move=False, align="left", font=("Arial", 48, "normal"))

def initGame():
  global running
  initScreen()
  initGameBounds()
  initScoreboard()
  initBall()
  initPaddles()
  running = True

# def initUI():
#     initMenu()
# initUI()
# initGame()
# update the score counters
def updateScores():
    global running
    global score1
    global score2
    p1score.clear()
    p2score.clear()
    if (score1 > 10):
        score1 = 0
        score2 = 0
    elif (score2 > 10):
        score1 = 0
        score2 = 0
    p1score.write(str(score1),
                  move=False,
                  align="left",
                  font=("Arial", 48, "normal"))
    p2score.write(str(score2),
                  move=False,
                  align="left",
                  font=("Arial", 48, "normal"))

# set the position of the ball, also allowing for paddle 2 tracking
def setBallPos(x, y):
    b.clear()
    b.setpos(x, y)
    

# move paddle 1, os is the offset, and exact y will set the exact y coordinate
def p1(os=0, ExactY=0):
    global p1pos
    if (((p1s.ycor() + os) > 250-50) or ((p1s.ycor() + os) < -250+50)):
        return
    if (ExactY != 0):
        p1s.setpos(-350, ExactY)
    else:
        p1s.setpos(-350, p1s.ycor() + os)

# move paddle 2, os is the offset, and exact y will set the exact y coordinate
def p2(os=0, ExactY=0):
    global p2pos
    if (ExactY != 0):
        p2s.setpos(350, ExactY)
    else:
        p2s.setpos(350, p2s.ycor() + os)


def p1stagey(y):
    global p1y
    p1y = y



# box boundaries
# x:
# -250 to 250
# y:
# -400 to 400

# use umove (the upcoming move ([x,y])) to move the ball. 
def moveBall():
    global umove
    global running
  
    # generate a new umove if it's blank
    if (umove[0] == 0 and umove[1] == 0):
        umove = genDirection()
        return moveBall()
    setBallPos(b.xcor() + umove[0] * speed, b.ycor() + umove[1] * speed)

def resetBall():
    global umove
    umove = [0, 0]  
    setBallPos(0, 0)      
    
def paddleAi():
    p2(ExactY=b.ycor())
    

# function to check if the ball is colliding with something, and functionality to bounce it
def checkCollision():
    global p1pos
    global score1
    global score2
    global umove

    pos = [b.xcor(), b.ycor()]

    x = pos[0]
    y = pos[1]

    ux = umove[0]
    uy = umove[1]

    propX = x + ux
    propY = y + uy
    if (propX < -400):
        # RIGHT SIDE
        score2 += 1
        updateScores()
        resetBall()
    elif (propX > 400):
        # LEFT SIDE
        score1 += 1
        updateScores()
        resetBall()
    elif (propY > 250 or propY < -250):
        umove[1] = -umove[1]
        # return "y"
    # MAIN PADDLE COLLISIONS (FRONT SIDE)
    elif (propX < p1s.xcor() + 10 and propX > p1s.xcor() - 10
          and propY < p1s.ycor() + 60 and propY > p1s.ycor() - 60):
        umove[0] = -umove[0]
        # PADDLE 1 IS ON THE LEFT, SO VALUES ARE NEGATIVE
        # COLLIDED WITH PADDLE 1
        # return "x"
    elif (propX < p2s.xcor() + 10 and propX > p2s.xcor() - 10
          and propY > p2s.ycor() - 60 and propY < p2s.ycor() + 60):
        # PADDLE 2 IS ON THE RIGHT, SO VALUES ARE POSITIVE
        # COLLIDED WITH PADDLE 2
        umove[0] = -umove[0]
        # return "x"

# rounds decimal to fifths, to be used to generate a random number from -1,1 including -0.5 and 0.5
def roundFifths(x, prec=1, base=.5):
    return round(base * round(float(x) / base), prec)


def genDirection():
    # generates a random diagonal direction
    xfactor = roundFifths(random.uniform(-1, 1))
    yfactor = roundFifths(random.uniform(-1, 1))
    if (xfactor == 0 or yfactor == 0):
        return genDirection()
    return [xfactor, yfactor]



def start():
    # initGame()
    while running == True:
      p1(0)
      p2(0)
      setBallPos(0, 0)
      break
  # game loop, runs 144 times a second for smooth rendering
  # moves the ball and checks collisions every loop
    while running == True:
        global p1y
        moveBall()
        paddleAi()
        checkCollision()
        if (p1y != 0):
            p1(p1y * 16)
            p1y = 0
        wn.update()
        time.sleep(0.00694444444)


start()
