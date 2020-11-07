import numpy as np

from utils import *
import models


if __name__ == "__main__":

	teams = ['DAMWON_Gaming', 'DRX', 'FlyQuest', 'Fnatic', 'G2_Esports', 'Gen.G', 'JD_Gaming', 'LGD_Gaming', 'Machi_Esports', 'PSG_Talon', 'Rogue_(European_Team)', 'Suning', 'Team_Liquid', 'Team_SoloMid', 'Top_Esports', 'Unicorns_Of_Love.CIS', ]

#	for team in teams:

	team = 'Team_SoloMid'

	url = construct_url_for_team(team)
	table_rows = extract_table_rows_from_url(url)

	all_players = set()
	all_games = list()

	for row in table_rows:
		game = extract_game_from_row(row, True)

		all_games.append(game)
		all_players = set(list(all_players) + game.players)

	print(all_players)





	# Given data, run analysis




