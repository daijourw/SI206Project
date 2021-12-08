# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from sqlite3.dbapi2 import Row
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
import re
import csv
import os
import sqlite3


#dictionary { title, date, genre, gross, awards, IMDB, metacritic, rotten_tomatoes}

def getGenreGrossData(db_filename, label):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    genreavgw = {}
    countw = {}
    entryw = {}

    genreavgb = {}
    countb = {}
    entryb = {}

    cur.execute('SELECT gross, genre FROM Movies JOIN Genres ON Movies.genreid = Genres.id WHERE label='+str(label),)
    for row in cur:#(number,genre)
        print(row)
    #     gross = row[0]
    #     genre = row[-1]
    #     count +=1
    #     if count == 100:
    #         break
    
    # #w = cur[0][0:100]
    # #b = cur[0][100:]
    # for row in w:
    #     gross = row[0]
    #     genre = row[1]

    #     if countw.get(genre,None) == None:
    #         countw[genre] = gross
    #         entryw[genre] = 1
    #     else:
    #         countw[genre] += gross
    #         entryw[genre] += 1

    #     for key in countw.keys():
    #         genre = key
    #         avg = countw[key]/entryw[key]
    #         genreavgw[genre] = avg
    # for row in b:
    #     gross = row[0]
    #     genre = row[1]

    #     if countb.get(genre,None) == None:
    #         countb[genre] = gross
    #         entryb[genre] = 1
    #     else:
    #         countb[genre] += gross
    #         entryb[genre] += 1

    #     for key in countb.keys():
    #         genre = key
    #         avg = countw[key]/entryw[key]
    #         genreavgb[genre] = avg

    # return genreavgw,genreavgb
#dict{genre:val,}
def barchart_movies(dict1,dict2):
    whitemovies = dict1
    blackmovies = dict2

    labels = whitemovies.keys()
    white = dict1.values()
    black = dict2.values()
    
    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, white, width, label='White Movies')
    rects2 = ax.bar(x + width/2, black, width, label='Black Movies')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Genres')
    ax.set_title('Gross by Genre and Category')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    fig.savefig('BarGraph.jpeg')
    plt.show()

def scatter_movies(dict1,dict2):
    #get title and rating and put in dictionary then go through databsse to get gross
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/movieData.db')
    cur = conn.cursor()

    bmovieRatings = {}
    wmovieRatings = {}

    with open('movies.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader[0:100]:
            title = row[0]
            rating = row[-1]
            bmovieRatings[title] = [rating]
        for row in reader[100:]:
            title = row[0]
            rating = row[-1]
            wmovieRatings[title] = [rating]
        
    for movie in bmovieRatings:
        cur.execute('SELECT gross FROM Movies WHERE title ='+movie)
        for row in cur:
            bmovieRatings[movie].append(row[0])
    for movie in wmovieRatings:
        cur.execute('SELECT gross FROM Movies WHERE title ='+movie)
        for row in cur:
            wmovieRatings[movie].append(row[0])
    wgross = []
    wrating = []
    bgross = []
    brating = []
    
    for item in wmovieRatings.values():
        wgross.append(item[1])
        wrating.append(item[0])
    for item in bmovieRatings.values():
        bgross.append(item[1])
        brating.append(item[0])
    
    fig,ax = plt.subplots()
    ax.plot(wrating, wgross)
    ax.plot(bgross, brating)

    ax.set_ylabel('Gross')
    ax.set_xlabel('Average Rating')
    ax.set_title('Gross vs Average Rating')
    #ax.set_xticks(x, wrating)
    ax.legend()
    fig.savefig('ScatterGraph.jpeg')
    plt.show()

def main():
    getGenreGrossData('movieData.db',0)
    #barchart_movies(dictionaries)
    #scatter_movies(dictionaries)
        
main()