from cmu_graphics import *
import time as time_module
import os
import sys
import random

def onAppStart(app):
    app.time_in_secs = time_module.time()
    app.time_string = time_module.ctime(app.time_in_secs)

    app.day, app.month, app.date, app.time, app.year = app.time_string.split()

    app.months = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30,
                  'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}

    app.sleepData = {}
    app.selectedDay = None
    app.isSettingSleepStart = False
    app.isSettingSleepEnd = False

    app.dayHighlight = None
    app.hourHighlight = None

    app.notHome = True

    app.stars = [{'x': x, 'y': y, 'opacity': random.randint(10, 96), 'change': random.randint(1, 3)}
                 for x, y in [
                     (100, 100), (200, 50), (300, 120), (400, 80), (600, 150),
                     (700, 100), (850, 50), (50, 200), (250, 300), (400, 250),
                     (550, 350), (700, 400), (850, 300), (150, 450), (300, 400),
                     (500, 500), (650, 450), (900, 550), (1000, 100), (800, 200),
                 ]]
    
def onStep(app):
    for star in app.stars:
        star['opacity'] += star['change']
        if star['opacity'] >= 97 or star['opacity'] <= 10:
            star['change'] *= -1 

def redrawAll(app):
    drawBackground(app)
    drawStarsAndMoon(app)
    drawGrid(app)
    drawSleepLines(app)

    if app.selectedDay is not None:
        drawLabel(f"Selected Day: {int(app.selectedDay)}", app.width // 2, 20, size=16, bold=True, fill='white')
        if app.isSettingSleepStart:
            drawLabel("Click to set sleep time.", app.width // 2, 40, size=12, fill='white')
        elif app.isSettingSleepEnd:
            drawLabel("Click to set wake-up time.", app.width // 2, 40, size=12, fill='white')

    if app.notHome:
        drawImage('home.png', 30, 30, width=30, height=30)
         #image from <https://www.flaticon.com/free-icon/home-button_61972>
    
    drawImage('mood.png', 1030, 750, width=30, height=30)


def drawBackground(app):
    for i in range(0, app.height, 10):
        color = rgb(0, 0, 80 + int(175 * (i / app.height)))  
        drawRect(0, i, app.width, 10, fill=color)

def drawStarsAndMoon(app):
    drawOval(app.width - 130, 200, 80, 80, fill='lightYellow', border=None)
    drawOval(app.width - 120, 190, 60, 60, fill=rgb(0, 0, 115), border=None)

    for star in app.stars:
        drawCircle(star['x'], star['y'], 3, fill='white', opacity=star['opacity'])

def drawGrid(app):
    timeCellWidth = 65
    timeCellHeight = 40
    times = [f"{h} pm" for h in range(8, 12)] + ["12 am"] + [f"{h} am" for h in range(1, 11)]
    for i, hour in enumerate(times):
        x = 100 + i * timeCellWidth
        drawRect(x, 50, timeCellWidth, timeCellHeight, fill=rgb(150, 200, 255) if app.hourHighlight == hour else rgb(100, 150, 200), border='white', borderWidth=1)
        drawLabel(hour, x + timeCellWidth / 2, 50 + timeCellHeight / 2, size=10, fill='white')


    totalDays = app.months[app.month]
    dayCellWidth = 50
    dayCellHeight = (app.height - 50 - timeCellHeight) / totalDays
    for day in range(1, totalDays + 1):
        y = 50 + timeCellHeight + (day - 1) * dayCellHeight
        drawRect(50, y, dayCellWidth, dayCellHeight, fill=rgb(150, 200, 255) if app.dayHighlight == day else rgb(100, 150, 200), border='white', borderWidth=1)
        drawLabel(day, 75, y + dayCellHeight / 2, size=10, fill='white')

def drawSleepLines(app):
    for day, (start, end) in app.sleepData.items():
        if start is not None and end is not None:
            dayY = 50 + 40 + (day - 1) * ((app.height - 50 - 40) / app.months[app.month]) + 10
            startX = 100 + (start - 8) * 65
            endX = 100 + (end - 8) * 65
            drawLine(startX, dayY, endX, dayY, fill='lightBlue', lineWidth=10)
            drawLabel(f"{end - start} hrs", (startX + endX) / 2, dayY, size=10, fill='black', bold=True)

def onMouseMove(app, mouseX, mouseY):
    app.dayHighlight = None
    app.hourHighlight = None

    if 50 <= mouseX <= 100:
        day = (mouseY - 90) // ((app.height - 50 - 40) / app.months[app.month]) + 1
        if 1 <= day <= app.months[app.month]:
            app.dayHighlight = day

    if 100 <= mouseX:
        hour_index = (mouseX - 100) // 65
        times = [f"{h} pm" for h in range(8, 12)] + ["12 am"] + [f"{h} am" for h in range(1, 11)]
        if 0 <= hour_index < len(times):
            app.hourHighlight = times[hour_index]

def onMousePress(app, mouseX, mouseY):
    if 50 <= mouseX <= 100:
        day = (mouseY - 90) // ((app.height - 50 - 40) / app.months[app.month]) + 1
        if 1 <= day <= app.months[app.month]:
            app.selectedDay = day
            app.isSettingSleepStart = True
            app.isSettingSleepEnd = False
            return
        
    if 1030<=mouseX<=1060 and 750<=mouseY<=780:
        scriptPath = '/Users/rishitashah/Downloads/cmu_graphics_installer/moodtracker.py'
        try:
            os.execv(sys.executable, ['python3', scriptPath])
        except Exception as e:
            print(f"Error launching home screen: {e}")

    if 30 <= mouseX <= 60 and 30 <= mouseY <= 60:
        app.notHome = False
        #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
        scriptPath = "/Users/rishitashah/Downloads/cmu_graphics_installer/homescreen"
        try:
            os.execv(sys.executable, ['python3', scriptPath])
        except Exception as e:
            print(f"Error launching home screen: {e}")

    if app.selectedDay is not None and 100 <= mouseX:
        hour_index = (mouseX - 100) // 65
        hour = hour_index + 8
        if app.isSettingSleepStart:
            app.sleepData[app.selectedDay] = (hour, None)
            app.isSettingSleepStart = False
            app.isSettingSleepEnd = True
        elif app.isSettingSleepEnd:
            if app.selectedDay in app.sleepData:
                start, _ = app.sleepData[app.selectedDay]
                app.sleepData[app.selectedDay] = (start, hour)
                app.isSettingSleepEnd = False
                app.selectedDay = None

def main():
    runApp(width=1100, height=800)

main()
