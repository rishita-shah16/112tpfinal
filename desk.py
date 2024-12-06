from cmu_graphics import *
import time as time_module
#found this time module from <https://www.geeksforgeeks.org/python-calendar-module/>
#found its functions from <https://docs.python.org/3/library/calendar.html>
import os #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
import sys #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
import random

def onAppStart(app):
    app.width=1000
    app.height=800
    app.rows = 5
    app.cols = 7
    app.boardTop = 50
    app.cellSize = 80
    app.boardLeft = app.width/2-(app.cellSize*7/2)
    app.cellBorderWidth = 1
    app.time_in_secs = time_module.time()
    app.time_string = time_module.ctime(app.time_in_secs)
    
    app.day, app.month, app.date, app.time, app.year = app.time_string.split()
   
    app.months = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30,
          'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}

    app.days = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}

    app.startCell = (app.days[app.day] - (int(app.date) % 7)) % 7
    print(app.startCell)
    
    app.events = dict()
    app.selectedDate = None

    app.toDoList = dict()

    app.boxesTopLeft = []
    app.checkedBoxes = []

    app.notHome = True
    app.hoverCell = None

    app.clickedInput = False
    app.input = ''
    app.isTyping = False
    app.savedInput = []

    app.toDo = False
    app.inputName = ''
    app.inputDuration = ''
    app.inputSlots = ''
    app.selectedDay = None
    app.focusField = None 
    #app.availableSlots = {day: [] for day in app.days} 
    app.calendarInput = False

    app.scheduledTasks = {day.upper(): [] for day in app.days}  # To store scheduled tasks for each day
    app.availableSlots = {day.upper(): ["09:00-23:00"] for day in app.days}
    app.displayScheduled=False
    
def onStep(app):
    app.time_in_secs = time_module.time()
    app.time_string = time_module.ctime(app.time_in_secs)

def drawBackground(app):
    if 6 <= int(app.time.split(':')[0]) < 18:  # Daytime
        drawRect(0, 0, app.width, app.height, fill='skyBlue', opacity=20)
        drawImage('sun.png', app.width - 160, 50, width=120, height=100) 
        # image from <gallery.yopriceville.com>
    else:  # Nighttime
        drawRect(0, 0, app.width, app.height, fill='darkBlue', opacity=20)
        drawImage('moon.png', app.width - 160, 50, width=100, height=100)
        #image from <https://www.vecteezy.com/free-png/3d-crescent-moon>
        for _ in range(50):
            x, y = random.randint(0, app.width), random.randint(0, app.height)
            drawCircle(x, y, 2, fill='white')

    
def redrawAll(app):
    drawBackground(app)
    drawLabel(f'{app.time_string}', app.width/2, 30, size=18)
    drawBoard(app)
    drawBoardBorder(app)
    drawDates(app)
    drawToDo(app)
    if app.notHome:
        drawImage('home.png', 30, 30, width=30, height=30)
        #image from <https://www.flaticon.com/free-icon/home-button_61972>

    if app.clickedInput:
        drawRect(app.width/2-150, app.height/2-150, 300, 300, fill='pink')
        drawRect(app.width/2-100, app.height/2-25, 200, 50, fill=gradient('white', 'lightGray', start='top'), border='black', borderWidth=1)
        drawLabel(f'Enter an event for {app.month} {int(app.selectedDate)}', app.width / 2, app.height / 2-50, fill='black', size=20)
        if not app.isTyping:
            drawLabel('type here...', app.width/2-40, app.height/2, fill='gray', size=18)
        else:
            drawLabel(app.input, app.width/2-90, app.height/2, size=15, align='left')
        
        drawRect(app.width/2-50, app.height/2+40, 100, 30, fill='lightgray', border='black', borderWidth=1)
        drawLabel('save', app.width/2, app.height/2+55)

        drawRect(app.width / 2 + 110, app.height / 2 - 140, 30, 30, fill='red')
        drawLabel('X', app.width / 2 + 125, app.height / 2 - 125, size=18, fill='white')

    if app.displayScheduled: 
        displayScheduledTasks(app)

    if app.toDo == True:
        drawTaskInput(app)
    
    drawLabel('click * for an automated task scheduler!', 15, 780, align='left', size=16)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.cellSize*app.cols, app.cellSize*app.rows,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    if app.hoverCell == (row, col):
        drawRect(cellLeft, cellTop, app.cellSize, app.cellSize, fill='green', opacity=20)
    else:
        drawRect(cellLeft, cellTop, app.cellSize, app.cellSize,  fill='pink', opacity=20, border='black', borderWidth=1)

def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellSize
    cellTop = app.boardTop + row * app.cellSize 
    return (cellLeft, cellTop)

def drawEventLabels(app, date, left, top):
    eventY = top + 30
    for event in app.events[date]:
        drawLabel(event, left + app.cellSize / 2, eventY, size = 10)
        eventY += 15 

def drawDates(app):
    num = 1    
    for col in range(app.startCell, app.cols):
        left, top = getCellLeftTop(app, 0, col)
        if num <= app.months[app.month]:
            if num == int(app.date):
                drawRect(left+1, top+1, 18, 19, fill='green', opacity=20)
            drawLabel(f'{num}', left+9, top+10)
            if num in app.events:
                for event in app.events[num]:
                    drawEventLabels(app, num, left, top)
        num += 1
   
    
    for row in range (1, app.rows):
        for col in range(0, app.cols):
            left, top = getCellLeftTop(app, row, col)
            if num <= app.months[app.month]:
                if num == int(app.date):
                    drawRect(left+1, top+1, 18, 19, fill='green', opacity=20)
                drawLabel(f'{num}', left+9, top+10)
                if num in app.events:
                    for event in app.events[num]:
                        drawEventLabels(app, num, left, top)
                num += 1
        
#inserting events:
def findCell(app, x, y):
    if (app.boardLeft <= x <= app.boardLeft + app.cols*app.cellSize) and (app.boardTop <= y <= app.boardTop + app.rows*app.cellSize):
           row = (y - app.boardTop) // app.cellSize
           col = (x - app.boardLeft) // app.cellSize
           return (row, col)
    return (None, None)

def displayScheduledTasks(app):
    displayWidth = 600
    displayHeight = 400
    displayLeft = app.width / 2 - displayWidth / 2
    displayTop = app.height / 2 - displayHeight / 2

    drawRect(displayLeft, displayTop, displayWidth, displayHeight, fill='white', border='black')
    drawLabel("Scheduled Tasks", app.width / 2, displayTop + 30, size=20, bold=True)

    closeButtonSize = 30
    drawRect(displayLeft + displayWidth - closeButtonSize - 10, displayTop + 10, closeButtonSize, closeButtonSize, fill='red', border='black')
    drawLabel('X', displayLeft + displayWidth - closeButtonSize / 2 - 10, displayTop + 25, size=18, fill='white')

    y = displayTop + 60
    for day, tasks in app.scheduledTasks.items():
        drawLabel(f"{day}:", displayLeft + 20, y, size=16, bold=True, align='left')
        y += 30
        for task in tasks:
            start = formatTime(task['start'])
            end = formatTime(task['end'])
            drawLabel(f"{task['name']} ({start} - {end})", displayLeft + 40, y, size=14, align='left')
            y += 25
        y += 10
    
def onMousePress(app, mouseX, mouseY): 
    listTop = app.boardTop + app.cellSize * app.rows + 20 
    listWidth = app.width - 200  
    listLeft = app.width / 2 - listWidth / 2 
    dayWidth = listWidth // 7 

    #handles the x in scheduled tasks
    if app.displayScheduled:
        displayWidth = 600
        displayHeight = 400
        displayLeft = app.width / 2 - displayWidth / 2
        displayTop = app.height / 2 - displayHeight / 2
        closeButtonSize = 30
        if (displayLeft + displayWidth - closeButtonSize - 10 <= mouseX <= displayLeft + displayWidth - 10 and
            displayTop + 10 <= mouseY <= displayTop + 10 + closeButtonSize):
            app.displayScheduled = False  # Close the scheduled tasks display
            return

    for i, day in enumerate(app.days.keys()):
        dayLeft = listLeft + i * dayWidth
        dayRight = dayLeft + dayWidth
        dayTop = listTop
        dayBottom = listTop + 40 

        # check if mouse click is within the day header bounds
        if dayLeft <= mouseX <= dayRight and dayTop <= mouseY <= dayBottom:
           app.toDo=True

    for top, left in app.boxesTopLeft:
        if (top + 15 >= mouseX >= top) and (left + 15 >= mouseY >= left):
            if (top, left) not in app.checkedBoxes:
                app.checkedBoxes.append((top, left))
            else:
                app.checkedBoxes.remove((top, left))

    if app.toDo:
        # input
        if app.width / 4 + 120 <= mouseX <= app.width / 4 + 320 and app.height / 4 + 90 <= mouseY <= app.height / 4 + 120:
            if app.isTyping:
                app.isTyping = False
            app.focusField = 'name'
            app.isTyping=True
        elif app.width / 4 + 150 <= mouseX <= app.width / 4 + 250 and app.height / 4 + 140 <= mouseY <= app.height / 4 + 170:
            if app.isTyping:
                app.isTyping = False
            print(app.focusField)
            app.isTyping=True
        # elif app.width / 4 + 220 <= mouseX <= app.width / 4 + 420 and app.height / 4 + 150 <= mouseY <= app.height / 4 + 180:
        #     if app.isTyping:
        #         app.isTyping = False
        #     app.isTyping=True
        else:
            app.isTyping=False

        # day selection
        xStart = app.width / 4 + 150
        for i, day in enumerate(app.days):
            x = xStart + i * 50
            if x <= mouseX <= x + 40 and app.height / 4 + 200 <= mouseY <= app.height / 4 + 230:
                app.selectedDay = day

        # add button
        if app.width / 4 + 50 <= mouseX <= app.width / 4 + 150 and app.height / 4 + 300 <= mouseY <= app.height / 4 + 330:
            if app.inputName and app.inputDuration.isdigit() and app.selectedDay:
                task = {"name": app.inputName, "duration": int(app.inputDuration)}
                app.selectedDay = app.selectedDay.upper()  
                if app.selectedDay not in app.toDoList:
                    app.toDoList[app.selectedDay] = []  
                app.toDoList[app.selectedDay].append(task) 
                app.inputName = ''
                app.inputDuration = ''
                app.inputSlots = ''
                app.selectedDay = None
                app.focusField = None
                app.toDo = False

        # Cancel button
        if app.width / 4 + 200 <= mouseX <= app.width / 4 + 300 and app.height / 4 + 300 <= mouseY <= app.height / 4 + 330:
            app.inputName = ''
            app.inputDuration = ''
            app.inputSlots = ''
            app.selectedDay = None
            app.focusField = None
            app.toDo = False


    # Click home button
    if 60 >= mouseX >= 30 and 60 >= mouseY >= 30:
        #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
        app.notHome = False
        scriptPath = "/Users/rishitashah/Downloads/cmu_graphics_installer/homescreen"
        try:
            os.execv(sys.executable, ['python3', scriptPath])
        except Exception as e:
            print(f"Error launching home screen: {e}")

    if not app.toDo:
        if app.clickedInput:    
            if app.width / 2 - 100 <= mouseX <= app.width / 2 + 100 and app.height / 2 - 25 <= mouseY <= app.height / 2 + 25:
                app.isTyping = True
                app.calendarInput = True
            else:
                app.isTyping = False
                app.calendarInput = False

            if app.width / 2 - 50 <= mouseX <= app.width / 2 + 50 and app.height / 2 + 40 <= mouseY <= app.height / 2 + 70:
                if app.input.strip():
                    if app.selectedDate not in app.events:
                        app.events[app.selectedDate] = []
                    app.events[app.selectedDate].append(app.input.strip())
                app.input = ''
                app.clickedInput = False

            if app.width / 2 + 110 <= mouseX <= app.width / 2 + 140 and app.height / 2 - 140 <= mouseY <= app.height / 2 - 110:
                app.clickedInput = False
        else:
            # xheck if a date cell is clicked
            row, col = findCell(app, mouseX, mouseY)
            if row is not None and col is not None:
                cellIndex = row * app.cols + col
                date = cellIndex - app.startCell + 1
                if 1 <= date <= app.months[app.month]:
                    app.selectedDate = date
                    app.clickedInput = True

#to do list code
def resetToDo (app):
    if app.day == 'Mon':
        return True

def drawToDo(app):  
    listTop = app.boardTop + app.cellSize * app.rows + 20 
    listWidth = (app.width-200)  
    listLeft = app.width/2-listWidth/2
    dayWidth = listWidth // 7 
    
    count = 0
    for day in app.days.keys():  
        dayUpper = day.upper()
        drawRect(listLeft + count * dayWidth, listTop, dayWidth, 40, fill='pink', opacity=20, border='black', borderWidth=1)
        drawLabel(f'{dayUpper}', listLeft + count * dayWidth + dayWidth / 2, listTop + 20, size=16)
        
        if dayUpper in app.toDoList:
            toDoCount = 0
            for task in app.toDoList[dayUpper]:
                if isinstance(task, dict): 
                    taskY = listTop + 60 + toDoCount * 20
                    drawLabel(f'{task["name"]} ({task["duration"]} mins)', listLeft + count * dayWidth + dayWidth / 2, taskY, size=12)
                    checkboxX = listLeft + count * dayWidth + 52
                    checkboxY = taskY
                    drawCheck(app, checkboxX, checkboxY)
                    toDoCount += 1

        count += 1
    count = 0
    
    #draw gridlines
    for i in range(8):
        x = listLeft + i * dayWidth
        drawLine(x, listTop, x, listTop + 300)
    drawLine(listLeft, listTop, listLeft + listWidth, listTop)
    drawLine(listLeft, listTop + 300, listLeft + listWidth, listTop + 300)

def onKeyPress(app, key):
    # possibleDays = {'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'}
    # if key == 'n':
    #     day = app.getTextInput('Enter the day for the task (MON, TUE, WED...):')
    #     day = day.upper()
    #     if day in possibleDays:
    #         task = app.getTextInput(f'Enter the to-do Task for {day}:')
    #         if task:
    #             if day not in app.toDoList:
    #                 app.toDoList[day] = [task]
    #             else:
    #                 app.toDoList[day].append(task)

    if app.calendarInput and app.isTyping:
        if key == 'space':
            app.input += ' '
        elif key == 'backspace':
            app.input = app.input[:-1]
        elif key == 'enter':
            app.savedInput.append(app.input)
            app.input = ''
            app.isTyping = False
        else:
            app.input += key
    
    if key=='*':
        scheduleTasks(app)
        app.displayScheduled=True

    if app.toDo and app.isTyping:
        #handle key input based on the focused field
        if key:
            if app.focusField == 'name':
                if key == 'space':
                    app.inputName += ' '
                elif key == 'backspace':
                    app.inputName = app.inputName[:-1]
                elif key == 'tab':
                    fields = ['name', 'duration', 'slots']
                    currentIndex = fields.index(app.focusField)
                    app.focusField = fields[(currentIndex + 1) % len(fields)]
                else:
                    app.inputName += key
            elif app.focusField == 'duration':
                if key.isdigit():  
                    app.inputDuration += key
                elif key == 'backspace':
                    app.inputDuration = app.inputDuration[:-1]
                elif key == 'tab':
                    fields = ['name', 'duration', 'slots']
                    currentIndex = fields.index(app.focusField)
                    app.focusField = fields[(currentIndex + 1) % len(fields)]
            # elif app.focusField == 'slots':
            #     if key == 'space':
            #         app.inputSlots += ' '
            #     elif key == 'backspace':
            #         app.inputSlots = app.inputSlots[:-1]
            #     elif key == 'tab':
            #         fields = ['name', 'duration', 'slots']
            #         currentIndex = fields.index(app.focusField)
            #         app.focusField = fields[(currentIndex + 1) % len(fields)]
                else:
                    app.inputSlots += key

                    
def drawCheck(app, w, h):
    drawRect(w-50, h-7, 15, 15, border='black', fill=None)
    if (w - 50, h - 7) in app.checkedBoxes:
        drawLine(w - 50, h - 7, w - 35, h + 8, fill='red', lineWidth=2)
        drawLine(w - 35, h - 7, w - 50, h + 8, fill='red', lineWidth=2)
    app.boxesTopLeft.append((w-50, h-7))

def onMouseMove(app, mouseX, mouseY):
    row, col = findCell(app, mouseX, mouseY)
    if row is not None and col is not None:
        app.hoverCell = (row, col)
    else:
        app.hoverCell = None

def drawTaskInput(app):
    drawRect(app.width / 4, app.height / 4, app.width / 2, app.height / 2, fill='white', border='black')
    drawLabel("Add Task", app.width / 2, app.height / 4 + 20, size=18, bold=True)
    drawLabel("Use the tab key to toggle between name and duration", app.width / 2, app.height / 4 + 40, size=12, bold=True)

    drawLabel("Task Name:", app.width / 4 + 20, app.height / 4 + 100, size=14, align='left')
    drawRect(app.width / 4 + 120, app.height / 4 + 90, 200, 30, fill='lightgray', border='blue' if app.focusField == 'name' else 'black')
    drawLabel(app.inputName, app.width / 4 + 130, app.height / 4 + 105, size=12, align='left')

    drawLabel("Duration (mins):", app.width / 4 + 20, app.height / 4 + 155, size=14, align='left')
    drawRect(app.width / 4 + 150, app.height / 4 + 140, 100, 30, fill='lightgray', border='blue' if app.focusField == 'duration' else 'black')
    drawLabel(app.inputDuration, app.width / 4 + 160, app.height / 4 + 155, size=12, align='left')

    # drawLabel("Time Slots (09:00-13:00):", app.width / 4 + 20, app.height / 4 + 160, size=14, align='left')
    # drawRect(app.width / 4 + 220, app.height / 4 + 150, 200, 30, fill='lightgray', border='blue' if app.focusField == 'slots' else 'black')
    # drawLabel(app.inputSlots, app.width / 4 + 230, app.height / 4 + 165, size=12, align='left')

    drawLabel("Select Day:", app.width / 4 + 20, app.height / 4 + 210, size=14, align='left')
    xStart = app.width / 4 + 150
    for i, day in enumerate(app.days):
        x = xStart + i * 50
        drawRect(x, app.height / 4 + 200, 40, 30, fill='lightgray', border='blue' if app.selectedDay == day else 'black')
        drawLabel(day, x + 20, app.height / 4 + 215, size=10)

    drawRect(app.width / 4 + 50, app.height / 4 + 300, 100, 30, fill='green')
    drawLabel("Add", app.width / 4 + 100, app.height / 4 + 315, size=14, fill='white')

    drawRect(app.width / 4 + 200, app.height / 4 + 300, 100, 30, fill='red')
    drawLabel("Cancel", app.width / 4 + 250, app.height / 4 + 315, size=14, fill='white')

def scheduleTasks(app):

    def convertTime(slot):
        start, end = slot.split('-')
        startMinutes = int(start[:2]) * 60 + int(start[3:])
        endMinutes = int(end[:2]) * 60 + int(end[3:])
        return startMinutes, endMinutes

    def isValid(app, day, task, startTime):
        endTime = startTime + task['duration']
        for scheduled in app.scheduledTasks[day]:
            if not (endTime <= scheduled['start'] or startTime >= scheduled['end']):
                return False
        return True

    def backtrack(app, day, tasks, taskIndex=0):
        if taskIndex >= len(tasks):
            return True

        task = tasks[taskIndex]
        for slot in app.availableSlots[day]:
            slotStart, slotEnd = convertTime(slot)
            for startTime in range(slotStart, slotEnd - task['duration'] + 1, 15):  #try every 15 minutes
                if isValid(app, day, task, startTime):
                    task['start'] = startTime
                    task['end'] = startTime + task['duration']
                    app.scheduledTasks[day].append(task)

                    if backtrack(app, day, tasks, taskIndex + 1):
                        return True
                    
                    app.scheduledTasks[day].remove(task)

        return False

    def scheduleDay(day):
        app.scheduledTasks[day] = []  
        tasks = app.toDoList[day]
        backtrack(app, day, tasks)

    for day in app.toDoList:
        scheduleDay(day)

    return(app.scheduledTasks)

def formatTime(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02}:{mins:02}"        

def main():
    runApp()
    

main()
