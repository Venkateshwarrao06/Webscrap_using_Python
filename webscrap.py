# Import Pakages
import os 
import requests 
from bs4 import BeautifulSoup 
from tqdm import tqdm 
import pandas as pd

# GET Request from URL
url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm" 
response = requests.get(url)

# Parse the HTML using Beautiful Soup
if response.ok: 
    data = BeautifulSoup(response.text,"html.parser") 
else: 
    print("Error")

# Pretiffy the Data
print(data.prettify())

# Find all data from Table with Class name "titleCloumn"
movie_info = data.findAll("td", {"class": "titleColumn"})

# Find all data from Table with Class name "ratingColumn imdbRating"
ratings_info = data.findAll("td", {"class": "ratingColumn imdbRating"})

# Print lenght of Movie Info and Ratings Info lists
print('movie_info : '+str(len(movie_info)),'ratings : '+str(len(ratings_info)))

# Create an Empty lists
movie_name = [] 
movie_cast = [] 
movie_year = [] 
velocity = [] 
ratings = []

# Append the data to lists
for i in tqdm(range(len(movie_info))): 
    try: 
        movie_name.append(movie_info[i].find('a').text) 
    except:
        movie_name.append("") 
    try: 
        movie_cast.append(movie_info[i].find('a').get('title')) 
    except: 
        movie_cast.append("") 
    try: 
        movie_year.append(movie_info[i].find('span').text) 
    except: 
        movie_year.append("") 
    try: 
        velocity.append(movie_info[i].findAll("div", {"class": "velocity"})[0].text.replace("\n"," ")) 
    except: 
        velocity.append("") 
    try: 
        ratings.append(ratings_info[i].find('strong').get('title')) 
    except: 
        ratings.append("")

# Zip all the lists
rows = zip(movie_name,movie_cast,movie_year,velocity,ratings)

# Create a Dataframe with Columns and store the rows to DataFrame
movie_data = pd.DataFrame(rows) 
movie_data.columns = ['Movie Name','Cast','Year','Velocity','Ratings Info']

# Print the DataFrame
print(movie_data.head())
print(movie_data.shape)

# DataFrame to CSV or Excel format
#CSV Format
movie_data.to_csv('IMDb Movie data.csv')
#Excel Format
movie_data.to_excel('IMDb Movie data.xlsx')