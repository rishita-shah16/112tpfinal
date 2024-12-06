from cmu_graphics import *
import time as time_module
import os
import sys

def onAppStart(app):
    app.width = 1000
    app.height = 800
    app.time_in_secs = time_module.time()
    app.time_string = time_module.ctime(app.time_in_secs)

    app.day, app.month, app.date, app.time, app.year = app.time_string.split()

    app.months = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30,
                  'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}

    app.habits = {'Exercise': [], 'Water': []}  #initial set habits
    app.maxHabits = 9  
    app.notHome = True

    app.currentMonth = app.month  

def resetHabits(app):
    if app.currentMonth != app.month:
        for habit in app.habits:
            app.habits[habit] = []  #clear
        app.currentMonth = app.month 

def redrawAll(app):
    drawImage('bg.jpg', 0, -400, width=app.width, height=app.height+1000) 
    #image is from <https://www.pinterest.com/pin/822610688202898801/>

    # title
    drawRect(0, 0, app.width, 50, fill='orange', opacity=20)
    drawLabel('Habit Tracker', app.width / 2, 25, size=28, bold=True, fill='white', font='Courier New')

    # habit button
    drawAddHabit(app)

    # grid
    xBase = 75  
    yBase = 80
    xChange = 280
    yChange = 240

    resetHabits(app)

    for habitIndex, (habit, completedDays) in enumerate(app.habits.items()):
        if habitIndex >= app.maxHabits:
            break

        x = xBase + (habitIndex % 3) * xChange
        y = yBase + (habitIndex // 3) * yChange


        drawRect(x, y, 250, 200, fill='white', border='red', borderWidth=2)
        drawLabel(habit, x + 125, y + 20, size=18, bold=True, align='center', fill='black', font='Courier New')

        # delete
        drawRect(x + 200, y + 10, 40, 20, fill='lightcoral', border='red', borderWidth=1)
        drawLabel('X', x + 220, y + 20, size=12, bold=True, fill='white')

        for day in range(1, app.months[app.month] + 1):
            dayX = x + ((day - 1) % 7) * 30 + 22.5
            dayY = y + 45 + ((day - 1) // 7) * 30

            fill = 'lightcoral' if day in completedDays else 'white'
            drawRect(dayX, dayY, 25, 25, fill=fill, border='gray', borderWidth=1)
            drawLabel(day, dayX + 12.5, dayY + 12.5, size=10, fill='black')

    # home button
    if app.notHome:
        drawImage('home.png', 30, 750, width=40, height=40)  #image from <https://www.flaticon.com/free-icon/home-button_61972>


def drawAddHabit(app):
    drawRect(800, 10, 170, 40, fill='lightcoral', border='red', borderWidth=2)
    drawLabel('+ Add Habit', 885, 30, bold=True, size=16, fill='white', font='Courier New')

def onMousePress(app, mouseX, mouseY):
    if 800 <= mouseX <= 970 and 10 <= mouseY <= 50:
        if len(app.habits) < app.maxHabits:
            habit = app.getTextInput('Enter a habit to track:')
            if habit and habit not in app.habits:
                app.habits[habit] = []

    
    xBase = 75
    yBase = 80
    xChange = 280
    yChange = 240

    for habitIndex, (habit, completedDays) in enumerate(app.habits.items()):
        if habitIndex >= app.maxHabits:
            break

        x = xBase + (habitIndex % 3) * xChange
        y = yBase + (habitIndex // 3) * yChange

       #deletebutton
        if x + 200 <= mouseX <= x + 240 and y + 10 <= mouseY <= y + 30:
            del app.habits[habit]
            return

        for day in range(1, app.months[app.month] + 1):
            dayX = x + ((day - 1) % 7) * 30 + 10
            dayY = y + 50 + ((day - 1) // 7) * 30

            if dayX <= mouseX <= dayX + 25 and dayY <= mouseY <= dayY + 25:
                if day not in completedDays:
                    completedDays.append(day)  
                else:
                    completedDays.remove(day) 
                return

    if 30 <= mouseX <= 70 and 750 <= mouseY <= 790:
        #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
        app.notHome = False
        scriptPath = "/Users/rishitashah/Downloads/cmu_graphics_installer/homescreen"
        try:
            os.execv(sys.executable, ['python3', scriptPath])
        except Exception as e:
            print(f"Error launching home screen: {e}")

def main():
    runApp(width=1000, height=800)

main()
