from tkinter import *
import tkinter as tk
import time
import math
import pickle
import os.path
import sys

# This game is called reverse ping pong. The user is a ball and has to hit the
# platforms. When the platforms are hit, they decrease in size and finally
# disappear, that's how one wins a level. There are 3 levels, each more
# difficult than the previous one. The user gets points for hitting a platform:
# in first level - 2 points each hit, second level - 4, third - 6
# Moreover, every level has a time limit the level has to be completed in. If
# the user doesn't finish the level in time, he/she loses.
# Saving happens automatically - if the user wins or looses. The leaderboard
# appears in the end. The loading-saving systems works like this: if one types
# in a username which already has been created, one can continue from the
# points which the username already had. If not, a new username is created with
# 0 points.
# Cheats: Shift+T for more time in a level, Shift+F for faster ball, Shift+S
# for slower ball. Each cheat can be used only one time in a level.
# Pause and unpause with space.

x = 0


# a class for creating a platform.
class Platform:
    # Arguments: the canvas and the coordinates where the platform is created
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.platform = canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    # function for moving the platform
    # it moves by changing the coordinates by x1 and y1
    def move(self, platform, canvas, x1, y1):
        self.canvas.move(self.platform, x1, y1)


# a class for creating a ball.
class Ball:
    # Arguments: the canvas, the width and height of the screen
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.ball = canvas.create_oval(
        	width/2 - 30, height/2 - 30, width/2, height/2, fill="purple"
        )

    # function for moving the ball
    # it moves by changing the coordinates by x1 and y1
    def bmove(self, ball, canvas, x1, x2):
        self.canvas.move(self.ball, x1, x2)


# A class for creating a topmenu
class Menu1():
    def __init__(self, window):
        self.window = window
        self.menubar = Menu(window)
        self.window.config(menu=self.menubar)

    # Adding menu items: play, boss_key, restart and quit
    def adding(self, menubar):
        self.menubar.add_separator()  # using separator for separating items
        self.menubar.add_separator()  # but it is not working on the
        self.menubar.add_separator()  # lab computers, yet working on others
        self.menubar.add_separator()
        self.menubar.add_command(label="PLAY", command=play)
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_command(label="BOSS KEY", command=boss_key)
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_command(label="RESTART", command=restart)
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_command(label="QUIT", command=quit)
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()
        self.menubar.add_separator()


# creating a window, returning it's width and height
def window1():
    window = Tk()
    window.title("REVERSE PING PONG")

    # getting width and height
    # and adapting a fulscreen mode so the title is visible
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))     # full screen
    window.configure(bg="black")
    window.resizable(width=TRUE, height=TRUE)  # resizable
    return window, w, h


# Countdown, which shows how much time is there left until you lose. You loose
# if the countdown reaches 0. Each level has a different countdown value.
# Arguments: x - time;
def Countdown(x):
    global text1, limit, ind1, t
    if t > 0:     # if time expansion cheat key combination is used you get
        x += t    # you get more time to finish the level
        t = 0     # and time cheat is disabled
    # if it's not the end of the time and restart and pause weren't enabled:
    if x > 0 and ind1 < 1 and restart1 < 1 and pause == 0:
        x -= 1
        canvas.delete(text1)
        text1 = canvas.create_text(
            width/6, height/18, text="TIME LEFT: " + str(x),
            font="Helvetica 40 bold", fill="Red"
        )
        window.after(500, lambda: Countdown(x))   # again
    elif pause == 1:
        window.after(7, lambda: Countdown(x))  # waits for unpause
    elif ind1 == 1:            # if all platform have been destroyed
        ind1 = 0
    elif x == 0:           # if you run out of time
        limit = 1
        canvas.delete("all")
        text1 = canvas.create_text(
            width/2, height/2, text="YOU LOSE ",
            font="Helvetica 40 bold", fill="Red"
        )
        window.update()
        time.sleep(1)
        leaderboard()


# a loop for moving everything
# Arguments: firstA, firstB-platform coordinates; minus - how much the platform
# decreases, min - what's the minimum for a platform to not disappear
# speed-a delay for every loop; ball_speed, plat_speed,
# points - points from the beginning (if the user is continuing the game)
# points_for_level - points if you hit a platform; menu, time - time for level
def MoveStuff(
    firstA, firstB, minus, min, speed, ball_speed, plat_speed,
    points, points_for_level, menu, time
):
    x11 = 10                 # first platform
    x12 = 20                 # first platform
    x21 = width - 20         # second platform
    x22 = width - 10         # second platform
    y11 = firstA
    y12 = firstB
    y21 = firstA
    y22 = firstB

    platform1 = Platform(canvas, x11, y11, x12, y12)
    platform2 = Platform(canvas, x21, y21, x22, y22)

    ball = Ball(canvas, width, height)

    global pause, text1, ind1, text
    pause = 0

# a=0 means first platform is going down and second one - up;a = 1 the opposite
    i = 0
# a=0 right->left up, a=1 right->left down, a=2 left->right down,
# a=3 left->right up
    a = 0
    ind = 0                # index of how many platforms have been removed
# the amount of how y axis is changing = amount of pixels a ball moves
    ball_y = ball_speed
    cball = canvas.coords(ball.ball)
# values of screen size I found looked the best and I made them resizable
# for every screen width and height
# p_down - an amount of how low can ball and platforms go down in the screen
    p_down = round((height * 0.1083), 0)
    h80 = round((height * 0.0889), 0)

    x = time
    text1 = canvas.create_text(
        width/6, height/18, text="TIME LEFT: " + str(x),
        font="Helvetica 40 bold", fill="Red"
    )
    window.after(1, lambda: Countdown(x))

    while ind < 2:         # while there is at least one platform
        if limit == 0:     # if countdown time is not 0
            if pause == 0:  # if not pause
                global faster, slower, direction
                window.update()
                window.after(speed)

                # if any of the cheats are activated
                if faster > 0:
                    ball_speed += faster
                    faster = 0
                if slower > 0:
                    ball_speed -= slower
                    slower = 0

                tupl1 = canvas.coords(platform1.platform)
                tupl2 = canvas.coords(platform2.platform)

                # if any key for going up or down is pressed and if not out of
                # bounds, coordinates which are added up change
                b = 3
                if cball[1] > h80 and cball[3] < height - h80:
                    if a == 0 or a == 3:
                        if direction == "up":
                            b = 0           # Just an index of what happened
                            ball_y += 10
                        elif direction == "down":
                            b = 1
                            ball_y -= 10
                    elif a == 1 or a == 2:
                        if direction == "up":
                            b = 0           # Just an index of what happened
                            ball_y -= 10
                        elif direction == "down":
                            b = 1
                            ball_y += 10
                else:
                    if direction == "up":
                        pass
                    elif direction == "down":
                        pass
                direction = ""   # set to zero again so it stops adding coords

                cball = canvas.coords(ball.ball)
                # ball is moving
                a = move_ball(cball, ball, a, ball_speed, ball_y, p_down)

                ball_y = ball_speed   # set to primary value again

                # If first platform is hit, it becomes smaller
                if (
                    cball[1] <= tupl1[3] and cball[1] >= tupl1[1] and
                    cball[0] <= tupl1[2] and cball[0] >= tupl1[2] - ball_speed
                ):
                    # making platform disappear and a smaller one appear
                    if tupl1[3] - tupl1[1] >= min:
                        canvas.itemconfigure(
                            platform1.platform, state='hidden'
                        )
                        platform1.move(platform1.platform, canvas, -100, 0)
                        platform1 = Platform(
                            canvas, tupl1[0], tupl1[1]+minus,
                            tupl1[2], tupl1[3] - minus
                        )
                        points += points_for_level  # points are added
                        display_points(points)      # displaying the points
                        tupl1 = canvas.coords(platform1.platform)
                    else:
                        # if platform was hit enough times it disappears
                        canvas.itemconfigure(
                            platform1.platform, state='hidden'
                        )
                        platform1.move(platform1.platform, canvas, -100, 0)
                        ind += 1  # incremented amount of platforms which were
                        # deleted
                        points += points_for_level
                        display_points(points)
                    save_points(points)  # saving the points to the pickle

                # If second platform is hit, it becomes smaller
                # all the comments are the same as for the first platform
                if (
                    cball[1] <= tupl2[3] and cball[3] >= tupl2[1] and
                    cball[2] >= tupl2[0] and cball[2] <= tupl2[2] + ball_speed
                ):
                    if tupl2[3] - tupl2[1] >= min:
                        canvas.itemconfigure(
                            platform2.platform, state='hidden'
                        )
                        platform2.move(
                            platform2.platform, canvas, width + 100, 0
                        )
                        platform2 = Platform(
                            canvas, tupl2[0], tupl2[1]+minus,
                            tupl2[2], tupl2[3] - minus
                        )
                        points += points_for_level
                        text = display_points(points)
                        tupl2 = canvas.coords(platform2.platform)
                    else:
                        canvas.itemconfigure(
                            platform2.platform, state='hidden'
                        )
                        platform2.move(
                            platform2.platform, canvas, width + 100, 0
                        )
                        ind += 1
                        points += points_for_level
                        text = display_points(points)
                    save_points(points)

            # Platforms are moving if they are not out of bounds of the window
            # (+- the speed of platforms)
                # left is going down, right - up
                if tupl1[3] < height - p_down and tupl2[1] > 70 and i == 0:
                    down_up(
                        platform1, platform1.platform, platform2,
                        platform2.platform, plat_speed, 1
                    )
                # if out of bounds, change the index to identify the direction
                elif (
                    (tupl1[3] >= height - p_down or
                        tupl1[3] <= height - p_down + plat_speed) or
                    (tupl2[1] <= 70 or tupl1[2] >= 70 - plat_speed) and i == 0
                ):
                    i = 1
                # left is going up, right - down
                if tupl1[1] > 70 and tupl2[3] < height - p_down and i == 1:
                    down_up(
                        platform1, platform1.platform, platform2,
                        platform2.platform, plat_speed, -1
                    )
                # if out of bounds, change the index to identify the direction
                elif (
                    (tupl1[1] <= 70 or tupl1[1] >= 70 - plat_speed) or
                    (tupl2[3] >= height - p_down or
                        tupl2[3] <= height - p_down + plat_speed) and i == 1
                ):
                    i = 0
            else:  # if pause
                canvas.update()
                continue
        else:  # if out of time
            break

    canvas.delete("all")
    ind1 = 1  # both platforms are destroyed
    return points


# the platforms are moving. The arguments: platform2 = platform1.platform
# (calling a class), platform3 - platform2, platform4 = platform2.platform.
# plat_speed - platform speed, x - going up or down
def down_up(platform1, platform2, platform3, platform4, plat_speed, x):
    platform1.move(platform2, canvas, 0, x * plat_speed)
    platform3.move(platform4, canvas, 0, x * -plat_speed)


# moving the ball. Arguments: cball - ball coordinates; ball-an object of ball
# a - an index of which way the ball is moving, ball_speed, ball_y, P_down -
# already explained
def move_ball(cball, ball, a, ball_speed, ball_y, p_down):
    while True:
        if cball[1] > 70 and cball[0] > 20 and a == 0:                     # 0
            ball.bmove(ball.ball, canvas, -ball_speed, -ball_y)
            break
        if cball[1] <= 70 and cball[1] >= 70 - ball_y - 10 and a == 0:
            a = 1
        if cball[0] <= 20 and cball[0] >= 20 - ball_speed and a == 0:
            a = 3
        if cball[3] < height - p_down and cball[0] > 20 and a == 1:         # 1
            ball.bmove(ball.ball, canvas, -ball_speed, ball_y)
            break
        if cball[0] <= 20 and cball[0] >= 20 - ball_speed and a == 1:
            a = 2
        if (
            cball[3] >= height - p_down and
            cball[3] <= height - p_down + ball_y + 10 and a == 1
        ):
            a = 0
        if cball[3] < height - p_down and cball[2] < width - 20 and a == 2:
            ball.bmove(ball.ball, canvas, ball_speed, ball_y)   # 2
            break
        if (
            cball[3] >= height - p_down and
            cball[3] <= height - p_down + ball_y + 10 and a == 2
        ):
            a = 3
        if (
            cball[2] >= width - 20 and
            cball[2] <= width - 20 + ball_speed and a == 2
        ):
            a = 1
        if cball[1] > 70 and cball[2] < width - 20 and a == 3:        # 3
            ball.bmove(ball.ball, canvas, ball_speed, -ball_y)
            break
        if cball[1] <= 70 and cball[1] >= 70 - ball_y - 10 and a == 3:
            a = 2
        if (
            cball[2] >= width - 20 and cball[2] <= width - 20 + ball_speed and
            a == 3
        ):
            a = 0
    return a


# calling Level1. Arguments: click_start - if start button was activated, menu.
def Level1(click_start, menu):
    global text1, text
    cheats()  # activated
    minus = 40      # how much the platform decreases when collision
    min = 240       # what's the minimum of platform length for it to disappear
    speed = 5       # a delay in every loop
    ball_speed = 2
    plat_speed = 2
    time = 101         # time for completing the game
    if click_start == 1:
        canvas.delete(text1)
        text1 = canvas.create_text(
            width/2, height/18, text="LEVEL 1",
            font="Helvetica 40 bold", fill="Red"
        )
        text = canvas.create_text(
            width - width/6, height/18, text="POINTS: " + str(points1),
            font="Helvetica 40 bold", fill="Red"
        )
        points = MoveStuff(            # call while loop for moving everything
            height/2 + 150, height/2 - 160, minus, min, speed,
            ball_speed, plat_speed, points1, 2, menu, time
        )
        canvas.delete(text1)
        return points
    else:
        text1 = canvas.create_text(
            width/2, height/18, text="PRESS PLAY",
            font="Helvetica 40 bold", fill="Red"
        )


# displaying level 2. Arguments: menu widget
def Level2(menu):
    global text1, text
    cheats()        # binding cheats again (one time per level)
    points = 8 + points1
    minus = 30      # how much the platform decreases when collision
    min = 190       # what's the minimum of platform length for it to disappear
    speed = 6
    ball_speed = 3
    plat_speed = 2
    time = 201
    text = canvas.create_text(
        width - width/6, height/18,
        text="POINTS: " + str(points), font="Helvetica 40 bold", fill="Red"
    )
    text = display_points(points)
    text1 = canvas.create_text(
        width/2, height/18, text="LEVEL 2",
        font="Helvetica 40 bold", fill="Red"
    )
    points = MoveStuff(
        height/2 + 130, height/2 - 140, minus, min, speed,
        ball_speed, plat_speed, points, 4, menu, time
    )
    canvas.delete(text1)
    return points


# displaying level 2. Arguments: menu widget
def Level3(menu):
    global text1, text
    cheats()        # binding cheats again (one time per level)
    points = 32 + points1
    minus = 30      # how much the platform decreases when collision
    min = 170       # what's the minimum of platform length for it to disappear
    speed = 7
    ball_speed = 4
    plat_speed = 3
    time1 = 301
    text = canvas.create_text(
        width - width/6, height/18,
        text="POINTS: " + str(points), font="Helvetica 40 bold", fill="Red"
    )
    text = display_points(points)
    text1 = canvas.create_text(
        width/2, height/18, text="LEVEL 3",
        font="Helvetica 40 bold", fill="Red"
    )
    points = MoveStuff(
        height/2 + 120, height/2 - 130, minus, min, speed,
        ball_speed, plat_speed, points, 6, menu, time1
    )
    canvas.delete(text1)
    text1 = canvas.create_text(
        width/2, height/18, text="YOU WIN!",
        font="Helvetica 40 bold", fill="Red"
    )
    save_points(points)  # saving info in the end of the game
    window.update()
    time.sleep(2)
    leaderboard()        # displaying leaderboard
    return points


# a countdown function before unpause
def countdown321():
    # making sure it is not started before the game begins or after it ends
    if click_start == 1:
        text3 = canvas.create_text(
            width/2, height/2, text="3",
            font=("Helvetica", 60), fill="Red"
        )
        window.update()
        time.sleep(1)
        canvas.delete(text3)
        text3 = canvas.create_text(
            width/2, height/2, text="2",
            font=("Helvetica", 40), fill="Red"
        )
        window.update()
        time.sleep(1)
        canvas.delete(text3)
        text3 = canvas.create_text(
            width/2, height/2, text="1",
            font=("Helvetica", 20), fill="Red"
        )
        window.update()
        time.sleep(1)
        canvas.delete(text3)


# a function for displaying the beginning of the game (settings) for typing in
# a key for going up, going down and surname.
def settings():
    global e1, e2, e3  # Entry widget contents

    # Empty spaces, text, entry widget and button for first key
    text00 = tk.Text(window, height=4, width=19, bg="black", bd=0)
    text00.config(highlightbackground="black", state=DISABLED)
    text00.pack()
    text0 = tk.Text(
        window, height=2, width=20, bg="black", fg="red", bd=0,
        font=("Helvetica", 50)
    )
    text0.config(highlightbackground="black")
    text0.pack()
    text0.insert(tk.END, "REVERSE PING PONG")
    text0.config(state=DISABLED)
    text00 = tk.Text(window, height=4, width=19, bg="black", bd=0)
    text00.config(highlightbackground="black", state=DISABLED)
    text00.pack()
    text1 = tk.Text(
        window, height=1, width=18, bg="black", fg="white", bd=0,
        font="Helvetica 20"
    )
    text1.config(highlightbackground="black")
    text1.pack()
    text1.insert(tk.END, "KEY FOR GOING UP")
    text1.config(state=DISABLED)
    e1 = Entry(window, width=38)
    e1.config(highlightbackground="black")
    e1.pack()
    e1.focus_set()
    text00 = tk.Text(window, height=1, width=19, bg="black", bd=0)
    text00.config(highlightbackground="black", state=DISABLED)
    text00.pack()
    up = Button(window, text="ENTER", width=10, command=key1)
    up.config(highlightbackground="black")
    up.pack()

    # Empty spaces, text, entry widget and button for second key
    text0 = tk.Text(window, height=5, width=19, bg="black", fg="white", bd=0)
    text0.config(highlightbackground="black", state=DISABLED)
    text0.pack()
    text2 = tk.Text(
        window, height=1, width=22, bg="black", fg="white", bd=0,
        font=("Helvetica", 20)
    )
    text2.config(highlightbackground="black")
    text2.pack()
    text2.insert(tk.END, "KEY FOR GOING DOWN")
    text2.config(state=DISABLED)
    e2 = Entry(window, width=38)
    e2.config(highlightbackground="black")
    e2.pack()
    text00 = tk.Text(window, height=1, width=19, bg="black", bd=0)
    text00.config(highlightbackground="black", state=DISABLED)
    text00.pack()
    down = Button(window, text="ENTER", width=10, command=key2)
    down.config(highlightbackground="black")
    down.pack()

    # Empty spaces, text, entry widget and button for entering username
    text0 = tk.Text(window, height=5, width=19, bg="black", fg="white", bd=0)
    text0.config(highlightbackground="black", state=DISABLED)
    text0.pack()
    text2 = tk.Text(
        window, height=1, width=24, bg="black", fg="white", bd=0,
        font="Helvetica 20"
     )
    text2.config(highlightbackground="black")
    text2.pack()
    text2.insert(tk.END, "ENTER YOUR USERNAME")
    text2.config(state=DISABLED)
    e3 = Entry(window, width=38)
    e3.config(highlightbackground="black")
    e3.pack()
    text00 = tk.Text(window, height=1, width=19, bg="black", bd=0)
    text00.config(highlightbackground="black", state=DISABLED)
    text00.pack()
    down = Button(window, text="SUBMIT", width=10, command=username)
    down.config(highlightbackground="black")
    down.pack()

    # Button done for continuing to the start screen
    text0 = tk.Text(window, height=5, width=19, bg="black", fg="white", bd=0)
    text0.config(highlightbackground="black", state=DISABLED)
    text0.pack()
    done = Button(window, text="DONE ", width=20, command=done1)
    done.config(highlightbackground="black")
    done.pack()


# when username is typed in and submit pressed, this function is called.
def username():
    global points1, usrn
    usrn = e3.get()    # entry widget contents
    e3.delete(0, END)  # making the entry widget empty after submit is pressed
    pickle_in = open("users.pickle", "rb")  # opening a pickle
    user_dict = pickle.load(pickle_in)      # and taking it's contents
    pickle_in.close()
    if user_dict.get(usrn) is None:       # checking if username already exists
        user_dict[usrn] = 0              # if it doesn't, create a new username
        points1 = 0
        user_dict[usrn] = points1
    else:
        points1 = user_dict.get(usrn)    # if it does, take the points
        user_dict[usrn] = points1
    pickle_out = open("users.pickle", "wb")
    pickle.dump(user_dict, pickle_out)
    pickle_out.close()


# saving points. Arguments: points2 - current scored points
def save_points(points2):
    user_dict[usrn] = points2
    pickle_out = open("users.pickle", "wb")
    pickle.dump(user_dict, pickle_out)
    pickle_out.close()


# displaying points. Arguments: currect points
def display_points(points2):
    global text
    canvas.delete(text)
    text = canvas.create_text(
        width - width/6, height/18, text="POINTS: " + str(points2),
        font="Helvetica 40 bold", fill="Red"
    )
    return text


# binding default keys for going up and down and pausing the game
def keys():
    window.bind('<Up>', upKey)
    window.bind('<Down>', downKey)
    window.bind("<space>", space)
    window.focus_set()


# binding keys for cheat codes
def cheats():
    window.bind("<Shift-T>", more_time)
    window.bind("<Shift-F>", faster_ball)
    window.bind("<Shift-S>", slower_ball)


# what happens when space is pressed: pause either enables or disables
def space(event):
    global pause
    if pause == 0:
        pause = 1
    else:
        countdown321()  # countdown is called if unpaused
        pause = 0


# one of the cheats - more time
def more_time(event):
    # t is time which is going to be provided additionaly as a cheat code
    global t
    t = 50
    window.unbind("<Shift-T>")  # unbinding so it's used only one time in level


# one of the cheat codes - faster ball
def faster_ball(event):
    global faster
    faster = 1    # the ball is going to move faster
    window.unbind("<Shift-F>")


# one of the cheat codes - slower ball
def slower_ball(event):
    global slower
    slower = 1    # the ball is going to move faster
    window.unbind("<Shift-S>")


# is called when play is pressed. Can be called only one time
def play():
    global menu, ind1, click_start
    if click_start == 0:   # if haven't been pressed before
        click_start = 1
        canvas.delete(menu)                 # Updating menu
        menu = Menu1(window)
        menu.adding(menu.menubar)
        points = Level1(click_start, menu)
        time.sleep(0.5)
        if points == 8 + points1:  # if full points were collected
            points = Level2(menu)
        if points == 32 + points1:  # if full points were collected
            time.sleep(0.5)
            points = Level3(menu)


# if key for going down is pressed
def downKey(event):
    global direction
    direction = "down"


# if key for going up is pressed
def upKey(event):
    global direction
    direction = "up"


# is called when submit is pressed when key for going up is typed in
def key1():
    o = e1.get()  # entry widget contents
    e1.delete(0, END)
    up = "<" + o[0].lower() + ">"
    window.bind(up, upKey)


# is called when submit is pressed when key for going up is typed in
def key2():
    b = e2.get()  # entry widget contents
    e2.delete(0, END)
    up = "<" + b[0].lower() + ">"
    window.bind(up, downKey)


# if done is pressed
def done1():
    for widget in window.winfo_children():
        widget.destroy()                   # removing everything from window
    create_canvas()               # and creating canvas for displaying the game


# creating canvas, adding the menu and calling Level1 to display "PRESS START"
def create_canvas():
    global canvas, menu
    canvas = Canvas(window, bg="black", width=width - 5, height=height - 40)
    canvas.pack()
    menu = Menu1(window)
    menu.adding(menu.menubar)
    Level1(click_start, menu)


# displaying leaderboard
def leaderboard():
    pickle_in = open("users.pickle", "rb")  # opening the pickle
    user_dict = pickle.load(pickle_in)      # and taking it's contents
    pickle_in.close()
    canvas.pack_forget()                    # removing the canvas for a game

    text0 = tk.Text(
        window, height=2, width=30, bg="black", fg="white",
        bd=0, font="Helvetica 25"
    )
    text0.config(highlightbackground="black", state=DISABLED)
    text0.pack()
    text1 = tk.Text(
        window, height=2, width=15, bg="black", fg="white", bd=0,
        font="Helvetica 25"
    )
    text1.config(highlightbackground="black")
    text1.pack()
    text1.insert(tk.END, "LEADERBOARD")
    text1.config(state=DISABLED)
    count = 0
    text2 = tk.Text(
        window, height=15, width=28, bg="black", fg="white", bd=0,
        font="Helvetica 20"
    )
    text2.config(highlightbackground="black")
    text2.pack()
    text2.insert(tk.END, "NO.     USERNAME          POINTS" + '    \n')

    # sorting dictionary
    listsort = sorted(user_dict.items(), key=lambda kv: (kv[1], kv[0]))
    user_dict.clear()
    for i in range(len(listsort)-1, -1, -1):
        user_dict[listsort[i][0]] = listsort[i][1]

    # displaying ten best
    for i in user_dict:
        if count < 10:
            count += 1
            no = str(count).zfill(3)  # number
            usern = i[:10]            # username
            points = str(user_dict[i]).zfill(3)  # points
            text = no + '\t' + usern + '\t\t ' + points
            text2.insert(tk.END, text)
            text2.insert(tk.END, '\n')
    text2.config(state=DISABLED)   # no typing in the text box


# function for restarting, works only while starting the program from terminal
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


# if boss key is pressed
def boss_key():
    global pause, img, var, click_start
    if click_start == 1:  # only can be enabled when the game is running
        if pause == 0:       # pauses the game and displays the image
            var = PhotoImage(file="boss.ppm")
            img = canvas.create_image(0, 0, anchor=NW, image=var)
            pause = 1
        else:  # the image is deleted and the game is unpaused
            canvas.delete(img)
            pause = 0


# if quit is pressed, the window closes
def quit():
    window.destroy()

# t-additional time from cheats, is going to be updated when shift t is pressed
t = 0
faster = 0          # a counter for knowing if the ball neds to go faster
slower = 0          # a counter for knowing if the ball neds to go slower
restart1 = 0        # if restart was pressed or not
pause = 0           # if pause was pressed or not
click_start = 0     # if start was pressed
direction = ""      # direction for going up or down
points = 0          # points a person has collected so far
points1 = 0         # points that have been loaded from the results file
limit = 0           # limit means if no time is left for a level
ind1 = 0            # if both platforms were destroyed
text = ""           # text for displaying points
window, width, height = window1()  # creating window
usrn = ""           # username
# checking if results file exists, if not, create one with empty dictionary
# if it exists, take the dictionary and make it global
if os.path.isfile('users.pickle'):
    pickle_in = open("users.pickle", "rb")
    user_dict = pickle.load(pickle_in)
    pickle_in.close()
else:
    pickle_out = open("users.pickle", "wb")
    user_dict = dict()
    pickle.dump(user_dict, pickle_out)
    pickle_out.close()

keys()  # binding the keys
text1 = 0  # text for displaying time left
settings()  # settings is called

window.mainloop()
