# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from sqlite3.dbapi2 import Row
from bs4 import BeautifulSoup
import matplotlib.pylot as plt
import numpy as np
import requests
import re
import csv
import os
import sqlite3


#dictionary { title, date, genre, gross, awards, IMDB, metacritic, rotten_tomatoes}
def getGenreGrossData(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    genreavgw = {}
    countw = {}
    entryw = {}

    genreavgb = {}
    countb = {}
    entryb = {}

    cur.execute('SELECT gross, genreid FROM Movies JOIN Genres ON Movies.genreid = Genres.id',)
    w = cur[0:100]
    b = cur[100:]
    for row in w:
        gross = row[0]
        genre = row[1]

        if countw.get(genre,None) == None:
            countw[genre] = gross
            entryw[genre] = 1
        else:
            countw[genre] += gross
            entryw[genre] += 1

        for key in countw.keys():
            genre = key
            avg = countw[key]/entryw[key]
            genreavgw[genre] = avg
    for row in b:
        gross = row[0]
        genre = row[1]

        if countb.get(genre,None) == None:
            countb[genre] = gross
            entryb[genre] = 1
        else:
            countb[genre] += gross
            entryb[genre] += 1

        for key in countb.keys():
            genre = key
            avg = countw[key]/entryw[key]
            genreavgb[genre] = avg

    return genreavgw,genreavgb
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

    plt.show()

def scatter_movies(dict1,dict2):
    #get title and rating and put in dictionary then go through databsse to get gross