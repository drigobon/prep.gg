from flask import Flask, render_template
import requests

abbrev_to_team_name = {
	"DWG": "DAMWON Gaming",
	"DRX": "DragonX",
	"GEN": "Gen.G",
	"TES": "Top Esports",
	"JDG": "JD Gaming",
	"LGD": "LGD Gaming",
	"SN": "Suning",
	"G2": "G2 Esports",
	"FNC": "Fnatic",
	"RGE": "Rogue", 
	"TSM": "Team SoloMid",
	"TL": "Team Liquid",
	"FLY": "FlyQuest",
	"M17": "Machi Esports",
	"UOL": "Unicorns of Love",
	"PSG": "PSG Talon"
}


application = Flask(__name__)

@application.route('/')
def home():
	return "Hello, world!"

@application.route('/<team_abbreviation>')
def team_page(team_abbreviation):
	r = requests.get('https://scoutgg123.s3.amazonaws.com/' + team_abbreviation + '.json')
	data = r.json()
	return render_template('index.html', data = data, team_abbrev=team_abbreviation, team=abbrev_to_team_name[team_abbreviation])


if __name__ == "__main__":
	application.run(debug=True)