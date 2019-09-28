from django.db import models

class Player(models.Model):
	riot_id = models.BigIntegerField()
	account_id = models.BigIntegerField()
	name = models.CharField(max_length=200)
	profile_icon_id = models.IntegerField()
	revision_date = models.BigIntegerField()
	summoner_level = models.IntegerField()
	loading_solo = models.BooleanField(default=False)
	loading_flex = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class SoloMatch(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	gameId = models.BigIntegerField()
	champion = models.IntegerField()
	season = models.IntegerField()
	timestamp = models.BigIntegerField()
	role = models.CharField(max_length=200)
	lane = models.CharField(max_length=200)
	game_version = models.CharField(max_length=200)
	win = models.BooleanField()
	top = models.BigIntegerField(default=0)
	mid = models.BigIntegerField(default=0)
	jun = models.BigIntegerField(default=0)
	adc = models.BigIntegerField(default=0)
	sup = models.BigIntegerField(default=0)

	def __str__(self):
		return f"{self.player} {self.gameId}"

class FlexMatch(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	gameId = models.BigIntegerField()
	champion = models.IntegerField()
	season = models.IntegerField()
	timestamp = models.BigIntegerField()
	role = models.CharField(max_length=200)
	lane = models.CharField(max_length=200)
	game_version = models.CharField(max_length=200)
	win = models.BooleanField()
	top = models.BigIntegerField(default=0)
	mid = models.BigIntegerField(default=0)
	jun = models.BigIntegerField(default=0)
	adc = models.BigIntegerField(default=0)
	sup = models.BigIntegerField(default=0)

	def __str__(self):
		return f"{self.player} {self.gameId}"
