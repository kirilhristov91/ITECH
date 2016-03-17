import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITECH.settings')

import django
django.setup()

import csv
import sys

      
from Guess_The_Movie.models import Movie, UserProfile
from django.contrib.auth.models import User

def populate():
    addUser('admin', 'admin')
    addUser('leifos', 'leifos')
    addUser('laura','laura')
    addUser('david','david')
    addAllMovies(); 

    for m in Movie.objects.all():
            print "- " + str(m)
    
def addAllMovies():
    #open the csv file with movies 
    f = open('movieInfo.csv','rt')
    reader = csv.reader(f)
    for row in reader: 
        add_Movie(row[0],row[1],row[2],row[3],row[4])

def add_Movie(imdbid,title, poster, screenshot, options):
    m = Movie.objects.create(title=title)
    m.imdb_id=imdbid
    m.image_url= screenshot 
    m.poster_url = poster
    m.other_options = options
    m.save()
    return m

def addUser(username, password):
    User.objects.create_superuser(username, '', password)


# Start execution here!
if __name__ == '__main__':
    print "Starting Guess_The_Movie population script..."
    populate()
