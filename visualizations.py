# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from bs4 import BeautifulSoup
import matplotlib.pylot as plt
import numpy as np
import requests
import re
import csv
import os
import sqlite3


#dictionary { title, date, genre, gross, awards, IMDB, metacritic, rotten_tomatoes}

def barchart_movies(dict1, dict2):
    xax1 = ['Action', 'Animation', 'Biography', 'Comedy', 'Drama', 'Family', 'Fantasy', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    yax1 = []
    for category in dict1:
        yax1.append(category[1])
    
    xax2 = []
    yax2 = []
    for category in dict2.items():
        xax2.append(category[0])
        yax2.append(category[1])

    fig, ax = plt.subplots()
    ax.barh(xax1,yax1)
    ax.set_xlabel('Gross')
    ax.set_ylabel('Genre')
    ax.set_title('Genre & Gross')

    plt.xticks(rotation=90)
    fig.savefig('HW8BarGraph.jpeg')
    plt.show()
    ret_dict = sorted(cat_dict.items(), key = lambda x: x[0])
    return(ret_dict)