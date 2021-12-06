# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import sqlite3

# Extract movies from imdb webpage using Beautiful Soup
def movielst(url):
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
    header = ('Movie Title', 'Movie Date', 'Rating')

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in data:
            writer.writerow(item)

#setup database file
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#Create movie table if not exists
def setUpMovieTable( cur, conn, movielst):
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (id INTEGER PRIMARY KEY, title TEXT, date INTEGER, genreid INTEGER, gross INTEGER, awards INTEGER, imdb rating INTEGER, metascore INTEGER, rotten tomatoes INTEGER)")
    for num in range(len(movielst)):
        cur.execute("INSERT INTO Movies (id,title,date) VALUES (?,?,?)",(num,movielst[num][0],movielst[num][1]))
    conn.commit()

#create genre table is not exists
def setUpGenreTable(cur, conn, genrelst):
    cur.execute("CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, genre TEXT)")
    for i in range(len(genrelst)):
        cur.execute("INSERT OR IGNORE INTO Genres (id, genre) VALUES (?,?)", (i, genrelst[i]))
    conn.commit()


def main():
    cur, conn = setUpDatabase('movieData.db')

    genres = ['Action', 'Animation', 'Biography', 'Comedy', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    m1 = movielst('https://www.imdb.com/list/ls008939186/') 
    m2 = movielst('https://www.imdb.com/list/ls054431555/')
    movies = m1 + m2

    
    write_csv(movies,'movies.csv')

    setUpGenreTable( cur, conn, genres)
    setUpMovieTable( cur, conn, movies)

main()

