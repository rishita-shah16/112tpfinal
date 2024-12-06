Project Title and Description:
112 Bullet Journal starts off with a homescreen where the user can move around and interact with different furniture to unlock different aspects of an online bullet journal.
It has a sleep tracker where the bed is, in which the user can track the time they went to bed and the time they woke up for every day of the month. That toggles to the mood tracker
as well. Here, the user can color in how they felt for every day of the month using the bank of colors associated with an emotion. 
It additionally has a calendar and to-do list feature, which opens when interacting with the desk. Here the user can input an event for a day in the month. The calendar uses live data to keep
a clock rolling and show what month it is. Additionally, it has a to-do list for the week. Here, the user can input the task name and duration and also check it off when
completed. Using backtracking, the user can also see a recommended auto-generated schedule to fit tasks in between 9:00AM to 11:00PM. Next, it has a habit tracker, which allows the user
to add and delete any habits for the month. It also resets based off real-time data. Here the user can color in the calendar if the task was completed. Lastly, my project has the couch feature,
which serves as a movie bank. It web scrapes for the movie's information, including actors, storyline, etc off of imdb's website and displays it for the user upon mouse click. 

Run Instructions:
The main entry file for my project is through homescreen.py. Run this in a python 3.8 editor. Additionally, these must be installed:
  cmu-graphics
  os, sys: For navigating through the py files
  requests, beautifulsoup4: For web scraping (used in the couch application)
pip install will work for all of these.
Then, place all the images in the src folder in the same directory where the scripts are located.

Shortcuts:
Click on the home button to return to homescreen.py
Click on the bed to enter bed.py (sleep tracker)
  Click on the smiley face for mood tracker
Click on the couch to enter couch.py (movies)
Click on the desk for calendar and to do list
  Click * for backtracking algorithm for scheduling tasks
  Click on days to add events and to-do lists
Click on coffee table for the habit tracker
