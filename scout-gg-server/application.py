from flask import Flask, render_template, redirect, url_for
import requests

abbrev_to_team_name = {
	"TSM": "Team SoloMid", #LCS
	"TL": "Team Liquid",
	"FLY": "FlyQuest",
	"C9": "Cloud9",
	"GG": "Golden Guardians",
	"EG": "Evil Geniuses",
	"IMT": "Immortals",
	"CLG": "Couter Logic Gaming",
	"DIG": "Dignitas",
	"100T": "100 Thieves", #CK
	"DWG": "DAMWON Gaming",
	"DRX": "DragonX",
	"GEN": "Gen.G",
	"T1": "T1",
	"SB": "Sandbox Gaming",
	"AF": "Afreeca Freecs",
	"KT": "KT Rolster",
	"HLE": "Hanwha Life Esports",
	"DYN": "Team Dynamics", #LPL
	"TES": "Top Esports",
	"JDG": "JD Gaming",
	"LGD": "LGD Gaming",
	"BLG": "Bilibili Gaming",
	"SN": "Suning",
	"FPX": "FunPlus Phoenix",
	"ES": "eStar Gaming",
	"RNG": "Royal Never Give Up",
	"DMO": "Dominus Esports",
	"EDG": "Edward Gaming",
	"RW": "Rogue Warriors",
	"IG": "Invictus Gaming",
	"LNG": "LNG Esports",
	"OMG": "Oh My God",
	"VG": "Vici Gaming",
	"V5": "Victory Five",
	"WE": "Team WE", #LEC
	"G2": "G2 Esports",
	"FNC": "Fnatic",
	"RGE": "Rogue",
	"S04": "FC Schalke 04",
	"XL": "Excel Esports",
	"MAD": "MAD Lions",
	"MSF": "Misfits Gaming",
	"OG": "Origen / Astralis",
	"SK": "SK Gaming",
	"VIT": "Team Vitality", #Other
	"M17": "Machi Esports",
	"UOL": "Unicorns of Love",
	"PSG": "PSG Talon"
}

LCS_abbrev = ["TL", "TSM", "C9", "FLY", "EG", "GG", "IMT", "CLG", "DIG", "100T"]
LEC_abbrev = ["G2", "FNC", "RGE", "MAD", "XL", "MSF", "OG", "VIT", "S04", "SK"]
LCK_abbrev = ["T1", "DWG", "SB", "AF", "KT", "DRX", "HLE", "DYN", "GEN"]
LPL_abbrev = ["BLG", "DMO", "EDG", "FPX", "ES", "IG", "JDG", "LGD", "LNG", "OMG", "RW", "RNG", "SN", "WE", "TES", "VG", "V5"]



application = Flask(__name__)

@application.route('/')
def home():
	return render_template('home.html', lcs=LCS_abbrev, lec=LEC_abbrev, lck=LCK_abbrev, lpl=LPL_abbrev)

@application.route('/<team_abbreviation>')
def team_page(team_abbreviation):
	try:
		r = requests.get('https://scoutgg123.s3.amazonaws.com/' + team_abbreviation + '.json')
		data = r.json()
		team_name = abbrev_to_team_name[team_abbreviation] if team_abbreviation in abbrev_to_team_name else team_abbreviation
		return render_template('index.html', data = data, team_abbrev=team_abbreviation, team=team_name)
	except:
		return redirect(url_for('error_msg'))

@application.route('/error')
def error_msg():
	return render_template('error.html')


if __name__ == "__main__":
	application.run(debug=True)