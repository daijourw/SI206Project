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


def getGenreGrossData(db_filename, label):
    # This function takes in a database fiilename, and movie type as its input. It then creates a connection and cursor to the database,
    # and selects several values to calculate the average gross earnings for each movie genre in the database. It then outputs this 
    # information in a dictionary with the genres as the key, and the gross earnings as the the values. 

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
    for row in cur:
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

def barchart_movies(dict1,name):
    # This function takes in a dictionary which contains movie genres as the keys and average gross earnings as the values. It also takes 
    # in the preferred filename of the graph which will be returned. The function uses the dictionary to create and decorate a bar chart 
    # which will compare the average gross earnings across movie genres. The function will output a jpeg file, with the preferred name 
    # which was passed into the function.

    genres = dict1.keys()
    average = dict1.values()
    font1 = {'family':'serif','color':'black','size':17}
    font2 = {'family':'serif','color':'black','size':14}
    plt.figure(figsize=(9,11))
    plt.bar(genres,average,color=['black', 'red', 'green', 'orange', 'blue', 'pink','purple', 'cyan','yellow','grey'])
    plt.xlabel('Genre Category',fontdict = font2)
    plt.ylabel('Average Gross (millions)',fontdict = font2)
    plt.title('Average Gross per Movie Category',fontdict = font1)
    plt.xticks(rotation=90)
    #plt.show()
    plt.savefig(name)


def scatter_movies():
    # This function takes no input, as it is designed to iterate through the ratings.csv file to create two dictionaries which contain 
    # bo the average critic rating and gross for each movie. These dictionaries are then used to create a scatter plot which compares 
    # the average critic ratings and gross earnings for each movie, across both movie types.

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
    
    font1 = {'family':'serif','color':'black','size':20}
    font2 = {'family':'serif','color':'black','size':15}
    plt.yscale('log')
    plt.xlabel('Average Rating',fontdict = font2)
    plt.ylabel('Gross ($)',fontdict = font2)
    plt.title('Gross vs Average Rating',fontdict = font1)
    plt.legend(loc="upper left")
    
    plt.savefig('ScatterGraph.jpeg')
    plt.tight_layout()
    #plt.show()

def main():
    # This function calls the above functions, getGenreGrossData,barchart_movies, and scatter_movies to create the visuals needed 
    # to compare and analyze the collected data.

    whitem = getGenreGrossData('movieData.db',0)
    blackm = getGenreGrossData('movieData.db',1)
    barchart_movies(blackm,'BarChartBlackMovies.jpeg')
    barchart_movies(whitem,'BarChartWhiteMovies.jpeg')
    scatter_movies()
    #barchart_movies(dictionaries)
    #scatter_movies(dictionaries)
        
main()