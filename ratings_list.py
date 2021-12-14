import requests
import re
import csv
import json
import sqlite3
import time


def getRatings():
    # This function gathers data from the omdb api, 20 items at a time. It accesses the movie titles in the movie.csv file in order to 
    # pull multiple movie metrics from the api. This pulled data is then places into the tables of the movieData.db 
    # database.

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
            if count == 20:
                rest_rows.append(row)
                continue
            title = row[0]
            parameters = {'t': title, 'apikey': api_key}
            response_obj = requests.get('https://www.omdbapi.com/', params=parameters)
            data = response_obj.json()
            #print(data)
            if 'Error' not in data:
                date = data.get('Year', 0)
                gross = data.get('BoxOffice', "$0")
                if gross == 'N/A':
                    gross = 0
                else:
                    gross_list = (gross[1:].split(","))
                    gross_int = ""
                    for num in gross_list:
                        gross_int += num
                    gross = int(gross_int)
                #print("gross_int is equal to:", gross_int)
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
    
                #print(" ")

                #print(count)
                #print(" ") 
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


def ratings_csv(filename):
    # This function takes in a csv filename as input, and selects data from the joined tables, Movies and Genres. 
    # This data is then used to calculate the average critic rating. This calculation is then output into
    # the ratings.csv file along with the movie title, gross, release date, and movie type.


    header = ('Movie Title', 'Movie Date', 'Average Rating', 'Gross', 'Movie Type')

    dbName ='movieData.db'
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Movies JOIN Genres ON Movies.genreid = Genres.id WHERE imdb_rating != ? AND metascore != ? AND rotten_tomatoes != ?',(0,0,0,))
    with open(filename, 'w', newline ='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for row in cursor:
            #print(row)
            imdb = row[-6]* 10
            meta = row[-5]
            rotten = row[-4]
            label = row[-3]
            gross = row[4]
            #print(row)
            #print(imdb,meta,rotten)
            score = (float(imdb)+float(meta)+float(rotten))
            avg = score//3
            #print(avg,score)
            ro = list(row)
            #print(avgscore)
            r = [ro[1],ro[2],avg,gross,label]
            #print(r)
            writer.writerow(r)


def main():
    # This function calls the above functions, getRatings, and ratings_csv. In order to gather enough data from 
    # the api, getRatings is called within a for loop, multiple times.

    for i in range(1,11):
        time.sleep(1)
        getRatings()
        hm = (i*25)
        print(str(hm) + ' Items Collected')
    
    ratings_csv('ratings.csv')
    
main()