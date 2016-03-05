from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login


from Guess_The_Movie.models import User
from Guess_The_Movie.models import UserProfile
from Guess_The_Movie.models import GameSession
from Guess_The_Movie.models import Question
from Guess_The_Movie.forms import UserForm, UserProfileForm

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
    return render(request, "guess_the_movie/user.html", context_dict)



def index(request):
    # Go render the response and return it to the client.
    context_dict = {}
    return render(request, "guess_the_movie/index.html", context_dict)


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
            return HttpResponse("Invalid login ")


    else:
         return render(request, 'guess_the_movie/login.html', {})