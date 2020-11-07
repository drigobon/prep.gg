class LeagueGame:
	def __init__(self, data):
		self.patch = data['patch']
		self.win = data['win']
		self.side = data['side']
		self.opp = data['opp']
		self.bans = data['bans']
		self.vs_bans = data['vs_bans']
		self.picks = data['picks']
		self.vs_picks = data['vs_picks']
		self.players = data['players']



class LeaguePlayer:
	def __init__(self, n_games, n_wins, data):
		self.n_games = n_games
		self.n_wins = n_wins
		self.K = data['K']
		self.D = data['D']
		self.A = data['A']
		self.CS = data['CS']
		self.CSM = data['CSM']
		self.G = data['G']
		self.GM = data['GM']
		self.KPAR = data['KPAR']
		self.KS = data['KS']
		self.GS = data['GS']
		



class LeagueTeam:
	def __init__(self, players, data):
		self.players = players

		self.region = data['region']
		self.season = data['season']
		self.WL = data['WL']
		self.avg_gm_dur = data['avg_gm_dur']
		self.most_banned_by = data['most_banned_by']
		self.most_banned_vs = data['most_banned_vs']
		self.economy = data['economy']
		self.aggression =  data['aggression']
		self.objectives = data['objectives']
		self.vision = data['vision']
		
