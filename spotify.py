# SI 206 Final Project
# Daijour Williams
#Get data from spotify api and put into database

from bs4 import BeautifulSoup
import requests
import re
import csv


#function read csv file and places mvoies into a list

#set up api
def SpotifySearch(term):
    parameters = {"id":}
    response = requests.get("https://api.spotify.com/v1/albums", params = parameters)
    data = response.json()
    results = data["results"]

#

#