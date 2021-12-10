# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from sqlite3.dbapi2 import Row
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import average
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
def barchart_movies(dict1,name):

    genres = dict1.keys()
    average = dict1.values()
    font1 = {'family':'serif','color':'black','size':17}
    font2 = {'family':'serif','color':'black','size':14}
    plt.figure(figsize=(9,7))
    plt.bar(genres,average,color=['black', 'red', 'green', 'orange', 'blue', 'pink','purple', 'cyan','yellow','grey'])
    plt.xlabel('Genre Category',fontdict = font2)
    plt.ylabel('Average Gross (millions)',fontdict = font2)
    plt.title('Average Gross per Movie Category',fontdict = font1)
    plt.xticks(rotation=90)
    #fig.savefig('HW8BarGraph.jpeg')
    plt.show()
    plt.savefig(name)
    
    # x = np.arange(len(labels))  # the label locations
    # width = 0.4  # the width of the bars

    # fig, ax = plt.subplots()
    # # rects1 = ax.bar(x - width/2, white, width, label='White Movies')
    # # rects2 = ax.bar(x + width/2, black, width, label='Black Movies')
    # ects1 = ax.bar(x, white, width, label='White Movies')
    # rects2 = ax.bar(x, black, width, label='Black Movies')
    # # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Genres')
    # ax.set_title('Gross by Genre and Category')
    # ax.set_xticks(x, labels)
    # ax.legend()

    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    # fig.tight_layout()
    # fig.savefig('BarGraph.jpeg')

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
    sortedm1 = sorted(movie1.values(), key = lambda x: x[0])
    sortedm2 = sorted(movie2.values(), key = lambda x: x[0])
    #print(sortedm1)
    wratings = []
    wgross = []
    sorted
    for key in sortedm1:
        rating = key[0]
        gross = key[1]
        wratings.append(rating)
        wgross.append(gross)
    bratings = []
    bgross = []
    for key in sortedm2:
        rating = key[0]
        gross = key[1]
        bratings.append(rating)
        bgross.append(gross)
    
    #print(wgross,wratings)
    plt.figure(figsize=(11,6))

    plt.scatter(bratings,bgross, color='blue',marker='x',s=25,label='Black Movies',edgecolor='black')
    plt.scatter(wratings,wgross, color='green',marker='o',s=25,label='White Movies',edgecolor='black')
    plt.xticks(np.arange(len(bratings)),bratings, rotation=90)
    #plt.yticks(np.arange(len(bgross)),bgross)
    #plt.xticks(np.arange(len(range(20))),range(0,100,5), rotation=90)
    #ax.set(xlim=(0, 100), xticks=np.arange(1, 100))
    # fig = plt.figure()
    # ax = fig.add_subplot(121)
    # ax2 = fig.add_subplot(122)
    # ax.scatter(wratings, wgross, color='g', marker='o',s=10,label='White Movies',edgecolor='black')
    # ax2.scatter(bratings, bgross, color='b',marker='x',s=10,label='Black Movies',edgecolor='black')
    
    #ax.set_xticks(range(0,100,10))
    #plt.xscale('log')
    font1 = {'family':'serif','color':'black','size':20}
    font2 = {'family':'serif','color':'black','size':15}
    plt.yscale('log')
    plt.xlabel('Average Rating',fontdict = font2)
    plt.ylabel('Gross ($)',fontdict = font2)
    plt.title('Gross vs Average Rating',fontdict = font1)
    plt.legend(loc="upper left")
    # ax.set_ylabel('Gross ($)')
    # ax.set_xlabel('Average Rating')
    # ax.set_title('Gross vs Average Rating')
    # ax2.set_ylabel('Gross')
    # ax2.set_xlabel('Average Rating')
    # ax2.set_title('Gross vs Average Rating')
    
    plt.savefig('ScatterGraph.jpeg')
    plt.tight_layout()
    plt.show()

def main():
    whitem = getGenreGrossData('movieData.db',0)
    blackm = getGenreGrossData('movieData.db',1)
    barchart_movies(whitem,'WBar.jpeg')
    barchart_movies(blackm,'BBar.jpeg')
    scatter_movies()
    #barchart_movies(dictionaries)
    #scatter_movies(dictionaries)
        
main()