import requests
import re
import csv
import json
import sqlite3

#possibly use dictionary instead of csv bc of racing issue
#CREATE TABLE Movies (id INTEGER PRIMARY KEY, title TEXT, date INTEGER, genreid TEXT, gross INTEGER, awards TEXT, IMDB REAL, metacritic REAL, rotten_tomatoes REAL, average rating REAL)


def getRatings():
    api_key = 'd8af6faf'
    rest_rows = []
    with open('movies.csv', 'r') as file:
        reader = csv.reader(file)
        count = 0
        dbName ='movieData.db'
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        #next(reader)
        for row in reader:
            #print(row)           
            if count == 25:
                rest_rows.append(row)
                continue
            title = row[0]
            parameters = {'t': title, 'apikey': api_key}
            response_obj = requests.get('https://www.omdbapi.com/', params=parameters)
            data = response_obj.json()
            print(data)
            if 'Error' not in data:
                date = data.get('Year', 0)
                gross = data.get('BoxOffice', "$0")
                if gross == 'N/A':
                    gross = "$0"
                gross_list = (gross[1:].split(","))
                gross_int = ""
                for num in gross_list:
                    gross_int += num
                gross_int = int(gross_int)
                print("gross_int is equal to:", gross_int)
                genre = data.get('Genre', 'Not Provided')
                if genre != 'Not Provided':
                    genre = genre.split(",")[0]
                date = int(date[:4])

                Awards_Won = '0'
                if 'Awards' in data:
                    Awards = data['Awards'].split(" ")
                    for index in range(len(Awards)-1):
                        if Awards[index + 1] == 'wins' or Awards[index + 1] == 'won':
                            Awards_Won = Awards[index]
                            break
            
                ratings_dict_list = data['Ratings']
                IMD_rating = 0
                RottenTomatoes_rating = 0
                Metacritic_rating = 0
                id = 0

                for dictionary in ratings_dict_list:
                    if dictionary['Source'] == 'Internet Movie Database':
                        IMD_rating = float(dictionary.get('Value', 0).split('/')[0]) #* 10 
                    if dictionary['Source'] == 'Rotten Tomatoes':
                        RottenTomatoes_rating = dictionary.get('Value', 0)
                        RottenTomatoes_rating = float(RottenTomatoes_rating[:-1])
                    if dictionary['Source'] == 'Metacritic':
                        Metacritic_rating = dictionary.get('Value', 0)
                        Metacritic_rating = float(Metacritic_rating.split('/')[0])
                    
                # print("The date is: ", date)
                # print("The genreid is: ", genre)
                # print("gross is: ", gross_int)
                # print("awards is: ", Awards_Won)
                # print("IMBD rating is: ", IMD_rating)
                # print("metacritic rating is: ", Metacritic_rating)
                # print("rotten_tomatoe rating is: ", RottenTomatoes_rating)
    
                print(" ")

                print(count)
                print(" ") 
                cursor.execute("SELECT * FROM Genres")
                for row in cursor:
                    #print(row)
                    if genre == row[1]:
                        id = row[0]

                cursor.execute("UPDATE Movies SET genreid = ? WHERE title = ?", (id, title))
                cursor.execute("UPDATE Movies SET gross = ? WHERE title = ?", (gross, title))
                cursor.execute("UPDATE Movies SET awards = ? WHERE title = ?", (id, title))
                cursor.execute("UPDATE Movies SET imdb_rating = ? WHERE title = ?", (IMD_rating, title))
                cursor.execute("UPDATE Movies SET metascore = ? WHERE title = ?", (Metacritic_rating, title))
                cursor.execute("UPDATE Movies SET rotten_tomatoes = ? WHERE title = ?", (RottenTomatoes_rating, title))

                count += 1

                    

                #cursor.execute("UPDATE Movies SET (genreid, gross, awards, imdb_rating, metascore, rotten_tomatoes) values (?,?,?,?,?,?) ", (id, gross, Awards_Won,  IMD_rating, Metacritic_rating, RottenTomatoes_rating))
                
        conn.commit()
        if rest_rows:
            with open('movies.csv', 'w') as file:    
                writer = csv.writer(file)
                writer.writerows(rest_rows)
getRatings()