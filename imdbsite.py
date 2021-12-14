# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import sqlite3

def movielst(url):
    # This function takes in a url from the imdb website, and creates a BeautifulSoup Object to parse through 
    # the site's HTML. The function returns a list of tuples which include the movie title, and movie release date.

    moviedates =[]
    movietitles =[]
    movielst =[]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    # get movie title
    spans = soup.find_all('img', class_='loadlate', height = '209')
    for item in spans:
        title = item.get('alt')
        movietitles.append(title)
    
    #get movie release date
    tagdates = soup.find_all('span', class_= 'lister-item-year text-muted unbold')
    for tag in tagdates:
        date = tag.text
        i = re.search("[0-9]+",date).group(0)
        moviedates.append(i)

    
    for indx in range(len(movietitles)):
        tupl = (movietitles[indx],moviedates[indx])
        movielst.append(tupl)

    return movielst

#Write movie list into a csv file

def write_csv(data, filename):
    # This file takes in a list of tuples and csv filename as input. It then iterates through the list of tuples 
    # to write multiple rows within the csv, outputting a csv file containing each movie title and release date.

    header = ('Movie Title', 'Movie Date', 'Rating')

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in data:
            writer.writerow(item)

#setup database file

def setUpDatabase(db_name):
    # This function simply takes in a string as input which contains the preferred database file name, and 
    # returns the cursor and connection to the created database.

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#Create movie table if not exists

def setUpMovieTable( cur, conn, movielst,type, x = 0):
    # This file takes a database cursor and conneciton, list of movie titles, movie type, and optional 
    # argument which specifies the starting position of the database id. The function creates a table, Movies, 
    # within the passed database and inserts each movie in movielst, along with its corresponding id, date, and type.
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (id INTEGER PRIMARY KEY, title TEXT, date INTEGER, genreid INTEGER, gross INTEGER, awards INTEGER, imdb_rating FLOAT, metascore FLOAT, rotten_tomatoes FLOAT, label INTEGER)")
    for num in range(len(movielst)):
        id = num + x
        cur.execute("INSERT INTO Movies (id,title,date,label) VALUES (?,?,?,?)",(id,movielst[num][0],movielst[num][1],type))
    conn.commit()



# def setUpMovieTable2( cur, conn, movielst,label):
#     cur.execute("CREATE TABLE IF NOT EXISTS Movies (id INTEGER PRIMARY KEY, title TEXT, date INTEGER, genreid INTEGER, gross INTEGER, awards INTEGER, imdb_rating FLOAT, metascore FLOAT, rotten_tomatoes FLOAT, label INTEGER)")
#     for num in range(len(movielst)):
#         id = num + 100
#         cur.execute("INSERT INTO Movies (id,title,date,label) VALUES (?,?,?,?)",(id,movielst[num][0],movielst[num][1],label))
#     conn.commit()


#create genre table is not exists

def setUpGenreTable(cur, conn, genrelst):
    # This function takes in a databse cursor and connection, as well as a list of movie genres. It then creates
    # a table, Genres, within the database, along with its corresponding id number.
    cur.execute("CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, genre TEXT)")
    for i in range(len(genrelst)):
        cur.execute("INSERT OR IGNORE INTO Genres (id, genre) VALUES (?,?)", (i, genrelst[i]))
    conn.commit()

def main():
    # This function calls all the above functions, setting up the database, defining the movie genres, 
    # grabbing the lists of movies, writing the csv, and setting up the databse tables.
    
    cur, conn = setUpDatabase('movieData.db')

    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    m1 = movielst('https://www.imdb.com/list/ls008939186/') 
    m2 = movielst('https://www.imdb.com/list/ls054431555/')
    movies = m1 + m2

    write_csv(movies,'movies.csv')

    setUpGenreTable( cur, conn, genres)
    setUpMovieTable( cur, conn, m1,0)
    setUpMovieTable( cur, conn, m2,1,100)

main()

