from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from guess_the_movie.models import Movie
from guess_the_movie.models import UserProfile
from guess_the_movie.models import Favourites
from django.core.urlresolvers import reverse


class GuessTheMovieMethodTests(TestCase):

    def test_ensure_create_user(self):
        """
        Ensures that creating a user and a userProfile works
        """
        u=User.objects.create_superuser("testUser", 'testMail', 'testPassword')
        u.save()
        up = UserProfile(user=u)
        up.save()
        u1 = UserProfile.objects.get(pk=up.pk)
        self.assertEqual((u1.user.username == "testUser"), True)

    def test_ensure_points_are_updated(self):
        """
        Ensures that points could be updated for a particular user
        """
        u=User.objects.create_superuser("testUser", 'testMail', 'testPassword')
        u.save()
        up = UserProfile(user=u)
        up.save()
        u1 = UserProfile.objects.get(pk=up.pk)
        u1.total_points += 1
        u1.save()
        testU = UserProfile.objects.get(pk=up.pk)
        self.assertEqual((testU.total_points > 0), True)

    def test_ensure_movie_get_saved(self):
        """
        Ensures that a movie can be successfully added to the Movie table
        """
        m = Movie(imdb_id='tt9999999', title="testMovie", image_url="http://someImageUrl.jpg", poster_url="http://somePosterUrl.jpg", other_options=[])
        m.save()
        m1 = Movie.objects.get(imdb_id='tt9999999')
        self.assertEqual((m1.title == "testMovie"), True)

    def test_adding_favourite(self):
        """
        Ensures that a favourite movie can be added to a particular user`s favourite movies
        """
        u=User.objects.create_superuser("testUser", 'testMail', 'testPassword')
        u.save()
        up = UserProfile(user=u)
        up.save()
        m = Movie(imdb_id='tt9999999', title="testMovie", image_url="http://someImageUrl.jpg", poster_url="http://somePosterUrl.jpg", other_options=[])
        m.save()
        fav = Favourites(user=up, movie=m)
        fav.save()
        favMov = Favourites.objects.get(user=up)
        self.assertEqual((favMov.movie.title == "testMovie"), True)

    def test_loggedin_to_play(self):
        """
        Ensures that the user can not play the game if he/she is not logged in
        """
        response = self.client.get(reverse('game'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log in to continue to Guess The Movie")
