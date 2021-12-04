# FALL 2021 Final Project
# SI 206
# Name: Daijour Williams & Lennox Thomas

from bs4 import BeautifulSoup
import requests
import re
import csv

def movielst(url):
    moviedates =[]
    movietitles =[]
    movielst =[]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    spans = soup.find_all('img', class_='loadlate', height = '209')
    for item in spans:
        title = item.get('alt')
        movietitles.append(title)
    
    tagdates = soup.find_all('span', class_= 'lister-item-year text-muted unbold')
    
    for tag in tagdates:
        date = tag.text
        i = re.search("[0-9]+",date).group(0)
        moviedates.append(i)
    
    for indx in range(len(movietitles)):
        tupl = (movietitles[indx],moviedates[indx])
        movielst.append(tupl)

    return movielst

#def bmovielst(url):
#https://www.imdb.com/list/ls054431555/



def write_csv(data, filename):
    header = ('Movie Title', 'Movie Date', 'Rating')

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in data:
            writer.writerow(item)


m1 = movielst('https://www.imdb.com/list/ls008939186/') 
m2 = movielst('https://www.imdb.com/list/ls054431555/')
movies = m1 + m2
write_csv(movies,'movies.csv')


