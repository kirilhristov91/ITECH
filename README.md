Guess The Movie 

Guess The Movie is game application, built using Django. Each user is given 10 question, which he should answer.
Each question consist of a movie screenshot and four possible answers, from which only one is correct. The objective 
is to find the right movie. 



How to get it on your machine?
1. Clone the repository 
    git clone https://github.com/kirilhristov91/ITECH/n
    
2. Make a virtual environment using the requirement.txt file. 
3. Once you have created the virtual environment, go to ITECH/itech/itech and type 
   the following commands:
    python manage.py makemigrations 
    python manage.py migrate 
  
  They will create the model. 

4. The population script has to executed, in order for the movie to be stored in the Database. 
   Superusers will also be created. Type: 
   python populate.py 
  
5. Once you this is done, you can run the server: 
  python manage.py runserver 
  
6. Go to http://127.0.0.1:8000/guess_the_movie and start playing 


The game is already deployed at http://guessthemovie.pythonanywhere.com/guess_the_movie/
