from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'itech.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #
    url(r'^admin/', include(admin.site.urls)),
    url(r'^guess_the_movie/', include('guess_the_movie.urls')), # ADD THIS NEW TUPLE!
)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )