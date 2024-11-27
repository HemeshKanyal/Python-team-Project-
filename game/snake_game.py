import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0
game_running = True 

wn = turtle.Screen()
wn.title("Snake Game by @Aryan")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("blue")
food.penup()
food.goto(0, 100)

segments = []

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0 High Score: 0", align="center", font=("Courier", 24, "normal"))

button_pen = turtle.Turtle()
button_pen.speed(0)
button_pen.shape("square")
button_pen.color("black")
button_pen.penup()
button_pen.hideturtle()

def draw_button(x, y, text, width=100, height=40):
    """Draws a button with text at the given position."""
    button_pen.goto(x - width // 2, y - height // 2)
    button_pen.fillcolor("white")
    button_pen.begin_fill()
    for _ in range(2):
        button_pen.forward(width)
        button_pen.left(90)
        button_pen.forward(height)
        button_pen.left(90)
    button_pen.end_fill()
    button_pen.goto(x, y - 10)
    button_pen.write(text, align="center", font=("Courier", 18, "bold"))

def check_click(x, y):
    """Checks if a button was clicked."""
    if -50 <= x <= 50 and -30 <= y <= 10:  
        reset_game()
    elif -50 <= x <= 50 and -80 <= y <= -40:  
        wn.bye()

def game_over():
    """Displays Game Over screen and buttons."""
    global game_running
    game_running = False  
    button_pen.clear()
    button_pen.goto(0, 50)
    button_pen.write("GAME OVER", align="center", font=("Courier", 24, "bold"))
    draw_button(0, -10, "Replay")
    draw_button(0, -60, "Quit")
    wn.onclick(check_click)  

def reset_game():
    """Resets the game state for replay."""
    global score, delay, segments, game_running
    button_pen.clear()
    wn.onclick(None) 
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    delay = 0.1
    pen.clear()
    pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    game_running = True 


def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)


wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_left, "a")

while True:
    wn.update()
    
    if not game_running:
        time.sleep(0.1)  
        continue  

    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        game_over()

    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("brown")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001

        score += 10
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)


    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()


    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            game_over()

    time.sleep(delay)

wn.mainloop()
