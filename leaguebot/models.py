from django.db import models

class Player(models.Model):
	riot_id = models.CharField(max_length=200)
	account_id = models.CharField(max_length=200)
	puuid = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	profile_icon_id = models.IntegerField()
	revision_date = models.BigIntegerField()
	summoner_level = models.IntegerField()
	loading_solo = models.BooleanField(default=False)
	loading_flex = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Rank(models.Model):
	player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
	tft_tier = models.CharField(max_length=200, default="IRON")
	tft_rank = models.CharField(max_length=200, default="V")
	tft_lp = models.IntegerField(default=0)
	tft_wins = models.IntegerField(default=0)
	tft_losses = models.IntegerField(default=0)
	solo_tier = models.CharField(max_length=200, default="IRON")
	solo_rank = models.CharField(max_length=200, default="V")
	solo_lp = models.IntegerField(default=0)
	solo_wins = models.IntegerField(default=0)
	solo_losses = models.IntegerField(default=0)
	flex_tier = models.CharField(max_length=200, default="IRON")
	flex_rank = models.CharField(max_length=200, default="V")
	flex_lp = models.IntegerField(default=0)
	flex_wins = models.IntegerField(default=0)
	flex_losses = models.IntegerField(default=0)

	def __str__(self):
		return self.player.name

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
	top = models.CharField(max_length=200, default='0')
	mid = models.CharField(max_length=200, default='0')
	jun = models.CharField(max_length=200, default='0')
	adc = models.CharField(max_length=200, default='0')
	sup = models.CharField(max_length=200, default='0')

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
	top = models.CharField(max_length=200, default='0')
	mid = models.CharField(max_length=200, default='0')
	jun = models.CharField(max_length=200, default='0')
	adc = models.CharField(max_length=200, default='0')
	sup = models.CharField(max_length=200, default='0')

	def __str__(self):
		return f"{self.player} {self.gameId}"
