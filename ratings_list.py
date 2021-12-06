import requests
import re
import csv
import json
import sqlite3

#possibly use dictionary instead of csv bc of racing issue
#CREATE TABLE Movies (id INTEGER PRIMARY KEY, title TEXT, date TEXT, genreid TEXT, gross TEXT, awards TEXT, IMDB REAL, metacritic REAL, rotten_tomatoes REAL, average rating REAL)

def getRatings():
    api_key = 'd8af6faf'

    with open('movies.csv', 'r') as file:
        reader = csv.reader(file)
        count = 0
        dbName ='movieData.db'
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        next(reader)
        for row in reader:
            #print(row)
            title = row[0]
            parameters = {'t': title, 'apikey': api_key}
            response_obj = requests.get('https://www.omdbapi.com/', params=parameters)
            data = response_obj.json()
            if 'Error' not in data:
                date = data.get('Year', 0)
                gross = data.get('BoxOffice', '0')
                genre = data.get('Genre', 'Not Provided')
                if genre != 'Not Provided':
                    genre = genre.split(",")[0]
                print(date)
                print(gross)
                print(genre)




                Awards_Won = '0'
                if 'Awards' in data:
                    Awards = data['Awards'].split(" ")
                    for index in range(len(Awards)-1):
                        if Awards[index + 1] == 'wins' or Awards[index + 1] == 'won':
                            Awards_Won = Awards[index]
                            break
                print(Awards_Won)
                

                ratings_dict_list = data['Ratings']
                print(ratings_dict_list)
                for dictionary in ratings_dict_list:
                    if dictionary['Source'] == 'Internet Movie Database':
                        first_rating = dictionary['Value'] 
                        IMD_rating = float(dictionary.get('Value', 0).split('/')[0]) * 10 
                        print(IMD_rating)
                    if dictionary['Source'] == 'Rotten Tomatoes':
                        RottenTomatoes_rating = dictionary.get('Value', 0)
                        RottenTomatoes_rating = float(RottenTomatoes_rating[:-1])
                        print(RottenTomatoes_rating)
                    if dictionary['Source'] == 'Metacritic':
                        Metacritic_rating = dictionary.get('Value', 0)
                        Metacritic_rating = float(Metacritic_rating.split('/')[0])
                        print(Metacritic_rating)
                    

                print(" ")
                count += 1

                print(count)
                print(" ") 
                cursor.execute("INSERT OR IGNORE INTO Movies (title, date, genreid, gross, awards, IMDB, metacritic, rotten_tomatoes) values (?,?,?,?,?,?,?,?) ", (title, date, genre, gross, Awards_Won,  IMD_rating, Metacritic_rating, RottenTomatoes_rating))
                
        conn.commit()
            
getRatings() 