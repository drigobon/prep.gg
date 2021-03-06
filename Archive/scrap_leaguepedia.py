import numpy as np
import pandas as pd

import json

from utils import *


if __name__ == "__main__":

	all_team_data = dict()

	teams = ['DAMWON_Gaming', 'DRX', 'FlyQuest', 'Fnatic', 'G2_Esports', 'Gen.G', 'JD_Gaming',
			 'LGD_Gaming', 'Machi_Esports', 'PSG_Talon', 'Rogue_(European_Team)', 'Suning',
			 'Team_Liquid', 'Team_SoloMid', 'Top_Esports', 'Unicorns_Of_Love.CIS']

	for team in teams:
		team_data = dict()

		# get leaguepedia data
		url = construct_url_for_team(team)
		table_rows = extract_table_rows_from_url(url)

		all_players = set()
		all_games = list()
		win_seq = list()

		for row in table_rows:
			game = extract_game_from_row(row, False)

			win_seq.append(game.win)
			all_games.append(game)
			all_players = set(list(all_players) + game.players)

		#print(all_players)

		team_data['recent_game_results'] = win_seq

		# get player-specific data
		all_player_champs = dict()

		for player in list(all_players):
			url = construct_url_for_player(player)
			rows = extract_player_data_from_url(url)

			player_champs = dict()

			for row in rows:
				try:
					data = extract_champ_from_row(row)

					player_champs[data['champ']] = data
				except:
					pass

			all_player_champs[player] = player_champs

		#print(all_player_champs)

		team_data['player_stats'] = all_player_champs

		# get teamwide data
		url = construct_gol_url(team)
		data = extract_gol_data(url)

		#print(data)

		team_data['team_stats'] = data


		

		all_team_data[team] = team_data



















	# n_games = {player: dict() for player in all_players}
	# n_wins = {player: dict() for player in all_players}

	# for game in all_games:

	# 	curr_players = game.players
	# 	curr_champs = game.picks

	# 	for i in range(len(curr_players)):

	# 		if curr_champs[i] not in set(n_games[curr_players[i]].keys()):
	# 			n_games[curr_players[i]][curr_champs[i]] = 1
	# 			n_wins[curr_players[i]][curr_champs[i]] = game.win
	# 		else:
	# 			n_games[curr_players[i]][curr_champs[i]] += 1
	# 			n_wins[curr_players[i]][curr_champs[i]] += game.win
	# df_games = pd.DataFrame(n_games)
	# print(df_games)

	# df_wins = pd.DataFrame(n_wins)
	# print(df_wins)

	# df_pickrate = df_games.divide(df_games.sum(axis = 0), axis = 1)
	# print(df_pickrate)

	# df_winrate = df_wins/df_games
	# print(df_winrate)
	# for player in all_players:
	# 	top_picked = df_pickrate.loc[:,player].sort_values(ascending = False)
	# 	top_win = df_winrate.loc[:,player].sort_values(ascending = False)

	# 	print('top picks for ' + player + ': \n' + str(top_picked[0:3]))
	# 	print('\ntop winrate for ' + player + ': \n' + str(top_win[0:3]))


	




