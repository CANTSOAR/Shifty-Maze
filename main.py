from flask import Flask, render_template, url_for, request, redirect
from random import random
from time import sleep

app = Flask(__name__)

#makes the initial array where 3s are surrounding walls and 2s are undiscovered cells
def mazearray(s):
    boxes = []
    
    for x in range(s):
        boxes.append([])
        for y in range(s):
            boxes[x].append(2)

    for x in range(s):
        boxes[x][s-1] = 3
        boxes[x][0] = 3
    for y in range(s):
        boxes[0][y] = 3
        boxes[s-1][y] = 3

    return boxes

#helper function for when i needed to print out a maze, and highlight the path and walls created
def printmaze(arr):
    for x in range(len(arr)):
        thing = ""
        for y in range(len(arr[0])):
            if arr[x][y] == 0:
                thing += "\033[92m"

            if arr[x][y] == 1:
                thing += "\033[91m"

            thing += str(arr[x][y]) + "\033[0m  "
        print(thing)
    print()

#4th attempt at making the maze, this one works by starting at a random spot and bridging out
def mazepath(s, x = 0, y = 0, new = True):

    boxes = mazearray(s)

    current = [x, y]

    if x == 0 and y == 0:
        x = int(random()*(len(boxes) - 4) + 2)
        y = int(random()*(len(boxes) - 4) + 2)

    boxes[x][y] = 0
    boxes[x - 1][y] = 1
    boxes[x + 1][y] = 1
    boxes[x][y - 1] = 1
    boxes[x][y + 1] = 1

    walls = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
    
    for wall in walls:
        if wall[0] in [0, len(boxes) - 1] or wall[1] in [0, len(boxes) - 1]:
            boxes[wall[0]][wall[1]] = 3
            walls.remove(wall)

    print(x, y, walls)

    while len(walls) > 0:
        start = int(random()*len(walls))

        x = walls[start][0]
        y = walls[start][1]

        choices = [[-1, 0], [0, -1], [0, 1], [1, 0]]

        used = False

        for choice in choices:
            if boxes[x + choice[0]][y + choice[1]] >= 2 and boxes[x - choice[0]][y - choice[1]] == 0 and pathcheck(boxes, x, y):
                used = True

                boxes[x][y] = 0
                
                del(walls[start])

                newwalls = [boxes[x + choice[0]][y + choice[1]], boxes[x + choice[1]][y + choice[0]], boxes[x - choice[1]][y - choice[0]]]
                newwallcoords = [[x + choice[0], y + choice[1]], [x + choice[1], y + choice[0]], [x - choice[1], y - choice[0]]]

                for n in range(3):
                    if newwalls[n] == 2:
                        newwalls[n] = 1

                    if newwalls[n] == 1 and newwallcoords[n] not in walls:
                        walls.append(newwallcoords[n])

                boxes[x + choice[0]][y + choice[1]] = newwalls[0]
                boxes[x + choice[1]][y + choice[0]] = newwalls[1]
                boxes[x - choice[1]][y - choice[0]] = newwalls[2]

        if not used:    
            del(walls[start])

    if new:
        for x in range(len(boxes)):
            if boxes[x][1] == 0:
                boxes[x][0] = 6
                current = [x, 0]
                break

    else:
        boxes[current[0]][current[1]] = 6

    for x in range(len(boxes)):
            if boxes[len(boxes) - 1 - x][len(boxes) - 2] in [0, 6]:
                boxes[len(boxes) - 1 - x][len(boxes) - 1] = 7
                break

    return boxes, current

#given the maze and a specific spot, returns true if there are no open spaces already near the spot, which makes sure there arnt any big pockets
def pathcheck(boxes, x, y):

    check = 0

    choices = [[-1, 0], [0, -1], [0, 1], [1, 0]]

    for choice in choices:
        if boxes[x + choice[0]][y + choice[1]] == 0:
            check += 1
    
    if check > 1:
        return False

    return True
    
#movement function
def move(boxes, direction, current):

    alldirections = ["left", "right", "up", "down"]

    side = alldirections.index(direction)

    choices = [[0, -1], [0, 1], [-1, 0], [1, 0]]

    x = current[0]
    y = current[1]

    if y > 0 and boxes[x + choices[side][0]][y + choices[side][1]] not in range(1, 4):
        current = [x + choices[side][0], y + choices[side][1]]
    elif y == 0 and side == 1:
        current = [x + choices[side][0], y + choices[side][1]]

    boxes[x][y] = 8
    boxes[current[0]][current[1]] = 6

    if current[1] == len(boxes) - 1:
        if len(boxes) > 100:
            factor = 5
        elif len(boxes) < 100:
            factor = 1
        else:
            factor = 4

        for x in range(25 * factor):
            for y in range(25 * factor):
                boxes[x][y] = 0

        colstuff = [list(range(10 * factor, 14 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(14 * factor, 15 * factor)) + list(range(21 * factor, 22 * factor)),
                    list(range(3 * factor, 8 * factor)) + list(range(12 * factor, 14 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(5 * factor, 6 * factor)) + list(range(14 * factor, 15 * factor)),
                    list(range(3 * factor, 8 * factor)) + list(range(10 * factor, 14 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(17 * factor, 18 * factor)) + list(range(19 * factor, 20 * factor)),
                    list(range(4 * factor, 8 * factor)) + list(range(11 * factor, 15 * factor)) + list(range(17 * factor, 19 * factor)) + list(range(20 * factor, 22 * factor)),
                    list(range(3 * factor, 4 * factor)) + list(range(5 * factor, 6 * factor)) + list(range(10 * factor, 11 * factor)) + list(range(12 * factor, 13 * factor)),
                    list(range(4 * factor, 8 * factor)) + list(range(11 * factor, 15 * factor)),
                    [],
                    list(range(10 * factor, 13 * factor)) + list(range(14 * factor, 15 * factor)) + list(range(17 * factor, 18 * factor)),
                    list(range(10 * factor, 11 * factor)) + list(range(12 * factor, 13 * factor)) + list(range(14 * factor, 15 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(3 * factor, 6 * factor)) + list(range(10 * factor, 11 * factor)) + list(range(12 * factor, 15 * factor)) + list(range(17 * factor, 18 * factor)),
                    list(range(6 * factor, 8 * factor)),
                    list(range(3 * factor, 6 * factor)) + list(range(10 * factor, 11 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(10 * factor, 15 * factor)),
                    list(range(3 * factor, 8 * factor)) + list(range(10 * factor, 11 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(3 * factor, 4 * factor)) + list(range(7 * factor, 8 * factor)) + list(range(18 * factor, 19 * factor)),
                    list(range(3 * factor, 8 * factor)) + list(range(10 * factor, 15 * factor)) + list(range(19 * factor, 20 * factor)),
                    list(range(10 * factor, 11 * factor)) + list(range(12 * factor, 13 * factor)) + list(range(14 * factor, 15 * factor)) + list(range(18 * factor, 19 * factor)),
                    list(range(3 * factor, 8 * factor)) + list(range(10 * factor, 11 * factor)) + list(range(14 * factor, 15 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(7 * factor, 8 * factor)),
                    list(range(3 * factor, 8 * factor)) + list(range(10 * factor, 15 * factor)) + list(range(17 * factor, 22 * factor)),
                    list(range(10 * factor, 11 * factor)) + list(range(14 * factor, 15 * factor)) + list(range(17 * factor, 18 * factor)) + list(range(19 * factor, 20 * factor)) + list(range(21 * factor, 22 * factor)),
                    list(range(11 * factor, 14 * factor)) + list(range(17 * factor, 18 * factor)) + list(range(21 * factor, 22 * factor))
                    ]

        for col in range(len(colstuff)):
            for x in colstuff[col]:
                for y in range(factor * col,factor * (col + 1)):
                    boxes[x][y] = 1

        # for x in range(100 * factor):
        #     for y in range(100 * factor):
        #         if x in list(range(12 * factor, 32 * factor)) + list(range(40 * factor, 60 * factor)) + list(range(68 * factor, 88 * factor)) and y not in list(range(36 * factor, 40 * factor)):
        #             print(x, y)
        #             boxes[x][y] = 1
        #         else:
        #             boxes[x][y] = 0

    return boxes, current

#various attempts to make the make work, feel free to check them out if u want
'''def pathcheck(boxes, x, y, old = []):
    check = 0

    print('start', x, y, old)

    if [x, y] == [1, 1]:
        print('returning true')
        return True

    choices = [[-1, 0], [0, -1], [0, 1], [1, 0]]
    old.append([x, y])

    new = []

    for choice in choices:
        current = [x + choice[0], y + choice[1]]

        if current in old:
            check -= 1

        if boxes[x + choice[0]][y + choice[1]] == 0:
            check += 1

            if current not in old:
                new.append(current)
    
    if check >= 1:
        for coord in new:
            print(coord)
            print('recursing')
            return pathcheck(boxes, coord[0], coord[1], old)
    
    print('returning false')
    return False

def mazepath():
    boxes = mazearray()
    check = mazearray()

    for a in range(200):
        x, y, = randrange(1, 24), randrange(1, 24)

        check[x][y] = 1

        if boxes[x][y] == 0:
            if pathcheck(boxes, x, y, []):
                boxes[x][y] = 1

    printmaze(check)

    return boxes

def mazepath():
    boxes = mazearray()
    done = False
    z = 0

    while z in range(100):
        x, y = randrange(1, 24), randrange(1, 24)
        old = []
        c = 0

        tempdone = False

        while not tempdone:
            print(x, y, c, old)

            if boxes[x][y] == 0 and checkwalls(boxes, x, y, old):
                boxes[x][y] = 1

                old.append([x, y])

                direction = randrange(4)

                if direction == 0:
                    x += 1
                elif direction == 1:
                    x -= 1
                elif direction == 2:
                    y += 1
                else:
                    y -= 1
            else:
                tempdone = True
            c += 1

        z += 1

    return boxes

def checkwalls(boxes, x, y, old = []):
    
    check = 0

    choices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    for choice in choices:
        current = [x + choice[0], y + choice[1]]

        if current in old:
            check += 1

        if boxes[x + choice[0]][y + choice[1]] == 0:
            check += 1
    
    if check >= 5:
        return True
    
    return False

def mazepath():
    boxes = mazearray()
    x, y = 0, 0

    while boxes[24][24] == 1:
        boxes[x][y] = 0

        xory = randrange(6)

        if xory == 0 and x > 0:
            x -= 1
        elif xory > 3 and x < len(boxes) - 1:
            x += 1
        elif xory == 1 and y > 0:
            y -= 1
        elif y < len(boxes[0]) - 1:
            y += 1

    return boxes'''
    
#main page
@app.route("/")
def home():
    return render_template("main.html")

#practicing using flask with some random stuff
'''
@app.route("/home")
def form():
    return render_template("form.html")

@app.route("/hello/<name>")
def name(name):
    return "Hello " + name

@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "POST":
        form = request.form
        return render_template("data.html", form_data = form)
    return "plz fill out the form"
'''

@app.route("/maze", methods=["GET", "POST"])
def maze():
    if request.method == "GET":
        return redirect(url_for("home"))

    #very primitive attempt to make the maze
    """for x in range(25):
        for y in range(25):
            if boxes[x][y] == 1:
                boxes[x][y] = randrange(6)"""

    diff = request.form

    for key in diff:
        if key == "idek if this works":
            maze = mazepath(25)
            boxwidth = 20
        elif key == "Eh":
            maze = mazepath(100)
            boxwidth = 5
        elif key == "Yeah Ok Good Luck Bud":
            maze = mazepath(500)
            boxwidth = 1
        else:
            premaze = []
            inrow = False
            row = -1
            current = []

            for char in key[2:-9]:
                if char == "[":
                    inrow = True
                    premaze.append([])
                    row += 1
                 
                elif char == "," or char == " ":
                    pass

                elif char == "]":
                    inrow = False

                elif inrow:
                    premaze[row].append(int(char))
            
            x = 0
            keyfind = ""

            while keyfind != "[":
                x += 1
                keyfind = key[-1 * x]

            isnum = False

            for char in key[-1 * x:]:
                if isnum:
                    if char not in ["[", ",", " ", "]"]:
                        current[-1] = current[-1] * 10 + int(char)
                    else:
                        isnum = False
                elif char not in ["[", ",", " ", "]"]:
                    isnum = True
                    current.append(int(char))

            maze = move(premaze, diff[key], current)

            if len(premaze) == 25 and current != maze[1] and maze[1][1] != len(premaze) - 1:
                maze = mazepath(25, maze[1][0], maze[1][1], False)

            boxwidth = 500 / len(maze[0])

            if boxwidth > 10:
                diff = {"oh, maybe it does": ";)"}
            elif boxwidth > 1:
                diff = {"Eh": "if you are reading this ur cool"}
            else:
                diff = {"cool ig u made a move": "hi"}

    boxes = maze[0]
    current = maze[1]

    return render_template("maze.html", boxes=boxes, diff=diff, boxwidth=boxwidth, current=current)

#starting webapp
if __name__ == "__main__":
   app.run(debug=True)