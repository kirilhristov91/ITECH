import requests 
import os 
import re
import json
from random import randint 
import random
import string
import csv


CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
SIMILAR_PATH = 'https://api.themoviedb.org/3/movie/{imdbid}?api_key=e14d30d8866462614fa0b5a19b45e26f&append_to_response=similar_movies' 
KEY = 'e14d30d8866462614fa0b5a19b45e26f'



def _get_json(url):
    r = requests.get(url)
    return r.json()
    
#reads a csv file in the format imdbid, movie title 
#returns it as array of dictionaries with keys id and title 
def readCSV(filename):
    f = open(filename, 'rt')
    reader = csv.reader(f)
    print f
    movieArr = []
    for row in reader: 
        movieArr.append({'id':row[0], 'title':row[1]})
    return movieArr


#makes an api call and returns an url for a movie poster
def getPosterUrl(imdbid):
   
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

   
    posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
    rel_path = posters[0]['file_path']
    url = "{0}{1}{2}".format(base_url, 'original', rel_path)

      
    return url


#makes an api call and returns an url for a movie still
def getStillUrl(imdbid):
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    stills = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['backdrops']

    stillNumber = random.randint(0,(len(stills)-1))
    rel_path = stills[stillNumber]['file_path']
    url = "{0}{1}{2}".format(base_url, 'original', rel_path)
    
    return url

#makes an api call and returns a list of similar movies 
def getSimilarMovies(imdbid):
    listOfSimilar = []
    similarMovies = _get_json(SIMILAR.format(key=KEY,imdbid=movies[i]['id']))['similar_movies']['results']
        for movie in similarMovies:
            listOfSimilar.append(p['title'].replace(',','').encode('utf-8'))


#generates a csv which will be used for populating a database from a list of movies
#format of the file is [imdbid, movietitle, posterurl, still url, similar movies]
def generateMovieCSV(movies):
    f = csv.writer(open('guessTheMovieMovies.csv', 'w'))
    for i in range(len(movies)):
        movieId=movies[i]['id']
        poster = getPosterUrl(movieId)
        still = getStillUrl(movieId)
        similar = getSimilarMovies(movieId)   
        f.writerow ( [movieId,movies[i]['title'],poster, still, similar])
        print 'Movie Generated'
       


if __name__=="__main__":
    movies = readCSV("movieList.csv")
    generateMovieCSV(movies)