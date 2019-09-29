from django.conf import settings
from leaguebot.models import Player, FlexMatch, SoloMatch
import requests

def headers():
	return { 'X-Riot-Token': settings.RIOT_KEY }

def addPlayer(name):
	r = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", headers=headers()).json()

	# player = Player(riot_id = r['id'],
	# 				account_id = r['accountId'],
	# 				name = r['name'],
	# 				profile_icon_id = r['profileIconId'],
	# 				revision_date = r['revisionDate'],
	# 				summoner_level = r['summonerLevel']
	# 				)
	# player.save()
	# player.refresh_from_db()
	return player

def populate_solo(player):
	if player.loading_solo == True:
		return -1

	aId = player.account_id
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

	player.refresh_from_db()
	player.loading_solo = False
	player.save()
	return count

def populate_flex(player):
	if player.loading_flex == True:
		return -1

	aId = player.account_id
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
