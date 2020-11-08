import numpy as np
import pandas as pd

import json

from utils import *


if __name__ == "__main__":

	all_team_data = dict()

	teams = ['DAMWON_Gaming', 'DRX', 'FlyQuest', 'Fnatic', 'G2_Esports', 'Gen.G', 'JD_Gaming',
			 'LGD_Gaming', 'Machi_Esports', 'PSG_Talon', 'Rogue_(European_Team)', 'Suning',
			 'Team_Liquid', 'Team_SoloMid', 'Top_Esports', 'Unicorns_Of_Love.CIS']

	team_dict = {'Team_Liquid': '876', 'Team_SoloMid': '877', 'FlyQuest': '873',
				 'DAMWON_Gaming': '849', 'DRX': '853', 'Gen.G': '852',
				 'Top_Esports': '829', 'JD_Gaming': '836', 'Suning': '834', 'LGD_Gaming': '840',
				 'G2_Esports': '891', 'Fnatic': '890', 'Rogue_(European_Team)': '895',
				 'Machi_Esports': '976', 'PSG_Talon': '982', 'Unicorns_Of_Love.CIS': '1014'}


	abbrv_dict = {'DAMWON_Gaming': 'DWG', 'DRX': 'DRX', 'FlyQuest': 'FLY', 'Fnatic': 'FNC', 'G2_Esports': 'G2',
				  'Gen.G': 'GEN', 'JD_Gaming': 'JDG', 'LGD_Gaming': 'LGD', 'Machi_Esports': 'M17', 'PSG_Talon': 'PSG',
				  'Rogue_(European_Team)': 'RGE', 'Suning': 'SN', 'Team_Liquid': 'TL', 'Team_SoloMid': 'TSM',
				  'Top_Esports': 'TES', 'Unicorns_Of_Love.CIS': 'UOL'}


	for team in teams:
		print(team)

		team_data = scrape_team(team, team_dict, abbrv_dict)

		with open('data/'+ abbrv_dict[team] +'.json', 'w') as outfile:
			json.dump(team_data, outfile)


		# team_data = dict()

		# team_data['name'] = " ".join(team.split("_"))
		# team_data['abbrv'] = abbrv_dict[team]


		# # get teamwide data
		# url = construct_gol_url(team, team_dict)
		# data = extract_gol_data(url)

		# team_data['team_stats'] = data


		# # get leaguepedia data
		# url = construct_url_for_team(team)
		# table_rows = extract_table_rows_from_url(url)

		# all_players = dict()
		# all_games = list()
		# win_seq = list()

		# roles = ['top', 'jungle', 'mid', 'adc', 'sup']

		# blue_wins = 0
		# blue_games = 0
		# red_wins = 0
		# red_games = 0

		# for row in table_rows:
		# 	game = extract_game_from_row(row, False)

		# 	if game['side'] == 'Blue':
		# 		blue_games += 1
		# 		blue_wins += game['win']
		# 	else:
		# 		red_games += 1
		# 		red_wins += game['win']

		# 	win_seq.append(game['win'])
		# 	all_games.append(game)

		# 	for (i,player) in enumerate(game['players']):
		# 		if player.lower() not in set([key.lower() for key in all_players.keys()]):
		# 			all_players[player] = {'role': roles[i]}

		# team_data['team_stats']['blue_winrate'] = round(100*blue_wins/blue_games,1)
		# team_data['team_stats']['red_winrate'] = round(100*red_wins/red_games,1)
		# team_data['recent_game_results'] = win_seq

		
		# # get player-specific data
		# all_player_champs = dict()

		# for player in list(all_players.keys()):

		# 	url = construct_url_for_player(player)
		# 	rows = extract_player_data_from_url(url)

		# 	player_champs = dict()

		# 	n_games = 0

		# 	for row in rows: 
		# 		try:
		# 			data = extract_champ_from_row(row)

		# 			player_champs[data['champ']] = data

		# 			n_games += int(data['games'])
		# 		except:
		# 			pass

		# 	for key in player_champs.keys():
		# 		player_champs[key]['pickrate'] = round(100*player_champs[key]['games']/n_games, 1)


		# 	avg_kda = list()
		# 	avg_k = list()
		# 	avg_d = list()
		# 	avg_a = list()
		# 	avg_kp = list()
		# 	avg_ks = list()
		# 	avg_gs = list()

		# 	avg_kda_den = list()
		# 	avg_k_den = list()
		# 	avg_d_den = list()
		# 	avg_a_den = list()
		# 	avg_kp_den = list()
		# 	avg_ks_den = list()
		# 	avg_gs_den = list()

		# 	for key in player_champs.keys():
		# 		try:
		# 			avg_kda.append(player_champs[key]['kda']*player_champs[key]['pickrate'])
		# 			avg_kda_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'kda error')

		# 		try:
		# 			avg_k.append(player_champs[key]['kills']*player_champs[key]['pickrate'])
		# 			avg_k_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'k error')

		# 		try:
		# 			avg_d.append(player_champs[key]['deaths']*player_champs[key]['pickrate'])
		# 			avg_d_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'd error')

		# 		try:
		# 			avg_a.append(player_champs[key]['assists']*player_champs[key]['pickrate'])
		# 			avg_a_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'a error')

		# 		try:
		# 				avg_kp.append(player_champs[key]['kpar']*player_champs[key]['pickrate'])
		# 				avg_kp_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'kp error')

		# 		try:
		# 			avg_ks.append(player_champs[key]['killshare']*player_champs[key]['pickrate'])
		# 			avg_ks_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'ks error')

		# 		try:
		# 			avg_gs.append(player_champs[key]['goldshare']*player_champs[key]['pickrate'])
		# 			avg_gs_den.append(player_champs[key]['pickrate'])
		# 		except:
		# 			print(player, key, 'gs error')

		# 	all_players[player]['avg_kda'] = round(np.sum(avg_kda)/np.sum(avg_kda_den),1)
		# 	all_players[player]['avg_k'] = round(np.sum(avg_k)/np.sum(avg_k_den),1)
		# 	all_players[player]['avg_d'] = round(np.sum(avg_d)/np.sum(avg_d_den),1)
		# 	all_players[player]['avg_a'] = round(np.sum(avg_a)/np.sum(avg_a_den),1)
		# 	all_players[player]['avg_kp'] = round(np.sum(avg_kp)/np.sum(avg_kp_den),1)
		# 	all_players[player]['avg_ks'] = round(np.sum(avg_ks)/np.sum(avg_ks_den),1)
		# 	all_players[player]['avg_gs'] = round(np.sum(avg_gs)/np.sum(avg_gs_den),1)



		# 	all_player_champs[player.split('_')[0]] = player_champs



		# team_data['player_champ_stats'] = all_player_champs

		# all_players_clean = dict()
		# for player in all_players.keys():
		# 	all_players_clean[player.split("_")[0]] = all_players[player]

		# team_data['player_stats'] = all_players_clean


		# with open('data/'+ abbrv_dict[team] +'.json', 'w') as outfile:
		# 	json.dump(team_data, outfile)






	




