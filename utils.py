import urllib.request
from bs4 import BeautifulSoup

from models import LeagueGame


def process_champ_name(champ_name):
	champ_name_lower = champ_name.lower()
	champ_name_processed = "".join(champ_name_lower.split("'"))
	champ_name_processed_space = "".join(champ_name_processed.split(" "))
	champ_name_processed_and = champ_name_processed_space.split("&")[0]
	champ_name_processed_period = "".join(champ_name_processed_and.split("."))
	return champ_name_processed_period


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

	game = LeagueGame(data)

	if verbose:
		print("game picked champs: ", game.picks)
		print("game vs picked champs: ", game.vs_picks)
		print("game win: ", game.win)
		print("game patch: ", game.patch)
		print()

		
	return game


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

	keys = ['champ', 'games', 'wins', 'losses', 'winrate', 'kills', 'deaths', 'assists','kda', 'cs', 'csm',
			'gold', 'gpm', 'kpar', 'killshare', 'goldshare']

	for i in range(len(keys)):
		data[keys[i]] = table_columns[i].get_text()
	
	return data




#############################################################################################
#	 						Gol Scraping 													#
#############################################################################################

def construct_gol_url(team):

	team_dict = {'Team_Liquid': '876', 'Team_SoloMid': '877', 'FlyQuest': '873',
				 'DAMWON_Gaming': '849', 'DRX': '853', 'Gen.G': '852',
				 'Top_Esports': '829', 'JD_Gaming': '836', 'Suning': '834', 'LGD_Gaming': '840',
				 'G2_Esports': '891', 'Fnatic': '890', 'Rogue_(European_Team)': '895',
				 'Machi_Esports': '976', 'PSG_Talon': '982', 'Unicorns_Of_Lov.CIS': '1014'}

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
		most_banned_by[item.find_all('img')[0].get('alt')] = item.get_text()
	data['most_banned_by'] = most_banned_by

	# bans against team
	most_banned_vs = dict()
	for item in data_tables[2].find_all('td', {'class': 'text-center'}):
		most_banned_vs[item.find_all('img')[0].get('alt')] = item.get_text()
	data['most_banned_vs'] = most_banned_vs

	# economy stats
	temp = data_tables[3].find_all('tr')

	economy = dict()
	keys = [None, 'gpm', 'gdpm', 'gd15', 'csm', 'csd15', 'towerdiff15', 'towerratio','FirstTower']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='FirstTower':
				economy[keys[i]] = temp[i].find_all('td')[1].find_all('span')[1].get_text()
			else:
				economy[keys[i]] = temp[i].find_all('td')[1].get_text()
	data['economy'] = economy

	# aggression stats
	temp = data_tables[4].find_all('tr')

	aggression = dict()
	keys = [None, 'dpm', 'FirstBlood', 'killsPG', 'deathsPG', 'killdeathratio', 'assistsperkill']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='FirstBlood':
				aggression[keys[i]] = temp[i].find_all('td')[1].find_all('span')[1].get_text()
			else:
				aggression[keys[i]] = temp[i].find_all('td')[1].get_text()
	data['aggression'] = aggression

	# objectives stats
	temp = data_tables[5].find_all('tr')

	objectives = dict()
	keys = [None, 'dragsPG', 'drags15', 'heraldsPG', 'baronsPG']
	for i in range(len(keys)):
		if keys[i] is not None:	
			objectives[keys[i]] = temp[i].find_all('td')[1].get_text()
	data['objectives'] = objectives

	# vision stats
	temp = data_tables[6].find_all('tr')

	vision = dict()
	keys = [None, 'wardsPM', 'visionwardsPM', 'wardsclearedPM', 'PercWC']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='PercWC':
				vision[keys[i]] = temp[i].find_all('td')[1].find_all('span')[1].get_text()
			else:
				vision[keys[i]] = temp[i].find_all('td')[1].get_text()
	data['vision'] = vision

	return data