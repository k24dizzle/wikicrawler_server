from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'go/', views.go, name='game_start'),
    url(r'(?P<game_id>[0-9]+)/(?P<page_name>.+)', views.step, name='go_to_page'),
    url(r'win/(?P<game_id>[0-9]+)/', views.win, name="game_win")
]
