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