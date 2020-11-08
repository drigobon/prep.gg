import numpy as np
import math
import urllib.request
from bs4 import BeautifulSoup



def process_champ_name(champ_name):
	champ_name_lower = champ_name.lower()
	champ_name_processed = "".join(champ_name_lower.split("'"))
	champ_name_processed_space = "".join(champ_name_processed.split(" "))
	champ_name_processed_and = champ_name_processed_space.split("&")[0]
	champ_name_processed_period = "".join(champ_name_processed_and.split("."))
	return champ_name_processed_period

def process_player_name(player_name):
	return "".join(player_name.split("_")).split("(")[0]



#############################################################################################
#	 						Leaguepedia Scraping 											#
#############################################################################################

def construct_url_for_team(team):
	url = "https://lol.gamepedia.com/" + team + "/Match_History"
	return url


def extract_table_rows_from_url(url):
	fp = urllib.request.urlopen(url)
	page_bytes = fp.read()
	page_html = page_bytes.decode("utf8")
	fp.close()
	soup = BeautifulSoup(page_html, 'html.parser')

	draft_table = soup.find_all('table',{"class": "wikitable"})[0]
	
	table_body = draft_table.find_all('tbody')[0]

	table_rows = draft_table.find_all('tr')[4:]

	return table_rows


def extract_game_from_row(row_of_interest, verbose=True):

	table_columns = row_of_interest.find_all('td')

	data = dict()

	data['patch'] = table_columns[2].get_text()
	data['win'] = int(table_columns[3].get_text() == 'Win')
	data['side'] = table_columns[4].get_text()
	data['opp'] = table_columns[5].find_all('a')[0].get('title')

	bans_tmp = table_columns[6].find_all('span')
	data['bans'] = [process_champ_name(ban.get('title')) for ban in bans_tmp]

	bans_tmp = table_columns[7].find_all('span')
	data['vs_bans'] = [process_champ_name(ban.get('title')) for ban in bans_tmp]

	picks_tmp = table_columns[8].find_all('span')
	data['picks'] = [process_champ_name(pick.get('title')) for pick in picks_tmp]

	picks_tmp = table_columns[9].find_all('span')
	data['vs_picks'] = [process_champ_name(pick.get('title')) for pick in picks_tmp]

	players_tmp = table_columns[10].find_all('a')
	data['players'] = [player.get('href').split('/')[1] for player in players_tmp]
		
	return data


def construct_url_for_player(player):
	url = "https://lol.gamepedia.com/Special:RunQuery/TournamentStatistics?TS%5Bpreload%5D=PlayerByChampion&TS%5Byear%5D=2020&TS%5Blink%5D="+player+"&pfRunQueryFormName=TournamentStatistics"

	return url


def extract_player_data_from_url(url):

	fp = urllib.request.urlopen(url)
	page_bytes = fp.read()
	page_html = page_bytes.decode("utf8")
	fp.close()
	soup = BeautifulSoup(page_html, 'html.parser')

	draft_table = soup.find_all('table',{"class": "wikitable"})[0]
	
	table_body = draft_table.find_all('tbody')[0]

	table_rows = draft_table.find_all('tr')[3:]

	return table_rows


def extract_champ_from_row(row_of_interest):
	table_columns = row_of_interest.find_all('td')

	data = dict()

	keys = ['champ', 'games', 'wins', 'losses', 'winrate', 'kills', 'deaths', 'assists', 'kda', 'cs', 'csm',
			'gold', 'gpm', 'kpar', 'killshare', 'goldshare']

	for i,key in enumerate(keys):
		if key == 'champ':
			data[key] = table_columns[i].get_text()

		else:
			try:
				data[key] = float(table_columns[i].get_text().split('%')[0])
				if math.isnan(data[key]) :
					data[key] = 'NaN'
			except:
				data[key] = 'NaN'
	return data




#############################################################################################
#	 						Gol Scraping 													#
#############################################################################################

def construct_gol_url(team, team_dict):
	url = "https://gol.gg/teams/team-stats/"+team_dict[team] + "/split-ALL/tournament-ALL/"
	return url


def extract_gol_data(url):

	fp = urllib.request.urlopen(url)
	page_bytes = fp.read()
	page_html = page_bytes.decode("utf8")
	fp.close()
	
	soup = BeautifulSoup(page_html, 'html.parser')
	data_tables = soup.find_all('table',{"class": "table_list"})

	data = dict()

	# simple team stats
	temp = data_tables[0].find_all('td',{'class': 'text-center'})

	keys = ['region', 'season', 'WL', None, 'avg_gm_dur']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] != 'WL':
				data[keys[i]] = temp[i].get_text()
			else:
				data[keys[i]] = temp[i].get_text().split(' - ')

	# bans by team
	most_banned_by = dict()
	for item in data_tables[1].find_all('td', {'class': 'text-center'}):
		most_banned_by[item.find_all('img')[0].get('alt')] = float(item.get_text().split('%')[0])
	data['most_banned_by'] = most_banned_by

	# bans against team
	most_banned_vs = dict()
	for item in data_tables[2].find_all('td', {'class': 'text-center'}):
		most_banned_vs[item.find_all('img')[0].get('alt')] = float(item.get_text().split('%')[0])
	data['most_banned_vs'] = most_banned_vs

	# economy stats
	temp = data_tables[3].find_all('tr')

	economy = dict()
	keys = [None, 'gpm', 'gdpm', 'gd15', 'csm', 'csd15', 'towerdiff15', 'towerratio','FirstTower']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='FirstTower':
				economy[keys[i]] = float(temp[i].find_all('td')[1].find_all('span')[1].get_text().split('%')[0])
			else:
				economy[keys[i]] = float(temp[i].find_all('td')[1].get_text())
	data['economy'] = economy

	# aggression stats
	temp = data_tables[4].find_all('tr')

	aggression = dict()
	keys = [None, 'dpm', 'FirstBlood', 'killsPG', 'deathsPG', 'killdeathratio', 'assistsperkill']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='FirstBlood':
				aggression[keys[i]] = float(temp[i].find_all('td')[1].find_all('span')[1].get_text().split('%')[0])
			else:
				aggression[keys[i]] = float(temp[i].find_all('td')[1].get_text())
	data['aggression'] = aggression

	# objectives stats
	temp = data_tables[5].find_all('tr')

	objectives = dict()
	keys = [None, 'dragsPG', 'drags15', 'heraldsPG', 'baronsPG']
	for i in range(len(keys)):
		if keys[i] is not None:	
			if keys[i] == 'drags15':
				objectives[keys[i]] = float(temp[i].find_all('td')[1].get_text())
			else:
				objectives[keys[i]] = float(temp[i].find_all('td')[1].get_text().split('(')[0])
				objectives[keys[i]+'Percent'] = float(temp[i].find_all('td')[1].get_text().split('(')[1].split('%')[0])

	data['objectives'] = objectives

	# vision stats
	temp = data_tables[6].find_all('tr')

	vision = dict()
	keys = [None, 'wardsPM', 'visionwardsPM', 'wardsclearedPM', 'PercWC']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='PercWC':
				vision[keys[i]] = float(temp[i].find_all('td')[1].find_all('span')[1].get_text().split('%')[0])
			else:
				vision[keys[i]] = float(temp[i].find_all('td')[1].get_text())
	data['vision'] = vision

	return data


#############################################################################################
#	 						Full Scraping 													#
#############################################################################################

def scrape_team(team, team_dict, abbrv_dict):
	team_data = dict()

	team_data['name'] = " ".join(team.split("_"))
	team_data['abbrv'] = abbrv_dict[team]


	# get teamwide data
	url = construct_gol_url(team, team_dict)
	data = extract_gol_data(url)

	team_data['team_stats'] = data


	# get leaguepedia data
	url = construct_url_for_team(team)
	table_rows = extract_table_rows_from_url(url)

	all_players = dict()
	all_games = list()
	win_seq = list()

	roles = ['top', 'jungle', 'mid', 'adc', 'sup']

	blue_wins = 0
	blue_games = 0
	red_wins = 0
	red_games = 0

	for row in table_rows:
		game = extract_game_from_row(row, False)

		if game['side'] == 'Blue':
			blue_games += 1
			blue_wins += game['win']
		else:
			red_games += 1
			red_wins += game['win']

		win_seq.append(game['win'])
		all_games.append(game)

		for (i,player) in enumerate(game['players']):
			if player.lower() not in set([key.lower() for key in all_players.keys()]):
				all_players[player] = {'role': roles[i]}

	team_data['team_stats']['blue_winrate'] = round(100*blue_wins/blue_games,1)
	team_data['team_stats']['red_winrate'] = round(100*red_wins/red_games,1)
	team_data['recent_game_results'] = win_seq


	# get player-specific data
	all_player_champs = dict()

	for player in list(all_players.keys()):

		url = construct_url_for_player(player)
		rows = extract_player_data_from_url(url)

		player_champs = dict()

		n_games = 0

		for row in rows: 
			try:
				data = extract_champ_from_row(row)

				player_champs[data['champ']] = data

				n_games += int(data['games'])
			except:
				pass

		for key in player_champs.keys():
			player_champs[key]['pickrate'] = round(100*player_champs[key]['games']/n_games, 1)


		avg_kda = list()
		avg_k = list()
		avg_d = list()
		avg_a = list()
		avg_kp = list()
		avg_ks = list()
		avg_gs = list()

		avg_kda_den = list()
		avg_k_den = list()
		avg_d_den = list()
		avg_a_den = list()
		avg_kp_den = list()
		avg_ks_den = list()
		avg_gs_den = list()

		for key in player_champs.keys():
			try:
				avg_kda.append(player_champs[key]['kda']*player_champs[key]['pickrate'])
				avg_kda_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'kda error')

			try:
				avg_k.append(player_champs[key]['kills']*player_champs[key]['pickrate'])
				avg_k_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'k error')

			try:
				avg_d.append(player_champs[key]['deaths']*player_champs[key]['pickrate'])
				avg_d_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'd error')

			try:
				avg_a.append(player_champs[key]['assists']*player_champs[key]['pickrate'])
				avg_a_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'a error')

			try:
					avg_kp.append(player_champs[key]['kpar']*player_champs[key]['pickrate'])
					avg_kp_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'kp error')

			try:
				avg_ks.append(player_champs[key]['killshare']*player_champs[key]['pickrate'])
				avg_ks_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'ks error')

			try:
				avg_gs.append(player_champs[key]['goldshare']*player_champs[key]['pickrate'])
				avg_gs_den.append(player_champs[key]['pickrate'])
			except:
				print(player, key, 'gs error')

		all_players[player]['avg_kda'] = round(np.sum(avg_kda)/np.sum(avg_kda_den),1)
		all_players[player]['avg_k'] = round(np.sum(avg_k)/np.sum(avg_k_den),1)
		all_players[player]['avg_d'] = round(np.sum(avg_d)/np.sum(avg_d_den),1)
		all_players[player]['avg_a'] = round(np.sum(avg_a)/np.sum(avg_a_den),1)
		all_players[player]['avg_kp'] = round(np.sum(avg_kp)/np.sum(avg_kp_den),1)
		all_players[player]['avg_ks'] = round(np.sum(avg_ks)/np.sum(avg_ks_den),1)
		all_players[player]['avg_gs'] = round(np.sum(avg_gs)/np.sum(avg_gs_den),1)


		
		all_player_champs[process_player_name(player)] = player_champs



	team_data['player_champ_stats'] = all_player_champs

	all_players_clean = dict()
	for player in all_players.keys():
		all_players_clean[process_player_name(player)] = all_players[player]

	team_data['player_stats'] = all_players_clean

	return team_data