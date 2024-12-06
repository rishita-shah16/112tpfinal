from cmu_graphics import *
from bs4 import BeautifulSoup
import requests
import os
import sys

def onAppStart(app):
    app.notHome = True
    app.width=1000
    app.height=800
    app.movieWidth = 200
    app.movieLength = 300
    app.movieSpacing = 280  
    #all images here are from imdb.com
    app.movieSet = {'Spiderman':('https://www.imdb.com/title/tt0145487','1.jpg'),
                    'Spiderman 2':('https://www.imdb.com/title/tt0316654','2.jpg'),
                    'Spiderman 3':('https://www.imdb.com/title/tt0413300','3.jpg'),
                    'The Amazing Spiderman':('https://www.imdb.com/title/tt0948470','4.jpg'),
                    'The Amazing Spiderman 2':('https://www.imdb.com/title/tt1872181','5.jpg'),
                    # 'Spiderman Homecoming':('https://www.imdb.com/title/tt2250912','6.jpg'),
                    # 'Spiderman Far From Home':('https://www.imdb.com/title/tt6320628','7.jpg'),
                    # 'Spiderman No Way Home':(https://www.imdb.com/title/tt10872600,'8.jpg'),
                    # 'Spiderman Into The Spiderverse':(https://www.imdb.com/title/tt4633694,'9.jpg'),
                    # 'Spiderman Across the Spiderverse':(https://www.imdb.com/title/tt9362722,'10.jpg'),
                    # 'Pitch Perfect':(https://www.imdb.com/title/tt1981677,'11.jpg'),
                    # 'Pitch Perfect 2':(https://www.imdb.com/title/tt2848292,'12.jpg'),
                    # 'Pitch Perfect 3':(https://www.imdb.com/title/tt4765284,'13.jpg'),
                    # 'Back to the Future':(https://www.imdb.com/title/tt0088763,'14.jpg'),
                    # 'Back to the Future 2':(https://www.imdb.com/title/tt0096874,'15.jpg'),
                    # 'Back to the Future 3':(https://www.imdb.com/title/tt0099088,'16.jpg'),
                    # 'Star Wars Episode I':(https://www.imdb.com/title/tt0120915,'17.jpg'),
                    # 'Star Wars Episode II':(https://www.imdb.com/title/tt0121765,'18.jpg'),
                    # 'Star Wars Episode III':(https://www.imdb.com/title/tt0121766,'19.jpg'),
                    # 'Star Wars Episode IV':(https://www.imdb.com/title/tt0076759,'20.jpg'),
                    # 'Star Wars Episode V':(https://www.imdb.com/title/tt0080684,'21.jpg'),
                    # 'Star Wars Episode VI':(https://www.imdb.com/title/tt0086190,'22.jpg'),
                    # 'Star Wars Episode VII':(https://www.imdb.com/title/tt2488496,'23.jpg'),
                    # 'Star Wars Episode VIII':(https://www.imdb.com/title/tt2527336,'24.jpg'),
                    # 'Star Wars Episode IX':(https://www.imdb.com/title/tt2527338,'25.jpg'),
                    # 'Rogue One: A Star Wars Story':(https://www.imdb.com/title/tt3748528,'26.jpg'),
                    # 'Solo: A Star Wars Story':(https://www.imdb.com/title/tt3778644,'27.jpg'),
                    # 'Toy Story':(https://www.imdb.com/title/tt0114709,'28.jpg'),
                    # 'Toy Story 2':(https://www.imdb.com/title/tt0120363,'29.jpg'),
                    # 'Toy Story 3':(https://www.imdb.com/title/tt0435761,'30.jpg'),
                    # 'Toy Story 4':(https://www.imdb.com/title/tt1979376,'31.jpg'),
                    # 'Cars':(https://www.imdb.com/title/tt0317219,'32.jpg'),
                    # 'Cars 2':(https://www.imdb.com/title/tt1216475,'33.jpg'),
                    # 'Cars 3':(https://www.imdb.com/title/tt3606752,'34.jpg'),
                    # 'Iron Man':(https://www.imdb.com/title/tt0371746,'35.jpg'),
                    # 'Iron Man 2':(https://www.imdb.com/title/tt1228705,'36.jpg'),
                    # 'Iron Man 3':(https://www.imdb.com/title/tt1300854,'37.jpg'),
                    # 'Captain America: First Avenger':(https://www.imdb.com/title/tt0458339,'38.jpg'),
                    # 'Captain America: Winter Soilder':(https://www.imdb.com/title/tt1843866,'39.jpg'),
                    # 'Captain America: Civil War':(https://www.imdb.com/title/tt3498820,'40.jpg'),
                    # 'Thor':(https://www.imdb.com/title/tt0800369,'41.jpg'),
                    # 'Thor: The Dark World':(https://www.imdb.com/title/tt1981115,'42.jpg'),
                    # 'Thor: Ragnarok':(https://www.imdb.com/title/tt3501632/,'43.jpg'),
                    # 'Thor: Love and Thunder':(https://www.imdb.com/title/tt10648342,'44.jpg'),
                    # 'Gaurdians of the Galaxy':(https://www.imdb.com/title/tt2015381,'45.jpg'),
                    # 'Gaurdians of the Galaxy Vol. 2':(https://www.imdb.com/title/tt3896198,'46.jpg'),
                    # 'Gaurdians of the Galaxy Vol. 3':(https://www.imdb.com/title/tt6791350,'47.jpg'),
                    # 'Deadpool':(https://www.imdb.com/title/tt1431045,'48.jpg'),
                    # 'Deadpool 2':(https://www.imdb.com/title/tt5463162,'49.jpg'),
                    # 'Deadpool and Wolverine':(https://www.imdb.com/title/tt6263850,'50.jpg'),
    }
    app.scrollX = 0
    app.scrollSpeed = 20
    app.keyPressed = None
    app.totalMovies = len(app.movieSet)
    app.totalLength = app.totalMovies * app.movieSpacing
    app.clickedMovie = None
    app.movieInfoDisplayed = False

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    drawMovies(app)
    if app.clickedMovie is not None and not app.movieInfoDisplayed:
        #drawLabel(f"You clicked on: {app.clickedMovie}", app.width / 2, 50, size=20, fill='blue')
        drawIMDB(app)
    if app.notHome:
        drawImage('home.png', 30, 30, width=30, height=30)
        #image from <https://www.flaticon.com/free-icon/home-button_61972>


def drawMovies(app):
    count = 0
    for movie, image in app.movieSet.items():
        x = 50 + (count * app.movieSpacing - app.scrollX) % app.totalLength
        y = 100

        if x < -app.movieWidth:
            x += app.totalLength
        elif x > app.width:
            x -= app.totalLength

        drawCircle(x + app.movieWidth / 2, y + app.movieLength / 2, app.movieWidth / 1.5, fill='darkGray', opacity=50)
        drawCircle(x + app.movieWidth / 2, y + app.movieLength / 2, app.movieWidth / 1.8, fill='white', opacity=30)

        drawRect(x - 5, y - 5, app.movieWidth + 10, app.movieLength + 10, border='gold', borderWidth=4, fill=None)
        drawLabel(movie, x + app.movieWidth / 2, y + app.movieLength + 30, align='center', size=18, fill='white', bold=True)
        drawImage(image[1], x, y, width=app.movieWidth, height=app.movieLength)

        count += 1

def onStep(app):
    if app.keyPressed == 'left':
        app.scrollX = (app.scrollX + app.scrollSpeed) % app.totalLength
    elif app.keyPressed == 'right':
        app.scrollX = (app.scrollX - app.scrollSpeed) % app.totalLength

def onKeyPress(app, key):
    if key in ('left', 'right'):
        app.keyPressed = key

def onKeyRelease(app, key):
    if key in ('left', 'right'):
        app.keyPressed = None

def onMousePress(app, mouseX, mouseY):
    count = 0
    for movie, image in app.movieSet.items():
        x = 50 + (count * app.movieSpacing - app.scrollX) % app.totalLength
        y = 100

        if x < -app.movieWidth:
            x += app.totalLength
        elif x > app.width:
            x -= app.totalLength

        if x - 5 <= mouseX <= x + app.movieWidth + 5 and y - 5 <= mouseY <= y + app.movieLength + 5:
            if app.clickedMovie != movie:  #check if a new movie is clicked
                app.clickedMovie = movie
                app.movieInfoDisplayed = False 
                extractMovieInfo(app, app.movieSet[app.clickedMovie][0])  
            break

        count += 1
        app.clickedMovie = None
        app.movieInfoDisplayed = False
    
    if 30 <= mouseX <= 60 and 30 <= mouseY <= 60:
        #<https://www.geeksforgeeks.org/uses-of-os-and-sys-in-python/>
        app.notHome = False
        scriptPath = "/Users/rishitashah/Downloads/cmu_graphics_installer/homescreen"
        try:
            os.execv(sys.executable, ['python3', scriptPath])
        except Exception as e:
            print(f"Error launching home screen: {e}")


def extractMovieInfo(app, url):
    #https://stackoverflow.com/questions/70139947/python-scraping-httperror-403-client-error-forbidden-for-url 
    # i used this source to get headers for the request to extract information from IMDB site
    #https://medium.com/@spaw.co/how-to-extract-content-from-a-div-tag-using-beautifulsoup-in-python-45c4acedd727
    # this was to get the specific tag information from the source code on each site
    headers = { 'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    titleTag = soup.find('h1')
    movieTitle = titleTag.text.strip()
    ratingTag = soup.find('span', class_='sc-d541859f-1 imUuxf')
    imdbRating = ratingTag.text if ratingTag else 'N/A'

    #WIP
    storylineTag = soup.find('div', {'class': 'ipc-html-content-inner-div'})
    print(storylineTag)
    storyline = storylineTag.text.strip() if storylineTag else 'N/A'

    wrappedStoryline = ''
    lineLength = 80
    for i in range(0, len(storyline), lineLength):
        wrappedStoryline += storyline[i:i+lineLength] + '\n'
    listOfLabels = wrappedStoryline.split('\n')

    

    directorTags = soup.find_all('a', href=lambda href: href and 'tt_ov_dr' in href)
    directors = [tag.text.strip() for tag in directorTags]

    starTags = soup.find_all('a', href=lambda href: href and 'tt_ov_st' in href)
    stars = []
    for tag in starTags:
        star = tag.text.strip().lower()  
        if star != 'stars' and star not in stars:  
            stars.append(tag.text.strip())
            stars=stars[:4]

    return (movieTitle, imdbRating, listOfLabels, ','.join(directors), stars[:-1])

def drawIMDB(app):
    if app.clickedMovie is None:
        return
    title, rating, storyline, directors, stars = extractMovieInfo(app, app.movieSet[app.clickedMovie][0])

    drawRect(0, 450, app.width, app.height - 450, fill='darkSlateGray', opacity=80)
    drawRect(50, 470, app.width - 100, app.height - 490, fill='black', border='gold', borderWidth=3)
    
    drawLabel(f"Title: {title}", app.width / 2, 500, size=20, fill='white')
    drawLabel(f"IMDb Rating: {rating}", app.width / 2, 530, size=20, fill='white')
    drawLabel(f"Director(s): {directors}", app.width / 2, 560, size=20, fill='white', align='center')
    drawLabel(f"Stars: {', '.join(stars)}", app.width / 2, 590, size=20, fill='white', align='center')
    count=0
    drawLabel('Storyline:', app.width/2, 630, size=20, fill='white')
    for line in storyline:
        drawLabel(line, app.width / 2, 650+count*20, size=20, fill='white', align='center')
        count+=1
    


def main():
    runApp(app.width, app.height)

main()