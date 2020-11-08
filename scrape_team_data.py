import numpy as np
import pandas as pd

import json

from utils import *


if __name__ == "__main__":

	all_team_data = dict()

	# from lol.gamepedia urls
	teams = ['DAMWON_Gaming', 'DRX', 'FlyQuest', 'Fnatic', 'G2_Esports', 'Gen.G', 'JD_Gaming',
			 'LGD_Gaming', 'Machi_Esports', 'PSG_Talon', 'Rogue_(European_Team)', 'Suning',
			 'Team_Liquid', 'Team_SoloMid', 'Top_Esports', 'Unicorns_Of_Love.CIS']

	# from gol.gg team ids
	team_dict = {'Team_Liquid': '876', 'Team_SoloMid': '877', 'FlyQuest': '873',
				 'DAMWON_Gaming': '849', 'DRX': '853', 'Gen.G': '852',
				 'Top_Esports': '829', 'JD_Gaming': '836', 'Suning': '834', 'LGD_Gaming': '840',
				 'G2_Esports': '891', 'Fnatic': '890', 'Rogue_(European_Team)': '895',
				 'Machi_Esports': '976', 'PSG_Talon': '982', 'Unicorns_Of_Love.CIS': '1014'}

	# for ease of presentation
	abbrv_dict = {'DAMWON_Gaming': 'DWG', 'DRX': 'DRX', 'FlyQuest': 'FLY', 'Fnatic': 'FNC', 'G2_Esports': 'G2',
				  'Gen.G': 'GEN', 'JD_Gaming': 'JDG', 'LGD_Gaming': 'LGD', 'Machi_Esports': 'M17', 'PSG_Talon': 'PSG',
				  'Rogue_(European_Team)': 'RGE', 'Suning': 'SN', 'Team_Liquid': 'TL', 'Team_SoloMid': 'TSM',
				  'Top_Esports': 'TES', 'Unicorns_Of_Love.CIS': 'UOL'}


	for team in teams:
		print(team)

		team_data = scrape_team(team, team_dict, abbrv_dict)

		with open('data/'+ abbrv_dict[team] +'.json', 'w') as outfile:
			json.dump(team_data, outfile)






	




