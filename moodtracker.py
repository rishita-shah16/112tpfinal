from cmu_graphics import *
import time as time_module
import math
import random
import os
import sys


def onAppStart(app):
    app.time_in_secs = time_module.time()
    app.time_string = time_module.ctime(app.time_in_secs)

    app.day, app.month, app.date, app.time, app.year = app.time_string.split()

    app.months = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30,
                  'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}
    
    app.numberPolygons = app.months[app.month]

    app.emotions = {
        'blue': 'sad', 'orange': 'happy', 'green': 'sick',
        'pink': 'neutral', 'red': 'angry', 'purple': 'anxious'
    }
    app.selectedColor = None
    app.colors = dict()  
    app.lineLengths = {i: random.randint(50, 300) for i in range(1, app.numberPolygons + 1)}  # diff lengths for each day
    app.notHome=True

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=gradient('white', 'orange'), opacity=30)
    bigX, bigY, bigR = 500, 500, 100
    drawCircle(bigX, bigY, bigR, fill=gradient('blue', 'white'), border='black', borderWidth=1)
    drawLabel('Mood Tracker', bigX, bigY, size=20, font='Courier New', bold=True)
    
    for i in range(1, app.numberPolygons + 1):
        angle = (2 * math.pi / app.numberPolygons) * i
        smallR = 20
        smallCX = bigX + bigR * math.cos(angle)
        smallCY = bigY + bigR * math.sin(angle)
        lenLine = app.lineLengths[i]
        endLineX = smallCX + lenLine * math.cos(angle)
        endLineY = smallCY + lenLine * math.sin(angle)

        
        drawLine(smallCX, smallCY, endLineX, endLineY, lineWidth=1)

        circleColor = app.colors.get(i, 'white')
        drawCircle(endLineX+20*math.cos(angle), endLineY+20*math.sin(angle), smallR, fill=circleColor, border='black', borderWidth=1, opacity=40)

        drawLabel(i, endLineX+20*math.cos(angle), endLineY+20*math.sin(angle), size=16, font='Courier New')
    
    if app.notHome:
        drawImage('home.png', 30, 30, width=30, height=30)
         #image from <https://www.flaticon.com/free-icon/home-button_61972>

    drawColorBank(app)

def drawColorBank(app):
    drawRect(1000, 100, 400, 800, fill=None, border='black', borderWidth=1)
    count = 1
    for color, emotion in app.emotions.items():
        y = 100 + count * (600 / len(app.emotions))
        drawRect(1050, y, 50, 50, fill=color, border='black', borderWidth=1, opacity=40)
        drawLabel(emotion, 1200, y + 25, size=20, font='Courier New', align='left')
        count += 1

def onMousePress(app, mouseX, mouseY):
    for count, (color, emotion) in enumerate(app.emotions.items(), start=1):
        y = 100 + count * (600 / len(app.emotions))
        if 1050 <= mouseX <= 1100 and y <= mouseY <= y + 50:
            app.selectedColor = color
            return 
        
    if app.selectedColor:
        for i in range(1, app.numberPolygons + 1):
            angle = (2 * math.pi / app.numberPolygons) * i
            smallCX = 500 + 100 * math.cos(angle)
            smallCY = 500 + 100 * math.sin(angle)
            lenLine = app.lineLengths[i]
            endLineX = smallCX + lenLine * math.cos(angle)
            endLineY = smallCY + lenLine * math.sin(angle)

            if distance(mouseX, mouseY, endLineX, endLineY) <= 20:
                app.colors[i] = app.selectedColor
                return
    
    if 30 <= mouseX <= 60 and 30 <= mouseY <= 60:
        app.notHome = False
        #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
        scriptPath = "/Users/rishitashah/Downloads/cmu_graphics_installer/homescreen"
        try:
            os.execv(sys.executable, ['python3', scriptPath])
        except Exception as e:
            print(f"Error launching home screen: {e}")

def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def main():
    runApp(width=3000, height=800)

main()
