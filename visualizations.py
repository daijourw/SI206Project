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
    genreavg = {}
    count = {}
    entry = {}

    genreavgb = {}
    countb = {}
    entryb = {}

    cur.execute('SELECT gross, genre FROM Movies JOIN Genres ON Movies.genreid = Genres.id WHERE label='+str(label),)
    for row in cur:#(number,genre) each adventure: avg gross
        genre = row[-1]
        gross = row[0]

        if count.get(genre,None) == None:
            count[genre] = gross
            entry[genre] = 1
        else:
            count[genre] += gross
            entry[genre] += 1

        for key in count.keys():
            avg = count[key]//entry[key]
            genreavg[key] = avg
    return genreavg
#dict{genre:val,}
def barchart_movies(dict1,dict2):
    whitemovies = dict1
    blackmovies = dict2

    labels = whitemovies.keys()
    white = dict1.values()
    black = dict2.values()
    
    x = np.arange(len(labels))  # the label locations
    width = 0.4  # the width of the bars

    fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width/2, white, width, label='White Movies')
    # rects2 = ax.bar(x + width/2, black, width, label='Black Movies')
    ects1 = ax.bar(x, white, width, label='White Movies')
    rects2 = ax.bar(x, black, width, label='Black Movies')
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

def scatter_movies():
    #get title and rating and put in dictionary then go through databsse to get gross
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/movieData.db')
    cur = conn.cursor()

    movie1 = {}
    movie2 = {}

    with open('ratings.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title = row[0]
            rating = row[2]
            type = row[-1]
            gross = row[-2]
            if int(type) == 0:
                movie1[title] = [rating,gross]
            else:
                movie2[title] = [rating,gross]
    wratings = []
    wgross = []
    #print(movie1)
    for key in movie1:
        lst= movie1[key]
        rating = lst[0]
        gross = lst[1]
        wratings.append(rating)
        wgross.append(gross)
    bratings = []
    bgross = []
    for key in movie2:
        lst= movie2[key]
        rating = lst[0]
        gross = lst[1]
        bratings.append(rating)
        bgross.append(gross)
    
    #print(wgross,wratings)
    
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax.scatter(wratings, wgross, color='g', marker='o',s=10,label='White Movies',edgecolor='black')
    ax2.scatter(bratings, bgross, color='b',marker='x',s=10,label='Black Movies',edgecolor='black')
    
    #ax.set_xticks(range(0,100,10))
    #plt.xscale('log')
    #plt.yscale('log')

    ax.set_ylabel('Gross')
    ax.set_xlabel('Average Rating')
    ax.set_title('Gross vs Average Rating')
    ax2.set_ylabel('Gross')
    ax2.set_xlabel('Average Rating')
    ax2.set_title('Gross vs Average Rating')
    
    #ax.legend()
    #fig.savefig('ScatterGraph.jpeg')
    plt.tight_layout()
    plt.show()

def main():
    whitem = getGenreGrossData('movieData.db',0)
    blackm = getGenreGrossData('movieData.db',1)
    #barchart_movies(whitem,blackm)
    scatter_movies()
    #barchart_movies(dictionaries)
    #scatter_movies(dictionaries)
        
main()