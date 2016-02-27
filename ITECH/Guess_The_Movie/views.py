from django.shortcuts import render
from Guess_The_Movie.models import User
from Guess_The_Movie.models import UserProfile
from Guess_The_Movie.models import GameSession
from Guess_The_Movie.models import Question

# Create your views here.


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
    return render(request, "Guess_The_Movie/user.html", context_dict)



def index(request):
    context_dict={}
    # Go render the response and return it to the client.
    return render(request, "Guess_The_Movie/index.html", context_dict)


 # A function to get an existing question
def guestionView(request, questionID):
     # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    try:
        userObject = Question.objects.get(game_session_id=questionID)
        context_dict['question'] = userObject

    except Guestion.UserDoesNotExist:
        #User does not exist
        pass
    # Go render the response and return it to the client.
    return render(request, "Guess_The_Movie/question.html", context_dict)




