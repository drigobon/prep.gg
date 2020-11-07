import numpy as np
import pandas as pd

from utils import *
import models


def construct_gol_url(team):

	team_dict = {'Team_Liquid': '876', 'Team_SoloMid': '877'}

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
	for item in data_tables[2].find_all('td', {'style': 'text-aligm:center'}):
		most_banned_vs[item.find_all('img')[0].get('alt')] = item.get_text()
	data['most_banned_vs'] = most_banned_vs

	# economy stats
	temp = data_tables[3].find_all('tr')

	economy = dict()
	keys = [None, 'GPM', 'GDPM', 'GD15', 'CSM', 'CSD15', 'TWD15', 'TRatio','FirstTower']
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
	keys = [None, 'DPM', 'FirstBlood', 'KPG', 'DPG', 'KD', 'APK']
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
	keys = [None, 'DragPG', 'Drag15', 'HeraldPG', 'BaronPG']
	for i in range(len(keys)):
		if keys[i] is not None:	
			objectives[keys[i]] = temp[i].find_all('td')[1].get_text()
	data['objectives'] = objectives

	# vision stats
	temp = data_tables[6].find_all('tr')

	vision = dict()
	keys = [None, 'WPM', 'VWPM', 'WCPM', 'PercWC']
	for i in range(len(keys)):
		if keys[i] is not None:
			if keys[i] =='PercWC':
				vision[keys[i]] = temp[i].find_all('td')[1].find_all('span')[1].get_text()
			else:
				vision[keys[i]] = temp[i].find_all('td')[1].get_text()
	data['vision'] = vision

	return data



if __name__ == "__main__":
	url = construct_gol_url('Team_Liquid')

	data = extract_gol_data(url)

