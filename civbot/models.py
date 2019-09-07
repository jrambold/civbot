from django.db import models
from django.utils import timezone

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    player = models.CharField(max_length=200)
    turn = models.IntegerField()
    updated = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=200)
    steamName = models.CharField(max_length=200)
    slackNotification = models.BooleanField(default=True)
    slackId = models.CharField(max_length=200, blank=True)
    discordNotification = models.BooleanField(default=False)
    discordId = models.CharField(max_length=200, blank=True)
    emailNotification = models.BooleanField(default=False)
    email = models.EmailField(max_length=200, blank=True)

    def __str__(self):
        return self.name
