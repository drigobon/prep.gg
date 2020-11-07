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

	temp = data_tables[0].find_all('td',{'class': 'text-center'})

	keys = ['region', 'season', 'WL', 'avg_gm_dur']

	for i in range(len(keys)):
		if keys[i] != 'WL':
			data[keys[i]] = temp[i].get_text()
		else:
			data[keys[i]] = temp[i].get_text().split(' - ')

	print(data)

	print(len(temp))
	
	table_body = draft_table.find_all('tbody')[0]

	table_rows = draft_table.find_all('tr')[4:]

	return table_rows



if __name__ == "__main__":
	url = construct_gol_url('Team_Liquid')

	temp = extract_gol_data(url)

