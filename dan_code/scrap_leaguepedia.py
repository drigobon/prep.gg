from utils import *
import models

if __name__ == "__main__":
	# scrap every row
	url = construct_url_for_team("Team_SoloMid")

	table_rows = extract_table_rows_from_url(url)

	for row in table_rows:
		extract_game_from_row(row, True)


