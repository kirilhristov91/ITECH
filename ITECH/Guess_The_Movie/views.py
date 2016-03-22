from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


from Guess_The_Movie.models import User
from Guess_The_Movie.models import UserProfile
from Guess_The_Movie.models import GameSession
from Guess_The_Movie.models import Question
from Guess_The_Movie.models import Movie
from Guess_The_Movie.models import Answer
from Guess_The_Movie.models import Favourites
from Guess_The_Movie.forms import UserForm, UserProfileForm, resetPasswordForm

from random import randint

import unicodedata
# Create your views here.

coding = 'utf-8'


def userView(request, user_name):
     # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    try:
        userObject = User.objects.get(username=user_name)
        context_dict['username'] = userObject

    except User.UserDoesNotExist:
        #User does not exist
        pass

    # Go render the response and return it to the client.
    return render(request, "guess_the_movie/user.html", context_dict)



def index(request):
    # Go render the response and return it to the client.
    context_dict = {}
    Userstop5 = UserProfile.objects.order_by('-total_points')[:5]
    context_dict['top5Users']=  Userstop5
    return render(request, "guess_the_movie/index.html", context_dict)


def question(request):

    if request.method == 'GET':
        question_id = request.GET['question_id']

    points = 0
    if question_id:
        #Hardcoded to work with the user table change to work with question table
        user = UserProfile.objects.get(user=1)
        if user:
            points = user.total_points + 1
            user.total_points =  points
            user.save()
    return HttpResponse(user.total_points)


def game_session(request):
    if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)
        context_dict = {}
        context_dict["user"] = currentUser

        gameSession = GameSession(user=currentUser)
        gameSession.save()
        movies_answers = get_movies()
        moviesArray = movies_answers['moviesArray']
        answersArray = movies_answers['answersArray']
        context_dict["answers"] = movies_answers['moviesArray']
        context_dict["movies"] = movies_answers['answersArray']
        context_dict['game_session'] = gameSession

        i=0
        while i < len(moviesArray):
            current_movie = moviesArray[i]
            answers = answersArray[i]
            question = Question(game_session=gameSession, movie=current_movie, index = i)
            question.save()
            for answer in answers:
                Answer(question=question, text=answer).save()
            i = i + 1

        return render(request, 'guess_the_movie/game.html', context_dict)
    else:
        return render(request, 'guess_the_movie/login.html', {})


def update_question(request, question_id):
    if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)

        #update question
        question = Question.objects.get(id=question_id)
        question.is_guess_correct = True
        question.save()

        #update users points
        currentUser.total_points = currentUser.total_points + 1
        currentUser.save()
        return HttpResponse(status=200)
    else:
        return render(request, 'guess_the_movie/login.html', {})


def get_movies():
    minId = Movie.objects.order_by('id')[0].id
    maxId = Movie.objects.order_by('-id')[0].id
    moviesArray = []
    answersArray = []
    index = 0

    while index < 10:
        randomId = randint(minId, maxId)
        movie = Movie.objects.get(id=randomId)
        exist = False
        for m in moviesArray:
            if m.title == movie.title:
                exist = True
        if exist == True:
            continue

        options = movie.other_options.split(", ")
        if len(options) < 3:
            continue

        answers = []
         
        title = movie.title
        title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
        title = title.replace('"', "")
        title = title.lstrip()

        flag=0
        size = len(options)-1
        while flag<3:

            randomMovie = randint(0, size)
            #print len(options)
            a = options.pop(randomMovie)
            a = unicodedata.normalize('NFKD', a).encode('ascii','ignore')
            a = a.lstrip()
            a = a.replace('"', "")
            a = a.replace('\'','')
            a = a.replace("]",'')
            a = a.replace("[",'')
            a = a.encode('utf-8')
            print a
            if(a is title): continue
            answers.append(a)
            flag = flag + 1
            size = size - 1


       
        answers.append(title)
        answers = sorted(answers)
        answersArray.append(answers)
        moviesArray.append(movie)
        index = index + 1

    return {'moviesArray':moviesArray, 'answersArray':answersArray}


 # A function to get an existing question
def guestionView(request, questionID):
     # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    try:
        userObject = Question.objects.get(game_session_id=questionID)
        context_dict['question'] = userObject

    except Question.UserDoesNotExist:
        #User does not exist
        pass
    # Go render the response and return it to the client.
    return render(request, "guess_the_movie/question.html", context_dict)


def register(request):
    registered = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()


            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']


            profile.save()


            registered = True


        else:
            print user_form.errors, profile_form.errors


    else:
        user_form = UserForm()
        profile_form = UserProfileForm()


    return render(request,
            'guess_the_movie/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):
    #If it is POST request, get the information out of it
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        # If it is a registered user, login
        if user:
            login(request,user)
            return HttpResponseRedirect('/guess_the_movie/')


        else:
            print "Invalid login details"
            return render(request, 'guess_the_movie/login.html', {"fail":True})


    else:
         return render(request, 'guess_the_movie/login.html', {})


def summary(request,game_session_id):
     print request.user
     if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)
        context_dict={}
        playersAnswers=[]
        

        gameSession = GameSession.objects.get(id=game_session_id)
        if currentUser == gameSession.user:
              correctAnswersCount = 0
              answers = Question.objects.filter(game_session=gameSession)
              playersAnswers=[]
              for i in range(len(answers)):
                   alreadyInFav = False
                   fav = Favourites.objects.filter(movie=answers[i].movie, user = request.user)
                   if len(fav)!=0:
                       alreadyInFav = True
                   playersAnswers.append({'movie': answers[i].movie, 'answered': answers[i].is_guess_correct, 'fav':alreadyInFav})
                   if answers[i].is_guess_correct:
                        correctAnswersCount+=1
        gameSession.points=correctAnswersCount
        gameSession.save()


        context_dict['answers']= playersAnswers
        context_dict['correct'] = correctAnswersCount
        print context_dict
        return render(request, 'guess_the_movie/summary.html', context_dict)
     else:
         return render(request, 'guess_the_movie/login.html', {})


def add_to_favourites(request,movieId):
    if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)
        currentMovie = Movie.objects.get(id=movieId)
        fav = Favourites(user=currentUser,movie=currentMovie)
        fav.save()
        return HttpResponse(status=200)

    else:
        return render(request, 'guess_the_movie/login.html', {})




def leaderboard(request):
    context_dict = {}
    allUsers = UserProfile.objects.order_by('-total_points')
    context_dict['allUsers']= allUsers
    return render(request, "guess_the_movie/leaderboard.html", context_dict)

def about(request):
    return render(request, "guess_the_movie/about.html", {})


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/guess_the_movie/')

def profile(request):
    context_dict = {'userp':UserProfile.objects.get(user=request.user), 'userfav':Favourites.objects.filter(user=request.user)}
    numberGames = GameSession.objects.filter(user=request.user)
    max = 0
    sum = 0

    for i in range(len(numberGames)):
        tempMax = numberGames[i].points
        if tempMax > max:
            max = tempMax
        sum +=tempMax

    context_dict['games'] = len(numberGames)
    context_dict['max'] = max
    if len(numberGames)==0:
           context_dict['avg'] = 0
    else:
        context_dict['avg'] = round(float(sum)/len(numberGames),2)

    return render(request, "guess_the_movie/profile.html", context_dict)

def upload_picture(request):
     if request.method == "POST":
         if request.user.is_authenticated():
             currentUser = UserProfile.objects.get(user=request.user)
             upload_form = UserProfileForm(data = request.POST,)
             if upload_form.is_valid():
                 upload = upload_form.save(commit=False)
                 if 'picture' in request.FILES:
                    upload.picture = request.FILES['picture']

                    currentUser.picture = upload.picture
                    currentUser.save()
                    return HttpResponseRedirect('/guess_the_movie/profile')
                 else:
                    print "Upload unsuccessful"
                    return render(request, 'guess_the_movie/upload_picture.html', {"fail":True})

             else:
                 print upload_form.errors
     else:
        upload_form = UserProfileForm()
        return render(request, "guess_the_movie/upload_picture.html", {'upload_form': upload_form})

def change_password(request):
            change = False
            if request.method == 'POST':
                    resetForm = resetPasswordForm(data = request.POST,)
                    if resetForm.is_valid():
                        reset = resetForm.save()
                        reset.set_password(reset.password)
                        reset.save()

                        change = True
                    else:
                        print resetForm.errors
            else:
                resetForm = resetPasswordForm()
            return render(request,
            'guess_the_movie/change_password.html',
            {'resetForm': resetForm, 'change': change})