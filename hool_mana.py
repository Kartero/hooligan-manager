# -*- coding: utf-8 -*-
#! python3

import pygame
import random
from collections import OrderedDict

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

# #####################################################################
class Player(object):
	
	def __init__(self):
		self.name = ""
		self.age = 0
		self.condition = 100
		self.dead = False
		self.description = ""
		self.properties = {
						"attack": 0,
						"defence": 0,
						"goalkeeping": 0,
						"aggression": 0,
						"power": 0,
						"speed": 0
						}
		self.stats = {
					"goals": 0,
					"kills": 0,
					"wons": 0,
					"defeats": 0,
					"draws": 0
					}
					
	def set_name(self):
		first_names = ["Richard", "Oystein", "Jack", "Leonard", "Tony",
			"Bill", "Pavel", "Donald", "John", "Peter", "Danny", "Igor",
			"Jorma", "Hector", "Ian", "Max", "Vladimir"]
		last_names = ["Wright", "Jones", "McDonald", "Keane", "Pettersson",
			"Trump", "Steel", "Mackey", "Kinney", "Fulton", "Hernandez",
			"Rodriguez", "Putin", "Kilmister"]
		random.shuffle(first_names)
		random.shuffle(last_names)
		
		first_name = random.choice(first_names)
		last_name = random.choice(last_names)
		self.name = first_name + " " + last_name
		
	def set_age(self):
		age = random.randint(16,42)
		self.age = age
		
	def set_properties(self):
		for key in self.properties:
			value = random.randint(1,20)
			self.properties[key] = value
		
	def set_player_data(self):
		self.set_name()
		self.set_age()
		self.set_properties()
		
	def draw_player_data(self):
		font = pygame.font.SysFont("Helvetica", 25, True, False)
		data = self.player.data()
		text = font.render(data, True, white)
		return text
		
	def order_property_dict(self):
		t = OrderedDict()
		t["attack"] = self.properties["attack"]
		t["defence"] = self.properties["defence"]
		t["goalkeeping"] = self.properties["goalkeeping"]
		t["aggression"] = self.properties["aggression"]
		t["power"] = self.properties["power"]
		t["speed"] = self.properties["speed"]
		
		return t
		
	def draw_condition_bar(self, screen, x, y):
		if self.condition >= 75:
			pygame.draw.rect(screen, green, [x, y, 2 * self.condition, 20])
		elif self.condition >= 40:
			pygame.draw.rect(screen, yellow, [x, y, 2 * self.condition, 20])
		else:
			pygame.draw.rect(screen, red, [x, y, 2 * self.condition, 20])
		
	def player_data(self):
		data = ""
		data += self.name
		if len(self.name) < 20:
			for i in range(20 - len(self.name)):
				data += " "
		data += str(self.age) + "      "
		
		temp_property = self.order_property_dict()
		for key in temp_property:
			data += str(temp_property[key])
			if temp_property[key] < 10:
				data += "   "
			else:
				data += "  "
			
		return data

# #####################################################################		
class Team(object):

	def __init__(self, name="Team"):
		self.name = name
		self.players = []
		self.team_color = red
		
	def set_team_color(self):
		color  = []
		for i in range(3):
			rgb = random.randint(40,255)
			color.append(rgb)
			
		self.team_color = color
		
	def set_players(self):
		for i in range(6):
			player = Player()
			self.players.append(player)
	
	def set_players_data(self):
		for i in self.players:
			i.set_player_data()
			
	def show_attributes(self):
		text = ""
		text += self.name
		if len(self.name) < 20:
			for i in range(20 - len(self.name)):
				text += " "
		text += "age     att def gk  agr pow spe      condition"
		return text
			
	def draw_team_players_data(self, screen, y):
		font = pygame.font.SysFont("Lucida Console", 20, False, False)
		text = font.render(self.show_attributes(), True, self.team_color)
		screen.blit(text, [10, y - 30])
		
		x = 10
		for i in self.players:
			data = i.player_data()
			text = font.render(data, True, self.team_color)
			screen.blit(text, [x,y])
			i.draw_condition_bar(screen, 700, y)
			y += 25

# #####################################################################
class Match(object):
	
	def __init__(self, home_team, away_team):
		self.home_team = home_team
		self.away_team = away_team
		self.home_score = 0
		self.away_score = 0
		self.fights = 0
		self.match_clock = 0
		
		self.slow_time = 0
		self.highlight_data = ""
		self.bg_color = black
		
		self.highlight_timer = 0
		self.hl_event = False
		
		self.events = []
	
	
	# # # DRAW MATCH # # #
	
	def init_match(self, screen):
		self.home_team.draw_team_players_data(screen, 40)
		self.away_team.draw_team_players_data(screen, 640)
		self.draw_team_information(screen)
		self.draw_highlights(screen, self.highlight_data, self.bg_color)
		
		for i in self.events:
			self.draw_events(screen, i[0], i[1], i[2], i[3])
				
	def draw_team_information(self, screen):
		font = pygame.font.SysFont("Lucida Console", 40, True, False)
		data = "GOALS: " + str(self.home_score)
		text = font.render(data, True, self.home_team.team_color)
		screen.blit(text, [10, 200])
		
		data = "Clock: " + str(self.match_clock) + " min"
		text = font.render(data, True, white)
		screen.blit(text, [10, 330])
		
		data = "Fights: " + str(self.fights)
		text = font.render(data, True, white)
		screen.blit(text, [10, 400])
		
		data = "GOALS: " + str(self.away_score)
		text = font.render(data, True, self.away_team.team_color)
		screen.blit(text, [10, 550])

	def draw_highlights(self, screen, data, bg_color):
		pygame.draw.rect(screen, bg_color, [420, 230, 500, 70])		
		font = pygame.font.SysFont("Helvetica", 30, False, False)
		text = font.render(data, True, white)
		screen.blit(text, [440, 250])
		
	def draw_events(self, screen, data, color, event, y):
		
		if event == "goal":
			font = pygame.font.SysFont("Arial", 15, True, False)
		else:
			font = pygame.font.SysFont("Sans Serif", 15, True, True)
			
		text = font.render(data, True, color)
		screen.blit(text, [500, 300 + y])
		
	# # # DRAW MATCH ENDS # # #
		
	def event_data(self, event, data, color):
		events = self.home_score + self.away_score + self.fights
		y = events * 20
		
		text = data + "    " + str(self.match_clock) + '"'
		temp_data = [text, color, event, y]
		self.events.append(temp_data)
		
	def goal_event(self):
		home_attack_stats = 0
		away_attack_stats = 0
		home_defence_stats = 0
		away_defence_stats = 0
		
		max_gk = 0
		for i in self.home_team.players:
			home_attack_stats += i.properties["attack"]
			home_defence_stats += i.properties["defence"]
			if i.properties["goalkeeping"] > max_gk:
				max_gk = i.properties["goalkeeping"]
				
		home_defence_stats += max_gk
		
		max_gk = 0
		for i in self.away_team.players:
			away_attack_stats += i.properties["attack"]
			away_defence_stats += i.properties["defence"]
			if i.properties["goalkeeping"] > max_gk:
				max_gk = i.properties["goalkeeping"]
				
		away_defence_stats += max_gk
		
		# Now the stats are initialized... Event itself can be calculated
		home_adv = home_attack_stats - away_defence_stats
		away_adv = away_attack_stats - home_defence_stats
		if home_adv >= 0 and away_adv < 0:
			home_prob = 0.66
		elif home_adv < 0 and away_adv >= 0:
			home_prob = 0.34
		else:
			home_prob = 0.50
			
		ran = random.random()
		if ran <= home_prob:
			scorer = self.goal_scorer(self.home_team)
			self.home_score += 1
			return (scorer + " scores!!",
					self.home_team.team_color)
		else:
			scorer = self.goal_scorer(self.away_team)
			self.away_score += 1
			return (scorer + " scores!!",
					self.away_team.team_color)

	def goal_scorer(self, team):
		probs = []
		pl_prob = 0
		for i in team.players:
			pl_prob += i.properties["attack"]
			pl_prob += int(i.properties["speed"] * 0.5)
			probs.append(pl_prob)
			pl_prob = 0
			
		total_probality = 0
		for i in probs:
			total_probality += i
			
		ran = random.randint(0,total_probality)
		
		player = 0
		count = 0
		for i in probs:
			count += i
			if (count >= ran):
				break
			player += 1
			
		return team.players[player].name
		
	def highlight_event(self):	
		if self.highlight_timer > 50:
			self.highlight_timer = 0
			self.hl_event = False
		elif self.hl_event == True:
			self.highlight_timer += 1
				
		if self.hl_event == False:
			ran = random.randint(0,4)
			# 0 = goal event
			# 1 = fight event
			# 2 (- 4) = no event
			self.hl_event = True
			if ran == 0:
				text, color = self.goal_event()
				self.event_data("goal", text, color)
			else:
				text = ""
				color = black

		else:
			text = self.highlight_data
			color = self.bg_color
		 
		self.highlight_data = text
		self.bg_color = color
		
	def run_clock(self):
		if self.slow_time > 15:
			self.match_clock += 1
			self.slow_time = 0
			self.player_condition_time()
		else:
			self.slow_time += 1
			
	def player_condition_time(self):
		all_players = self.home_team.players + self.away_team.players
		for i in all_players:
			ran = random.randint(0,2)
			if ran == 0 and i.condition > 0:
				i.condition -= 1
				
	
	def run_match(self):
		# Runs all match logic
		self.run_clock()
		self.highlight_event()
		
# #####################################################################
class League(object):
	
	def __init__(self):
		self.name = "Sunday League"
		self.teams = []
					
	def create_league(self):
		# Creates a league with six teams and initializes all players
		# This should be done ONLY once when instance of League has created
		
		team_names = ["Pub Warriors", "Underbridge Titans", "Poor w*nkers",
					"Junkyard Cowboys", "Germany", "Moscow Bums"]
		for i in team_names:
			team = Team(i)
			team.set_team_color()
			team.set_players()
			team.set_players_data()
			self.teams.append(team)
		
	
# #####################################################################
class Program(object):
	
	def __init__(self):
		pass

		
# #####################################################################
def main():
	# # # # #
	pygame.init()
	size = [1000, 800]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Hooligan Football Manager version 0.1")
	# # # # #
	
	league = League()
	league.create_league()
	match = Match(league.teams[3], league.teams[4])
	
	# # # # #
	done = False
	clock = pygame.time.Clock()
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		
		if match.match_clock < 90:
			match.run_match()
		
		# # # # #
		screen.fill(black)
		# # # # #
		
		# league.teams[5].draw_team_players_data(screen)
		match.init_match(screen)
		
		# # # # #
		clock.tick(60)
		pygame.display.flip()
		
	pygame.quit()
	
if __name__ == "__main__":
	main()