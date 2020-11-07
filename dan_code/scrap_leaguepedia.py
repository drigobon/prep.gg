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
	data['players'] = [player.get('data-to-id') for player in players_tmp]

	game = LeagueGame(data)

	if verbose:
		print("game picked champs: ", game.picks)
		print("game vs picked champs: ", game.vs_picks)
		print("game win: ", game.win)
		print("game patch: ", game.patch)
		print()

		
	return game



if __name__ == "__main__":
	# scrap every row
	url = construct_url_for_team("Team_Liquid")

	table_rows = extract_table_rows_from_url(url)

	for row in table_rows:
		extract_game_from_row(row, True)


