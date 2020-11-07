import numpy as np
import pandas as pd

import json

from utils import *


if __name__ == "__main__":

	all_team_data = dict()

	teams = ['DAMWON_Gaming', 'DRX', 'FlyQuest', 'Fnatic', 'G2_Esports', 'Gen.G', 'JD_Gaming',
			 'LGD_Gaming', 'Machi_Esports', 'PSG_Talon', 'Rogue_(European_Team)', 'Suning',
			 'Team_Liquid', 'Team_SoloMid', 'Top_Esports', 'Unicorns_Of_Love.CIS']

	abbrv_dict = {'DAMWON_Gaming': 'DWG', 'DRX': 'DRX', 'FlyQuest': 'FLY', 'Fnatic': 'FNC', 'G2_Esports': 'G2', 'Gen.G': 'GEN', 'JD_Gaming': 'JDG',
			 'LGD_Gaming': 'LGD', 'Machi_Esports': 'M17', 'PSG_Talon': 'PSG', 'Rogue_(European_Team)': 'RGE', 'Suning': 'SN',
			 'Team_Liquid': 'TL', 'Team_SoloMid': 'TSM', 'Top_Esports': 'TES', 'Unicorns_Of_Love.CIS': 'UOL'}

	for team in teams:

#	team = 'Team_Liquid'
		print(team)

		team_data = dict()

		team_data['name'] = " ".join(team.split("_"))
		team_data['abbrv'] = abbrv_dict[team]


		# get leaguepedia data
		url = construct_url_for_team(team)
		table_rows = extract_table_rows_from_url(url)

		all_players = dict()
		all_games = list()
		win_seq = list()

		roles = ['top', 'jungle', 'mid', 'adc', 'sup']

		for row in table_rows:
			game = extract_game_from_row(row, False)

			win_seq.append(game.win)
			all_games.append(game)

			for (i,player) in enumerate(game.players):
				if player not in set(all_players.keys()):
					all_players[player] = {'role': roles[i]}


		#print(all_players)
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
				player_champs[key]['pickrate'] = str(int(player_champs[key]['games'])/n_games)




			avg_kda = list()
			avg_kp = list()
			avg_ks = list()
			avg_gs = list()

			avg_kda_den = list()
			avg_kp_den = list()
			avg_ks_den = list()
			avg_gs_den = list()

			for key in player_champs.keys():

				try:
					avg_kda.append(float(player_champs[key]['kda'])*float(player_champs[key]['pickrate']))
					avg_kda_den.append(float(player_champs[key]['pickrate']))
				except:
					print(player, key, 'kda error')

				try:
					avg_kp.append(float(player_champs[key]['kpar'].split('%')[0])*float(player_champs[key]['pickrate']))
					avg_kp_den.append(float(player_champs[key]['pickrate']))
				except:
					print(player, key, 'kp error')

				try:
					avg_ks.append(float(player_champs[key]['killshare'].split('%')[0])*float(player_champs[key]['pickrate']))
					avg_ks_den.append(float(player_champs[key]['pickrate']))
				except:
					print(player, key, 'ks error')

				try:
					avg_gs.append(float(player_champs[key]['goldshare'].split('%')[0])*float(player_champs[key]['pickrate']))
					avg_gs_den.append(float(player_champs[key]['pickrate']))
				except:
					print(player, key, 'gs error')


			all_players[player]['avg_kda'] = np.sum(avg_kda)/np.sum(avg_kda_den)
			all_players[player]['avg_kp'] = np.sum(avg_kp)/np.sum(avg_kp_den)
			all_players[player]['avg_ks'] = np.sum(avg_ks)/np.sum(avg_ks_den)
			all_players[player]['avg_gs'] = np.sum(avg_gs)/np.sum(avg_gs_den)
			

			all_player_champs[player] = player_champs


	#	print(all_player_champs)

		team_data['player_champ_stats'] = all_player_champs

		team_data['player_stats'] = all_players


		# get teamwide data
		url = construct_gol_url(team)
		data = extract_gol_data(url)

		#print(data)

		team_data['team_stats'] = data

		with open('data/'+ abbrv_dict[team] +'.json', 'w') as outfile:
			json.dump(team_data, outfile)



	# end loop

#	with open('data/all_teams.json', 'w') as outfile:
#			json.dump(all_team_data, outfile)


















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


	




