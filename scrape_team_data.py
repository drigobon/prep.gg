import numpy as np
import pandas as pd

import json

from utils import *


if __name__ == "__main__":

	all_team_data = dict()

	# from lol.gamepedia urls
	teams = ['T1', 'DAMWON_Gaming', 'SANDBOX_Gaming', 'Afreeca_Freecs', 'Gen.G', 'DRX', 'KT_Rolster', 'Hanwha_Life_Esports', 'Team_Dynamics', 'SeolHaeOne_Prince', 
			 'Excel_Esports', 'FC_Schalke_04_Esports', 'Fnatic', 'G2_Esports', 'MAD_Lions', 'Misfits_Gaming', 'Origen', 'Rogue_(European_Team)', 'SK_Gaming', 'Team_Vitality', 
			 'EStar_(Chinese_Team)', 'FunPlus_Phoenix', 'Royal_Never_Give_Up', 'Top_Esports', 'Bilibili_Gaming', 'EDward_Gaming', 'LNG_Esports', 'Invictus_Gaming', 'Suning', 
			 			'Team_WE', 'JD_Gaming', 'Dominus_Esports', 'Victory_Five', 'Rogue_Warriors', 'LGD_Gaming', 'Vici_Gaming', 'Oh_My_God', 
			 'Machi_Esports', 'PSG_Talon', 'Unicorns_Of_Love.CIS',
			 '100_Thieves', 'Counter_Logic_Gaming', 'Cloud9', 'Dignitas', 'Evil_Geniuses.NA', 'FlyQuest', 'Golden_Guardians', 'Immortals', 'Team_Liquid', 'Team_SoloMid'
			 ]

	# from gol.gg team ids
	team_dict = {'T1': '847', 'DAMWON_Gaming': '849', 'SANDBOX_Gaming': '850', 'Afreeca_Freecs': '851', 'Gen.G': '852', 'DRX': '853', 'KT_Rolster': '854',
						 'Hanwha_Life_Esports': '855', 'Team_Dynamics': '857', 'SeolHaeOne_Prince': '858',
				 'Excel_Esports': '888', 'FC_Schalke_04_Esports': '889', 'Fnatic': '890', 'G2_Esports': '891', 'MAD_Lions': '892', 'Misfits_Gaming': '893',
				 		 'Origen': '894', 'Rogue_(European_Team)': '895', 'SK_Gaming': '896', 'Team_Vitality': '897',
				 'EStar_(Chinese_Team)': '867', 'FunPlus_Phoenix': '827', 'Royal_Never_Give_Up': '828', 'Top_Esports': '829', 'Bilibili_Gaming': '830',
				 		 'EDward_Gaming': '831', 'LNG_Esports': '832', 'Invictus_Gaming': '833', 'Suning': '834', 'Team_WE': '835', 'JD_Gaming': '836',
				 		 'Dominus_Esports': '837', 'Victory_Five': '838', 'Rogue_Warriors': '839', 'LGD_Gaming': '840', 'Vici_Gaming': '841', 'Oh_My_God': '842',
				 'Machi_Esports': '976', 'PSG_Talon': '982', 'Unicorns_Of_Love.CIS': '1014',
				 '100_Thieves': '868', 'Counter_Logic_Gaming': '869', 'Cloud9': '870', 'Dignitas': '871', 'Evil_Geniuses.NA': '872', 'FlyQuest': '873',
				 		 'Golden_Guardians': '874', 'Immortals': '875', 'Team_Liquid': '876', 'Team_SoloMid': '877'
				 }

	# for ease of presentation
	abbrv_dict = {'T1': 'T1', 'DAMWON_Gaming': 'DWG', 'SANDBOX_Gaming': 'SB', 'Afreeca_Freecs': 'AF', 'Gen.G': 'GEN', 'DRX': 'DRX', 'KT_Rolster': 'KT',
						 'Hanwha_Life_Esports': 'HLE', 'Team_Dynamics': 'DYN', 'SeolHaeOne_Prince': 'SP',
				  'Excel_Esports': 'XL', 'FC_Schalke_04_Esports': 'S04', 'Fnatic': 'FNC', 'G2_Esports': 'G2', 'MAD_Lions': 'MAD', 'Misfits_Gaming': 'MSF',
				  		 'Origen': 'OG', 'Rogue_(European_Team)': 'RGE', 'SK_Gaming': 'SK', 'Team_Vitality': 'VIT',
				  'EStar_(Chinese_Team)': 'ES', 'FunPlus_Phoenix': 'FPX', 'Royal_Never_Give_Up': 'RNG', 'Top_Esports': 'TES', 'Bilibili_Gaming': 'BLG',
				  		 'EDward_Gaming': 'EDG', 'LNG_Esports': 'LNG', 'Invictus_Gaming': 'IG',  'Suning': 'SN', 'Team_WE': 'WE', 'JD_Gaming': 'JDG', 
				  		 'Dominus_Esports': 'DMO', 'Victory_Five': 'V5', 'Rogue_Warriors': 'RW', 'LGD_Gaming': 'LGD', 'Vici_Gaming': 'VG', 'Oh_My_God': 'OMG', 
				  'Machi_Esports': 'M17', 'PSG_Talon': 'PSG', 'Unicorns_Of_Love.CIS': 'UOL', 
				  '100_Thieves': '100T', 'Counter_Logic_Gaming': 'CLG', 'Cloud9': 'C9', 'Dignitas': 'DIG', 'Evil_Geniuses.NA': 'EG', 'FlyQuest': 'FLY',
				  		 'Golden_Guardians': 'GG', 'Immortals': 'IMT', 'Team_Liquid': 'TL', 'Team_SoloMid': 'TSM',
				  }


	for team in teams:
		print(team)

		team_data = scrape_team(team, team_dict, abbrv_dict)

		with open('data/'+ abbrv_dict[team] +'.json', 'w') as outfile:
			json.dump(team_data, outfile)






	




