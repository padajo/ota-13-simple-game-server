from django.db import models
import json

# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class Client(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def to_object(self):
        return {'pk':self.pk, 'name':self.name, 'player_count': self.player_set.count()}

class Game(TimeStampedModel):
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def to_object(self):
        return {'pk':self.pk, 'name':self.name, 'client_pk':self.client_id}

class Player(TimeStampedModel):
    game = models.ForeignKey(Game)
    device_id = models.CharField(max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def to_object(self):
        info = {'pk':self.pk, 'name':self.name, 'device_id': self.device_id, 'game_pk':self.game_id}
        items = []
        for item in self.item_set.all():
           items.append(item.to_object())
        info['items'] = items
        return info

class Item(TimeStampedModel):
    player = models.ForeignKey(Player)
    name = models.CharField(max_length=100, blank=False, null=False)
    amount = models.IntegerField(default=0)

    def to_object(self):
        return {'pk':self.pk, 'name':self.name, 'amount': self.amount, 'player_pk':self.player_id}
