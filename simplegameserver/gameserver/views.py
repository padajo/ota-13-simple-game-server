# Create your views here.
from django.views.generic import DetailView, ListView, UpdateView
from django.core import serializers
from gameserver.models import Client, Game, Player, Item
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from braces.views import JSONResponseMixin, CsrfExemptMixin
from django.http import Http404

class ClientGameListJSONView(JSONResponseMixin, ListView):
    model = Client
    
    def get_queryset(self):
        client_pk = self.kwargs.get("pk")
        client = get_object_or_404(Client, pk=client_pk) 
        return client.game_set.all()

    def get(self, request, *args, **kwargs):
        games = []
        for game in self.get_queryset():
            games.append(game.to_object())
        return self.render_json_response(games)
    
class GamePlayerListJSONView(JSONResponseMixin, ListView):
    model = Game
    
    def get_queryset(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        return game.player_set.all()

    def get(self, request, *args, **kwargs):
        players = []
        for player in self.get_queryset():
            players.append(player.to_object())
        return self.render_json_response(players)

class GamePlayerInfoJSONView(JSONResponseMixin, DetailView):
    model = Player

    def get_object(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("game_pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        player_pk = self.kwargs.get("pk")
        player = get_object_or_404(Player, game=game, pk=player_pk)
        return player

    def get(self, request, *args, **kwargs):
        return self.render_json_response(self.get_object().to_object())

class GamePlayerJoinGameJSONView(JSONResponseMixin, CsrfExemptMixin, UpdateView):
    model = Game

    def get_object(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        return game

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        device_id = request.POST.get('device_id', '') 
        game = self.get_object()
        try:
            player = game.player_set.create(name=name, device_id=device_id)
            return self.render_json_response(player.to_object())
        except Exception as e:
            return self.render_json_response({'success':False, 'code': 6, 'msg':str(e)})

class GamePlayerLeaveGameJSONView(JSONResponseMixin, CsrfExemptMixin, UpdateView):
    model = Game

    def get_object(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        return game

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        device_id = request.POST.get('device_id', '') 
        game = self.get_object()
        try:
            player = game.player_set.get(device_id=device_id)
            player.delete()
            return self.render_json_response({'success':True})
        except Exception as e:
            return self.render_json_response({'success':False, 'code': 5, 'msg':str(e)})


class GamePlayerAddItemJSONView(JSONResponseMixin, CsrfExemptMixin, UpdateView):
    model = Player

    def get_object(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("game_pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        player_pk = self.kwargs.get("player_pk")
        player = get_object_or_404(Player, game=game, pk=player_pk)
        return player

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '') 
        amount = request.POST.get('amount', '') 
        player = self.get_object()
        item_exists = (player.item_set.filter(name=name).count() > 0)
        if item_exists:
            return self.render_json_response({'success':False, 'code': 2, 'msg':'Item with that name exists. Please use update not add.'})
        try:
            item = player.item_set.create(name=name, amount=amount)
            return self.render_json_response(item.to_object())
        except Exception as e:
            return self.render_json_response({'success':False, 'code': 1, 'msg':str(e)})

class GamePlayerUpdateItemJSONView(JSONResponseMixin, CsrfExemptMixin, UpdateView):
    model = Item

    def get_object(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("game_pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        player_pk = self.kwargs.get("player_pk")
        player = get_object_or_404(Player, game=game, pk=player_pk)
        item_name = self.kwargs.get("item_name")
        item = get_object_or_404(Item, player=player, name=item_name)
        return item

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        amount = request.POST.get('amount', '')
        try:
            item.amount = amount
            item.save()
            return self.render_json_response(item.to_object())
        except Exception as e:
            return self.render_json_response({'success':False, 'code': 3, 'msg':str(e)})

class GamePlayerDeleteItemJSONView(JSONResponseMixin, CsrfExemptMixin, UpdateView):
    model = Item

    def get_object(self):
        client_pk = self.kwargs.get("client_pk")
        client = get_object_or_404(Client, pk=client_pk)
        game_pk = self.kwargs.get("game_pk")
        game = get_object_or_404(Game, client=client, pk=game_pk)
        player_pk = self.kwargs.get("player_pk")
        player = get_object_or_404(Player, game=game, pk=player_pk)
        item_name = self.kwargs.get("item_name")
        item = get_object_or_404(Item, player=player, name=item_name)
        return item

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        try:
            item.delete()
            return self.render_json_response({'success':True})
        except Exception as e:
            return self.render_json_response({'success':False, 'code': 4, 'msg':str(e)})


