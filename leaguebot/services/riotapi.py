from django.conf import settings
from leaguebot.models import Player, FlexMatch, SoloMatch, Rank
import requests
import time

def headers():
	return { 'X-Riot-Token': settings.RIOT_KEY }

def addPlayer(name):
	r = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", headers=headers()).json()

	try:
		check = Player.objects.filter(account_id = r['accountId'])
		if check.count() > 0:
			player = check.first()
			player.name = r['name']
			player.save()
		else:
			player = Player(riot_id = r['id'],
							account_id = r['accountId'],
							puuid = r['puuid'],
							name = r['name'],
							profile_icon_id = r['profileIconId'],
							revision_date = r['revisionDate'],
							summoner_level = r['summonerLevel']
							)
			player.save()
			player.refresh_from_db()
			rank = Rank(player=player)
			rank.save()
		return player
	except:
		pass

	return None

def getRanks(player):
	r = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player.riot_id}", headers=headers()).json()
	try:
		rank = player.rank
	except:
		rank = Rank(player=player)

	for queue in r:
		if queue['queueType'] == "RANKED_TFT":
			rank.tft_tier = queue['tier']
			rank.tft_rank = queue['rank']
			rank.tft_lp = queue['leaguePoints']
			rank.tft_wins = queue['wins']
			rank.tft_losses = queue['losses']
		elif queue['queueType'] == "RANKED_SOLO_5x5":
			rank.solo_tier = queue['tier']
			rank.solo_rank = queue['rank']
			rank.solo_lp = queue['leaguePoints']
			rank.solo_wins = queue['wins']
			rank.solo_losses = queue['losses']
		elif queue['queueType'] == "RANKED_FLEX_SR":
			rank.flex_tier = queue['tier']
			rank.flex_rank = queue['rank']
			rank.flex_lp = queue['leaguePoints']
			rank.flex_wins = queue['wins']
			rank.flex_losses = queue['losses']
	rank.save()
	return player

def populate_solo(player):
	if player.loading_solo == True:
		return -1

	aId = player.account_id
	player.refresh_from_db()
	player.loading_solo = True
	player.save()

	count = 0

	more_matches = True
	index = 0
	most_recent = player.solomatch_set.order_by('-timestamp')
	if len(most_recent) > 0:
		most_recent = most_recent[0].timestamp
	else:
		most_recent = 0

	while more_matches:
		r = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{aId}?queue=420&season=13&beginIndex={index}", headers=headers()).json()
		if len(r['matches']) == 0:
			more_matches = False
		for match in r['matches']:

			gameId = match['gameId']
			champion = match['champion']
			season = match['season']
			timestamp = match['timestamp']
			role = match['role']
			lane = match['lane']

			if timestamp > most_recent:

				details = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matches/{gameId}", headers=headers()).json()
				time.sleep(2)

				game_version = details['gameVersion']

				participantID = 0

				for participant in details['participantIdentities']:
					if (participant['player']['accountId'] == aId):
						participantID = participant['participantId']

				win = details['participants'][participantID-1]['stats']['win']

				if participantID > 5:
					i = 5
				else:
					i = 0

				top = 0
				mid = 0
				jun = 0
				adc = 0
				sup = 0

				for j in range(5):
					p_role = details['participants'][j+i]['timeline']['role']
					p_lane = details['participants'][j+i]['timeline']['lane']
					if p_role == 'SOLO' and p_lane == 'TOP':
						top = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'SOLO' and p_lane == 'MIDDLE':
						mid = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'NONE' and p_lane == 'JUNGLE':
						jun = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'DUO_CARRY' and p_lane == 'BOTTOM':
						adc = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'DUO_SUPPORT' and p_lane == 'BOTTOM':
						sup = details['participantIdentities'][j+i]['player']['accountId']

				solo = SoloMatch(player = player,
								gameId = gameId,
								champion = champion,
								season = season,
								timestamp = timestamp,
								role = role,
								lane = lane,
								game_version = game_version,
								win = win,
								top = top,
								mid = mid,
								jun = jun,
								adc = adc,
								sup = sup)
				solo.save()

				count += 1
			else:
				more_matches = False
		index += 100

	player = player.refresh_from_db()
	player.loading_solo = False
	player.save()
	return count

def populate_flex(player):
	if player.loading_flex == True:
		return -1

	aId = player.account_id
	player.refresh_from_db()
	player.loading_flex = True
	player.save()

	count = 0
	more_matches = True
	index = 0
	most_recent = player.flexmatch_set.order_by('-timestamp')
	if len(most_recent) > 0:
		most_recent = most_recent[0].timestamp
	else:
		most_recent = 0

	while more_matches:
		r = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{aId}?queue=440&season=13&beginIndex={index}", headers=headers()).json()
		if len(r['matches']) == 0:
			more_matches = False
		for match in r['matches']:

			gameId = match['gameId']
			champion = match['champion']
			season = match['season']
			timestamp = match['timestamp']
			role = match['role']
			lane = match['lane']

			if timestamp > most_recent:

				details = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matches/{gameId}", headers=headers()).json()
				time.sleep(2)

				game_version = details['gameVersion']

				participantID = 0

				for participant in details['participantIdentities']:
					if (participant['player']['accountId'] == aId):
						participantID = participant['participantId']

				win = details['participants'][participantID-1]['stats']['win']

				if participantID > 5:
					i = 5
				else:
					i = 0

				top = 0
				mid = 0
				jun = 0
				adc = 0
				sup = 0

				for j in range(5):
					p_role = details['participants'][j+i]['timeline']['role']
					p_lane = details['participants'][j+i]['timeline']['lane']
					if p_role == 'SOLO' and p_lane == 'TOP':
						top = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'SOLO' and p_lane == 'MIDDLE':
						mid = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'NONE' and p_lane == 'JUNGLE':
						jun = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'DUO_CARRY' and p_lane == 'BOTTOM':
						adc = details['participantIdentities'][j+i]['player']['accountId']
					elif p_role == 'DUO_SUPPORT' and p_lane == 'BOTTOM':
						sup = details['participantIdentities'][j+i]['player']['accountId']

				flex = FlexMatch(player = player,
								gameId = gameId,
								champion = champion,
								season = season,
								timestamp = timestamp,
								role = role,
								lane = lane,
								game_version = game_version,
								win = win,
								top = top,
								mid = mid,
								jun = jun,
								adc = adc,
								sup = sup)
				flex.save()

				count += 1
			else:
				more_matches = False
		index += 100

	player.refresh_from_db()
	player.loading_flex = False
	player.save()
	return count
