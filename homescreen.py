from cmu_graphics import *
import os
import sys


def onAppStart(app):
    #walking animation
    # i used chat gpt to generate these walking frames
    app.forwardWalkFrames = ["walk1.png", "walk2.png", "walk3.png"]
    app.backwardWalkFrames = ["walk4.png", "walk5.png", "walk6.png"]

    app.currentFrame = 0  
    app.frameDelay = 5   
    app.stepCount = 0  

    #starting dog position app.width/2 - dog width/2
    app.dogX = 540
    app.dogY = 464

    app.move = 10
    app.roomBounds = {"left": 100, "right": 900, "top": 100, "bottom": 700}
    app.furniture = {
        "bed": (630, 160, 300, 150),          
        "coffee table": (150, 150, 150, 150), 
        "couch": (650, 610, 280, 150),
        "desk": (125, 565, 200, 200)
    }

    app.highlight = {
        'couch': (600, 540, 280, 150),
        'bed': (590, 108, 300, 150),
        'desk': (108, 490, 200, 200),
        'coffee table': (120, 108, 150, 150) 
    }

    app.isMoving = False 
    app.notHome = False
    app.selectedFurniture = None
    app.hoveredFurniture = None

    app.facingLeft = False

def onKeyHold(app, keys):
    x, y = app.dogX, app.dogY
    app.isMoving = False

    if 'up' in keys:
        app.dogY -= app.move
        app.isMoving = True
    if 'down' in keys:
        app.dogY += app.move
        app.isMoving = True
    if 'left' in keys:
        app.dogX -= app.move
        app.isMoving = True
        app.facingLeft = True
    if 'right' in keys:
        app.dogX += app.move
        app.isMoving = True
        app.facingLeft = False

    #check if colliding with furniture or if leaves the room
    if isColliding(app, app.dogX, app.dogY) or not isInsideRoom(app, app.dogX, app.dogY):
        app.dogX, app.dogY = x, y  #doesn't move past the original x,y

def onMousePress(app, mouseX, mouseY):
    if app.notHome:
        if 400 <= mouseX <= 600 and 450 <= mouseY <= 500:
            app.notHome = False
        return

    for name, (x, y, width, height) in app.furniture.items():
        if x <= mouseX <= x + width and y <= mouseY <= y + height:
            app.notHome = True
            app.selectedFurniture = name
            #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
            scriptPath = f"/Users/rishitashah/Downloads/cmu_graphics_installer/{app.selectedFurniture}.py"
            try:
                os.execv(sys.executable, ['python3', scriptPath])
            except FileNotFoundError:
                print(f"Error: Script {scriptPath} not found.")
            return

def onStep(app):
    if app.isMoving:
        app.stepCount += 1
        if app.stepCount % app.frameDelay == 0:
            app.currentFrame = (app.currentFrame + 1) % 3
    else:
        app.currentFrame = 0 

    app.isMoving = False

def onMouseMove(app, mouseX, mouseY):
    for name, (x, y, width, height) in app.furniture.items():
        if x <= mouseX <= x + width and y <= mouseY <= y + height:
            app.hoveredFurniture = name
            break
        app.hoveredFurniture = None

def redrawAll(app):
    drawLabel('112 Bullet Journal', app.width/2, 50, size=30, font='Courier New')
    #drawing the map
    # i used chat gpt to generate these images
    drawImage('floor.png', 100, 100, width=800, height=600)
    drawImage('couch.png', 600, 540, width=280, height=150)
    drawImage('bed.png', 590, 108, width=300, height=150)
    drawImage('desk.png', 108, 490, width=200, height=200)
    drawImage('coffee table.png', 120, 108, width=150, height=150)

    if app.hoveredFurniture:
        x, y, width, height = app.highlight[app.hoveredFurniture]
        drawRect(x, y, width, height, fill=None, border='yellow', borderWidth=3)

    #draw the dog at the frame
    if app.facingLeft:
        currentImage = app.backwardWalkFrames[app.currentFrame]
    else:
        currentImage = app.forwardWalkFrames[app.currentFrame]
    
    drawImage(currentImage, app.dogX - 80, app.dogY - 128, width=80, height=128)

def isColliding(app, x, y):
    dogWidth, dogHeight = 80, 128 
    for furniture, (fX, fY, fWidth, fHeight) in app.furniture.items():
        if (x - dogWidth / 2 < fX + fWidth and x + dogWidth / 2 > fX and
            y - dogHeight / 2 < fY + fHeight and y + dogHeight / 2 > fY):
            return True
    return False

def isInsideRoom(app, x, y):
    dogWidth, dogHeight = 80, 128 
    return (app.roomBounds["left"] <= x - dogWidth and
            x <= app.roomBounds["right"] and
            app.roomBounds["top"] <= y - dogHeight and
            y <= app.roomBounds["bottom"])

runApp(width=1000, height=800)