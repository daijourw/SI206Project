import requests
import re
import csv
import json

#possibly use dictionary instead of csv bc of racing issue

def getRatings():
    api_key = 'd8af6faf'

    with open('movies.csv', 'r') as file:
        reader = csv.reader(file)
        row_counter = 0
        count = 0
        for row in reader:
            if row_counter == 0:
                row_counter += 1

            elif row_counter != 0:
                title = row[0]
                parameters = {'t': title, 'apikey': api_key}
                response_obj = requests.get('https://www.omdbapi.com/', params=parameters)
                data = response_obj.json()
                print(data)
                print(" ")
                count += 1
                print(count)
                print(" ")
            

getRatings()