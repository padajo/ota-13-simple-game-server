"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from gameserver.models import *

class ClientTestCase(TestCase):
    
    def setUp(self):
        self.test_client = Client.objects.create(name='RockPaperScissorsLizardSpock')
        
        self.test_client.game_set.create(name="game 1")
        self.test_client.game_set.create(name="game 2")
        self.test_client.game_set.create(name="game 3")
        self.test_client.game_set.create(name="game 4")
        
        self.game = self.test_client.game_set.get(name="game 1")
        
        self.game.player_set.create(name="Player 1", device_id="1234")
        self.game.player_set.create(name="Player 2", device_id="4567")
        self.game.player_set.create(name="Player 3", device_id="8765")
    
    def test_client_creation(self):
        self.assertEqual(Client.objects.count(), 1)
    
    def test_client_game_creation(self):
        self.assertEqual(Game.objects.count(), 4)
    
    def test_client_game_player_list(self):
        self.assertEqual(Player.objects.count(), 3)
    
    
        
