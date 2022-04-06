
from cmu_112_graphics import *
from run_pitch_main import runPitch
from Mechanics import *
import random

def appStarted(app):
    url = 'baseball_sprite.png'
    spritestrip = app.loadImage(url)
    app.sprites = [ ]

    sprite = spritestrip.crop((0, 0, 100, 234))
    app.sprites.append(sprite)

    sprite = spritestrip.crop((100, 0, 195, 244))
    app.sprites.append(sprite)
    
    sprite = spritestrip.crop((192, 0, 297, 244))
    app.sprites.append(sprite)

    sprite = spritestrip.crop((295, 0, 385, 244))
    app.sprites.append(sprite)

    sprite = spritestrip.crop((380, 0, 525, 244))
    app.sprites.append(sprite)

    sprite = spritestrip.crop((527, 0, 670, 244))
    app.sprites.append(sprite)

    sprite = spritestrip.crop((668, 0, 762, 244))
    app.sprites.append(sprite)

    sprite = spritestrip.crop((750, 0, 890, 244))
    app.sprites.append(sprite)

    app.initialScreen = True
    app.grassColor = "green4"
    app.pitchDist = 60.5
    app.timerDelay = 30
    app.spriteCounter = 0
    app.runSprite = True
    app.pitch = False
    app.timeTrack = 0
    app.pitchIndex = 0
    app.field = Field([], 0, 70)

    app.pitchTrajectory = None
    app.feetToPixelScalar = 10
    app.homePlateWidth = 17.5 * app.feetToPixelScalar #17.5 inches times scalar 10, denoting that each inch represents 10 pixels
    app.ballStartRadius = 5 #pixels
    app.ballHit = False
    app.hitIndex = 0


    app.ball = Ball(Vector(0, 6, 60.5)) # 

    app.plateDistance, app.strikeHeight = runPitch()

    pitch_spin_axis = {1: Vector(1, 0, 0).norm(), # "curve ball"
    2: Vector(-1, 0, 0).norm(), # "fastball
    3: Vector(1, 3, 0), # "slider"
    4: Vector(-3, 2, 0), # "change up"
    5: Vector (-2, 1, 0)} # "sinker"

    #index = random.randint(1, 5)
    index = 2
    pitch_velocity = {
        1: Vector(0, 7, -115),
        2: Vector(0, 1, -125),
        3: Vector(-3, 7, -115),
        4: Vector(-2, 3, -110),
        5: Vector(-2, 2, -125)
    }

    print("index:", index)
    #app.hit = Hit(app.swing, )
    app.pitch = Pitch(pitch_velocity[index], pitch_spin_axis[index]) # Pitch((0, 2, -130), Vector(-1, 0, 0))


    app.pitchTrajectory = getPitchTrajectory(app.ball, app.pitch, app.timerDelay)
    #call greg's function with the pitchVector and set pitch Trajectory equal to it





    app.swing = Swing(app.strikeHeight, app.plateDistance)

    contact_ball_tuple = app.pitchTrajectory[-1]
    x, y, z = contact_ball_tuple

    app.ball_contact = Ball(Vector(x, y, z))
    print(app.ball.pos.getComponents())
    if abs(app.swing.height - Vector(x, y, z).y) > app.swing.bat_radius:
        app.hit = None
    else:
        app.hit = Hit(app.swing, app.ball_contact)
        app.ballHitTrajectory = getHitTrajectory(app.field, app.hit, app.ball_contact, timerDelay)
    print("yo:", app.hit)
    


def timerFired(app):
    if app.runSprite:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    if app.spriteCounter == 7:
        app.pitch = True
        app.runSprite = False
    if app.pitch:
        app.pitchIndex += 1
    if app.pitchTrajectory != None and app.pitchIndex >= len(app.pitchTrajectory) and app.hit != None:
        app.pitch = False
        app.runSprite = False
        app.initialScreen = False
        app.ballHit = True
        app.hitIndex += 1
        app.numBallMovements = len(app.ballHitTrajectory)


def keyPressed(app, event):
   pass

def pitchFindPixelFromFeet(app, x, y, z):
    minimumBoundAdjustor = 0.1
    minimumBounds = {"topBound": app.height/3 - app.height*minimumBoundAdjustor,
                         "lowerBound": app.height/3 + app.height*minimumBoundAdjustor,
                         "leftBound": app.width/2 - app.width*minimumBoundAdjustor,
                         "rightBound": app.width/2 + app.width*minimumBoundAdjustor}
    topBound = minimumBounds["topBound"] - ((60.5 - z)/app.pitchDist)*(minimumBounds["topBound"])
    lowerBound = minimumBounds["lowerBound"] + ((60.5 - z)/app.pitchDist)*(app.height - minimumBounds["lowerBound"])
    leftBound = minimumBounds["leftBound"] - ((60.5 - z)/app.pitchDist)*(minimumBounds["leftBound"])
    rightBound = minimumBounds["rightBound"] + ((60.5 - z)/app.pitchDist)*(app.width - minimumBounds["rightBound"])
    cy = lowerBound - (lowerBound - topBound) * (y / 10)
    boundWidth = rightBound - leftBound
    cx = app.width/2 + boundWidth * (-x / 10)
    radius = app.ballStartRadius + ((60.5 - z) / 60.5) * 10
    x0 = cx - radius
    x1 = cx + radius
    y0 = cy - radius
    y1 = cy + radius
    return (x0, y0, x1, y1)

def hitFindPixelFromFeet(app, x, y, z):
    cx = app.width/2 + app.width * (-x / 300)
    cy = app.height - 30 - app.height * (z / 300)
    radius = app.ballStartRadius + y
    x0 = cx + radius
    x1 = cx - radius
    y0 = cy + radius
    y1 = cy - radius
    return (x0, y0, x1, y1)

def drawStrikeZone(app, canvas):
    x0 = app.width/2 - 60
    x1 = app.width/2 + 60
    y0 = 2*app.height/3 + 75
    y1 = 2*app.height/3 - 75
    canvas.create_rectangle(x0, y0, x1, y1)

def redrawAll(app, canvas):
    sprite = app.sprites[app.spriteCounter]
    if app.initialScreen:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = app.grassColor)
        canvas.create_image(app.width/2, app.height/3, image=ImageTk.PhotoImage(sprite))
        drawStrikeZone(app, canvas)
    if app.runSprite:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = app.grassColor)
        canvas.create_image(app.width/2, app.height/3, image=ImageTk.PhotoImage(sprite))
        drawStrikeZone(app, canvas)
    if app.pitch and app.pitchIndex < len(app.pitchTrajectory):
        (x, y, z) = app.pitchTrajectory[app.pitchIndex]
        x0, y0, x1, y1 = pitchFindPixelFromFeet(app, x, y, z)
        canvas.create_oval(x0, y0, x1, y1, fill = "black")
        drawStrikeZone(app, canvas)
    if not app.pitch and app.hit == None:
        print("yo")
        canvas.create_text(app.width/2, app.height/2, text = "You Missed!")
    if app.ballHit and app.hitIndex < app.numBallMovements and app.hit != None:
        canvas.create_rectangle(0, 0, app.width, app.height, fill=app.grassColor)
        # home plate
        canvas.create_line(app.width/2 - 10, app.height - 40, app.width/2 + 10, app.height - 40)
        canvas.create_line(app.width/2 - 10, app.height - 20, app.width/2 - 10, app.height - 40)
        canvas.create_line(app.width/2 + 10, app.height - 20, app.width/2 + 10, app.height - 40)
        canvas.create_line(app.width/2 - 10, app.height - 20, app.width/2, app.height - 10)
        canvas.create_line(app.width/2 + 10, app.height - 20, app.width/2, app.height - 10)
        # first & third base
        canvas.create_rectangle(3*app.width/4, 3*app.height/4 - 10, 3*app.width/4 + 20, 3*app.height/4 - 30, fill="white")
        canvas.create_rectangle(app.width/4, 3*app.height/4 - 10, app.width/4 - 20, 3*app.height/4 - 30, fill="white")
        # second base
        canvas.create_rectangle(app.width/2 - 10, app.height/2, app.width/2 + 10, app.height/2 - 20, fill="white")
        canvas.create_oval(-app.width/4, 0, app.width + app.width/4, app.height + app.height/4)
        (x, y, z) = app.ballHitTrajectory[app.hitIndex]
        x0, y0, x1, y1 = hitFindPixelFromFeet(app, x, y, z)
        if y <= 0.1:
            color = "red"
        else:
            color = "black"
        canvas.create_oval(x0, y0, x1, y1, fill = color)

def runAnimation():
    runApp(width=1280, height=720)