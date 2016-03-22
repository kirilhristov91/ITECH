from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from guess_the_movie.models import User
from guess_the_movie.models import UserProfile
from guess_the_movie.models import GameSession
from guess_the_movie.models import Question
from guess_the_movie.models import Movie
from guess_the_movie.models import Answer
from guess_the_movie.models import Favourites
from guess_the_movie.forms import UserForm, UserProfileForm

from random import randint
import unicodedata

# Create your views here.

coding = 'utf-8'


def index(request):
    # Go render the response and return it to the client.
    context_dict = {}
    Userstop5 = UserProfile.objects.order_by('-total_points')[:5]
    context_dict['top5Users'] = Userstop5
    return render(request, "guess_the_movie/index.html", context_dict)


def game_session(request):
    # check if the user is logged in
    if request.user.is_authenticated():
        context_dict = {}

        # add the current user object to the context_dict
        currentUser = UserProfile.objects.get(user=request.user)
        context_dict["user"] = currentUser

        # create a new game session for the current user
        gameSession = GameSession(user=currentUser)
        gameSession.save()
        context_dict['game_session'] = gameSession

        # get ten random movies using the get_movies() helper function
        movies_answers = get_movies()

        # add the movies and the answers to the context_dict
        moviesArray = movies_answers['moviesArray']
        answersArray = movies_answers['answersArray']
        context_dict["answers"] = movies_answers['moviesArray']
        context_dict["movies"] = movies_answers['answersArray']

        # create and add to the database the 10 questions for the game session
        # this is done so that later if the user guess correctly
        #   a particular question the is_guess_correct field in the database is updated to True
        i = 0
        while i < len(moviesArray):
            current_movie = moviesArray[i]
            answers = answersArray[i]
            question = Question(game_session=gameSession, movie=current_movie, index=i)
            question.save()
            for answer in answers:
                Answer(question=question, text=answer).save()
            i = i + 1

        return render(request, 'guess_the_movie/game.html', context_dict)

    # if no user is logged in return the login page
    else:
        return render(request, 'guess_the_movie/login.html', {})


# set the is_guess_correct field to True if a question during the game session is answered correctly and update the points
def update_question(request, question_id):
    if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)

        # update question
        question = Question.objects.get(id=question_id)
        question.is_guess_correct = True
        question.save()

        # update users points
        currentUser.total_points = currentUser.total_points + 1
        currentUser.save()
        return HttpResponse(status=200)
    else:
        return render(request, 'guess_the_movie/login.html', {})


# function to get 10 random movies from the database
def get_movies():
    minId = Movie.objects.order_by('id')[0].id
    maxId = Movie.objects.order_by('-id')[0].id
    moviesArray = []
    answersArray = []
    index = 0

    while index < 10:
        # generate a random id to get the corresponding movie
        randomId = randint(minId, maxId)
        movie = Movie.objects.get(id=randomId)

        # check if the movie is not already present in the movies array
        # to avoid showing the user the same movie within the same game session
        exist = False
        for m in moviesArray:
            if m.title == movie.title:
                exist = True
        if exist == True:
            continue

        # check if the alternative answers for the current movie are more than 3
        # because some of the movies contain less than three titles in other_options
        options = movie.other_options.split(", ")
        if len(options) < 3:
            continue

        # get rid of weird characters and leave only the title of the movie
        answers = []
        title = movie.title
        title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
        title = title.replace('"', "")
        title = title.lstrip()

        # choose randomly 3 other titles from the other_options
        flag = 0
        size = len(options) - 1
        while flag < 3:
            randomMovie = randint(0, size)
            # get rid of weird characters and leave only the title of the other option
            a = options.pop(randomMovie)
            a = unicodedata.normalize('NFKD', a).encode('ascii', 'ignore')
            a = a.lstrip()
            a = a.replace('"', "")
            a = a.replace('\'', '')
            a = a.replace("]", '')
            a = a.replace("[", '')
            a = a.encode('utf-8')
            if (a is title):
                continue

            # store the option in the answers array
            answers.append(a)
            flag = flag + 1
            size = size - 1

        # store the title of the movie in the answers array as well
        answers.append(title)

        # sort the array of answers
        answers = sorted(answers)
        answersArray.append(answers)
        moviesArray.append(movie)
        index = index + 1

    return {'moviesArray': moviesArray, 'answersArray': answersArray}


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
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # If it is POST request, get the information out of it
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # If it is a registered user, login
        if user:
            login(request, user)
            return HttpResponseRedirect('/guess_the_movie/')
        else:
            print "Invalid login details"
            return render(request, 'guess_the_movie/login.html', {"fail": True})

    else:
        return render(request, 'guess_the_movie/login.html', {})


def summary(request, game_session_id):
    print request.user
    if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)
        context_dict = {}
        playersAnswers = []

        gameSession = GameSession.objects.get(id=game_session_id)
        if currentUser == gameSession.user:
            correctAnswersCount = 0
            answers = Question.objects.filter(game_session=gameSession)
            playersAnswers = []
            for i in range(len(answers)):
                alreadyInFav = False
                fav = Favourites.objects.filter(movie=answers[i].movie, user=request.user)
                if len(fav) != 0:
                    alreadyInFav = True
                playersAnswers.append(
                        {'movie': answers[i].movie, 'answered': answers[i].is_guess_correct, 'fav': alreadyInFav})
                if answers[i].is_guess_correct:
                    correctAnswersCount += 1
        gameSession.points = correctAnswersCount
        gameSession.save()

        context_dict['answers'] = playersAnswers
        context_dict['correct'] = correctAnswersCount
        print context_dict
        return render(request, 'guess_the_movie/summary.html', context_dict)

    else:
        return render(request, 'guess_the_movie/login.html', {})


def add_to_favourites(request, movieId):
    if request.user.is_authenticated():
        currentUser = UserProfile.objects.get(user=request.user)
        currentMovie = Movie.objects.get(id=movieId)
        fav = Favourites(user=currentUser, movie=currentMovie)
        fav.save()
        return HttpResponse(status=200)

    else:
        return render(request, 'guess_the_movie/login.html', {})


def leaderboard(request):
    context_dict = {}
    allUsers = UserProfile.objects.order_by('-total_points')
    context_dict['allUsers'] = allUsers
    return render(request, "guess_the_movie/leaderboard.html", context_dict)


def about(request):
    return render(request, "guess_the_movie/about.html", {})


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/guess_the_movie/')


def profile(request):
    context_dict = {'userp': UserProfile.objects.get(user=request.user),
                    'userfav': Favourites.objects.filter(user=request.user)}
    numberGames = GameSession.objects.filter(user=request.user)
    max = 0
    sum = 0

    for i in range(len(numberGames)):
        tempMax = numberGames[i].points
        if tempMax > max:
            max = tempMax
        sum += tempMax

    context_dict['games'] = len(numberGames)
    context_dict['max'] = max
    if len(numberGames) == 0:
        context_dict['avg'] = 0
    else:
        context_dict['avg'] = round(float(sum) / len(numberGames), 2)

    return render(request, "guess_the_movie/profile.html", context_dict)


def upload_picture(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            currentUser = UserProfile.objects.get(user=request.user)
            upload_form = UserProfileForm(data=request.POST, )
            if upload_form.is_valid():
                upload = upload_form.save(commit=False)
                if 'picture' in request.FILES:
                    upload.picture = request.FILES['picture']

                    currentUser.picture = upload.picture
                    currentUser.save()
                    return HttpResponseRedirect('/guess_the_movie/profile')
                else:
                    print "Upload unsuccessful"
                    return render(request, 'guess_the_movie/upload_picture.html', {"fail": True})

            else:
                print upload_form.errors
    else:
        upload_form = UserProfileForm()
        return render(request, "guess_the_movie/upload_picture.html", {'upload_form': upload_form})
