# api
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from gameserver.views import *

urlpatterns = patterns('',
    url(r'^api/(?P<pk>\d+)/games/?$', ClientGameListJSONView.as_view(), name='client_game_list'),
    url(r'^api/(?P<client_pk>\d+)/games/(?P<pk>\d+)/players/?$', GamePlayerListJSONView.as_view(), name='client_game_players'),
    url(r'^api/(?P<client_pk>\d+)/games/(?P<game_pk>\d+)/players/(?P<pk>\d+)/?$', GamePlayerInfoJSONView.as_view(), name='client_game_player_info'),
    url(r'^api/(?P<client_pk>\d+)/games/(?P<pk>\d+)/players/add/?$', GamePlayerJoinGameJSONView.as_view(), name='client_game_player_join'),
    url(r'^api/(?P<client_pk>\d+)/games/(?P<pk>\d+)/players/delete/?$', GamePlayerLeaveGameJSONView.as_view(), name='client_game_player_leave'),


    url(r'^api/(?P<client_pk>\d+)/games/(?P<game_pk>\d+)/players/(?P<player_pk>\d+)/items/add?$', GamePlayerAddItemJSONView.as_view(), name='player_add_item'),
    url(r'^api/(?P<client_pk>\d+)/games/(?P<game_pk>\d+)/players/(?P<player_pk>\d+)/items/(?P<item_name>\w+)/update/?$', GamePlayerUpdateItemJSONView.as_view(), name='player_update_item'),
    url(r'^api/(?P<client_pk>\d+)/games/(?P<game_pk>\d+)/players/(?P<player_pk>\d+)/items/(?P<item_name>\w+)/delete/?$', GamePlayerDeleteItemJSONView.as_view(), name='player_delete_item'),


)
