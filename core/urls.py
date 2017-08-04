from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='index'),
    # url(r'^games/(?P<steamid>[0-9]+)$', views.games, name='games'),
    url(r'^home/$', views.home, name='home'),
    url(r'^games/', views.games, name='games'),
    url(r'^friends/', views.friends, name='friends'),
    url(r'^calculator/', views.calculator, name='calculator')
    

]