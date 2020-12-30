# actor.py
from random import randint
from time import sleep

import globals as glbl
from globals import Bar, GameOver, dialogue
from graphics import Point, Rectangle, Text, color_rgb

import pygame
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

class Actor:
	# anything that's common to both enemy and player goes here
	
	def __init__(self, name, attack=0, defense=0, lvl=0, base_HP=0, current_EXP=0, gold=0):
		self.name = name
		self.attack = attack
		self.defense = defense
		self.lvl = lvl
		self.base_HP = base_HP
		self.current_HP = base_HP

		self.current_EXP = current_EXP
		self.gold = gold
		self.abilities = []

	def take_turn(self, other):
		if self.attack >= other.defense:
			# get a random damage amount
			damage = self.get_damage()
			dialogue(f'{self.name} did {damage} DMG.', right=True)
			other.current_HP -= damage
			if other.current_HP < 0:
				other.current_HP = 0
			dialogue(f"{other.name}'s HP dropped to {other.current_HP}.", right=True)

		# Otherwise, the attack missed.
		else:
			dialogue(f"{self.name}'s attack missed!", right=True)
	
	def get_damage(self):
		return randint(1, 3)


class Player(Actor):	
		
	def __init__(self, name, lvl, attack, defense, current_HP, base_HP, current_SP, base_SP, current_EXP, next_EXP, gold, items):
		super().__init__(name, attack, defense, lvl, base_HP, current_EXP, gold)
		
		self.current_HP = current_HP
		self.current_SP = current_SP
		self.base_SP = base_SP
		self.next_EXP = next_EXP
		self.items = items
		
		
	# battle mathod
	def battle(self, enemy):

		pygame.mixer.music.stop()

		# musicChoice = (randint(1,2)

		# if musicChoice == '1':
		# 	battle_music = pygame.mixer.music.load("Battle_Music.wav")
		# 	pygame.mixer.music.play(-1)
		# else:
		# 	battle_music2 = pygame.mixer.music.load("battle2.mp3")
		# 	pygame.mixer.music.play(-1)


		battle_music = pygame.mixer.music.load("Battle_Music.wav")
		
		pygame.mixer.music.play(-1)

		prior = len(glbl.gw.items)

		battle_background = Rectangle(Point(-2, -2), Point(1002, 502))
		battle_background.setFill(color_rgb(150, 150, 150))
		battle_background.draw(glbl.gw)

		e_name_box = Rectangle(Point(11, 11), Point(len(enemy.name) * 20 + 22, 50))
		e_name_box.setFill(color_rgb(50, 50, 50))
		e_name_box.setWidth(3)
		e_name_box.draw(glbl.gw)
		e_name = Text(Point(22, 16), enemy.name)
		e_name.setAnchor('nw')
		e_name.setStyle('bold')
		e_name.setSize(20)
		e_name.draw(glbl.gw)

		e_name.draw(glbl.gw)
		e_health = Bar(enemy.current_HP, enemy.base_HP, 'red', Point(11, 55), Point(331, 81))
		e_health.show()


		p_name_box = Rectangle(Point(978 - (len(self.name) * 20), 11), Point(989, 50))
		p_name_box.setFill(color_rgb(50, 50, 50))
		p_name_box.setWidth(3)
		p_name_box.draw(glbl.gw)
		p_name = Text(Point(978, 16), self.name)
		p_name.setAnchor('ne')
		p_name.setStyle('bold')
		p_name.setSize(20)
		p_name.draw(glbl.gw)

		p_health = Bar(self.current_HP, self.base_HP, 'red', Point(669, 55), Point(989, 81))
		p_health.show()
		p_exp = Bar(self.current_EXP, self.next_EXP, 'green', Point(719, 86), Point(989, 100), show_text=False)
		p_exp.show()


		while True:
			# Check to see if the player has died.
			if self.current_HP <= 0:
				raise GameOver('lost battle')
				
		
			#this calls the menu and takes the input to be called here.
			# returns a valid player selection
			x = self.battleInput()

			if x == 'Attack':
				self.attack_enemy(enemy)

			elif x in '012':
				self.abilities[int(x)].execute(self, enemy)
			
			elif x.count('Potion') > 0:
				self.use_potion()
			
			elif x == 'Run':
				self.run(enemy)


			# Since the player attacked the enemy, update their health bar.
			e_health.update(enemy.current_HP)
	
			# Check to see if the enemy died last turn.
			# If so, give out rewards, and maybe level up.
			if enemy.current_HP <= 0:
				pygame.mixer.music.stop()

				dialogue(f'{enemy.name} died!', speed=.01, right=True)
	
				if enemy.name == 'Orc':
					glbl.game_stats['orc_dead'] = True
					raise GameOver('orc dead')
					
				else:
					pygame.mixer.music.stop()
					town_music = pygame.mixer.music.load("Overworld_Music.mp3")
					pygame.mixer.music.play(-1)
					
					line = f'{self.name} gained {enemy.current_EXP} XP'
					if enemy.gold > 0:
						line += f'and {enemy.gold} gold'
					line += '.'
					dialogue(line, speed=.01, right=True)
					self.current_EXP += enemy.current_EXP
					self.gold += enemy.gold

					p_exp.update(self.current_EXP)
					while self.current_EXP >= self.next_EXP:
						self.level_up()
						p_exp.update(self.current_EXP, self.next_EXP)

				sleep(1)
				glbl.gw.clear(prior)
				return
			
			enemy.take_turn(self)

			p_health.update(self.current_HP)
	
	# prints the menu and gets user input
	def battleInput(self):
		
		while True:
		
			x = dialogue('What will you do?', ['Attack', f'Special ({self.current_SP}/{self.base_SP})', f'Potion ({self.items["Potions"]})', 'Run'], speed=.01, return_arg=True, right=True)

			# get which special ability 
			if x.count('Special') > 0:
				
				options = []
				
				for a in self.abilities:
					options.append(f'{a.name} ({a.cost}SP)')
				options.append('Cancel')

				while True:
					x = dialogue(f'Current SP:  ({self.current_SP}/{self.base_SP})\n', options, speed=.01, right=True)

					if x != 3 and self.current_SP < self.abilities[x].cost:
						dialogue("You don't have enough SP for that.", speed=.01, right=True)

					elif x == 3:
						break
					else:
						return str(x)

			elif x.count('Potion') > 0:
				if self.items["Potions"] == 0:
					dialogue("You don't have any potions to drink!", speed=.01, right=True)
				else:
					break
					
			
			else:
				break

		return x
		
	def attack_enemy(self, enemy):
		# The battle system is like DnD. There a roll to see if the attack hits, then another for the actual damage dealt.
		attack = randint(10, 20) + (self.attack/2)
		if attack >= enemy.defense:
			damage = round(randint(1,5) + (self.attack/2.5))
			enemy.current_HP -= damage
	
			dialogue(f'{self.name} {self.attack_type} the enemy for {damage} DMG.', speed=.01, right=True)
			if enemy.current_HP < 0:
				enemy.current_HP = 0
	
			# Tell the player how much damage the attack did.
			dialogue(f"{enemy.name}'s HP dropped to {enemy.current_HP}.", speed=.01, right=True)

		# And in case the attack missed:
		else:
			dialogue('Your attack missed!', speed=.01, right=True)

	def use_potion(self):
		self.items['Potions'] -= 1
		self.current_HP += round(randint(4,10)* 4.2)
	
		if self.current_HP > self.base_HP:
			self.current_HP = self.base_HP
	
		dialogue(f'HP restored to {self.current_HP}/{self.base_HP}.', speed=.01, right=True)
			
	def run(self, enemy):
		# The escape formula is based on what level the player is versus what level the monster is.
		# The if the player has a higher level than the opponent, they have a higher chance of escape..
		# Conversly, if the monster has a higher level, it'll be harder for the player to run.
		j = self.lvl - enemy.lvl
		if j == 0:
			j = 1
	
		if (j * 2) + randint(4,8) > 8:
			dialogue('Escape succeeded!', right=True)
	
		else:
			dialogue('Escape failed!', right=True)
				
	def level_up(self):

		# Raises the player's level by 1, while subracting how much is required for that level up.
		self.lvl += 1

		# Tell the player they've just leveled up.
		dialogue(f"{self.name} levels up!", right=True)
		
		# This is the formula for how much more experience the player will need to obtain the next level.
		# I fiddled with values in graph making software to come up with this one.
		self.next_EXP += round((6 * (self.lvl**.769))-7.182)

		points = randint(1, 5)
		dialogue(f'You gained {points} points to spend.', right=True)
		while points != 0:
			x = dialogue(f'Assign a point to which stat?\n({points} left)',
				[f'ATT ({self.attack})', f'HP ({self.base_HP})', f'SP ({self.base_SP})'], right=True)

			if x == 0:
				self.attack += 1
		
			elif x == 1:
				self.base_HP += 1
				self.current_HP = self.base_HP

			else:
				self.base_SP += 1
				self.current_SP = self.base_SP

			points -= 1
		
		x = randint(1, 9)
		if x > 6:
			if x == 9: self.defense += 2
			else: self.defense += 1
			dialogue(f"DEF also rose to: {self.defense}", right=True)
		else:
			dialogue(f"DEF remains:  {self.defense}", right=True)

		
		# And for good measure, tell the player how much more they'll need for their next level.
		dialogue(f"Next Lv. at {self.next_EXP} EXP.", right=True)


class Warrior(Player):
	def __init__(self, name='Grog', lvl=3, attack=5, defense=9, current_HP=17, base_HP=17,
		current_SP=10, base_SP=10, current_EXP=0, next_EXP=4, gold=2, 
		items={"Shield": 0, "Potions": 0, "Apples": 2, "Herbs": 2, "magic_item": 0,
				"Fire Scroll": 0, "Thunder Scroll": 0, "Ice Scroll": 0}):

		super().__init__(name, lvl, attack, defense, current_HP, base_HP, current_SP, base_SP, current_EXP, next_EXP, gold, items)	
		
		self.character_class = 'Warrior'
		
		# Attacks/Weaponry
		self.attack_type = 'slashes at'
		
		self.basic_attack = Ability("Basic Attack", 0, "slashes at enemy with Damascus Sword")
		
		SSH = DamageAbility("Super Sword Hit!", 4, "You execute whatever", 1.5)
		SDH = DamageAbility("Super DUPER Sword Hit!", 7, "You execute a harder hitting whatever",2)
		SOD = DamageAbility("Slash of Dragons!", 10, "You execute the strongest whatever", 3)

		self.abilities = [SSH, SDH, SOD]	


class Sorcerer(Player):
	def __init__(self, name='Magnus', lvl=3, attack=4, defense=10, current_HP=20, base_HP=20,
		current_SP=18, base_SP=18, current_EXP=0, next_EXP=4, gold=2, 
		items={"Shield": 0, "Potions": 0, "Apples": 1, "Herbs": 4, "magic_item": 0,
				"Fire Scroll": 0, "Thunder Scroll": 0, "Ice Scroll": 0}):

		super().__init__(name, lvl, attack, defense, current_HP, base_HP, current_SP, base_SP, current_EXP, next_EXP, gold, items)	
		
		self.character_class = 'Sorcerer'
		
		# Attacks/Weaponry
		self.attack_type = 'fires magic at'
		
		FFR = DamageAbility("Flaming Fire Rod!", 6, "You execute whatever", 1.7)
		FIR = DamageAbility("Freezing Ice Rod!", 15, "You execute whatever", 2.4)
		HEA = HealingAbility("Healthy Healing Magic!", 25, "You execute whatever")
		
		self.abilities = [FFR, FIR, HEA]


class Rogue(Player):
	def __init__(self, name='Fief', lvl=3, attack=6, defense=7, current_HP=15, base_HP=15,
		current_SP=8, base_SP=8, current_EXP=0, next_EXP=4, gold=2, 
		items={"Shield": 0, "Potions": 0, "Apples": 1, "Herbs": 4, "magic_item": 0,
				"Fire Scroll": 0, "Thunder Scroll": 0, "Ice Scroll": 0}):

		super().__init__(name, lvl, attack, defense, current_HP, base_HP, current_SP, base_SP, current_EXP, next_EXP, gold, items)	
		
		self.character_class = 'Rogue'
	
		# Attacks/Weaponry
		self.attack_type = 'stabs'
		
		# Inventory
		self.gold = 2
		self.p_left = 4
		
		DAG = DamageAbility("Dasturdly Dagger!", 2, "You execute whatever", 1.3)
		POK = DamageAbility("Precious Poke", 8, "You execute whatever", 1.9)
		STE = StealPotion("Quick Quiet Movement", 13, "You steal a potion behind the enemy's back!")
		
		self.abilities = [DAG, POK, STE]


class Ability:
	def __init__(self, name="", cost=0, desc="empty"):
		self.name = name
		self.cost = cost
		self.description = desc


class DamageAbility(Ability):
	def __init__(self, name, cost, desc, scalar):
		super().__init__(name,cost,desc)
		self.scalar = scalar
		
	def execute(self, player, enemy):
		damage = round(self.scalar * (randint(1,5) + (player.attack/2.5)))
		enemy.current_HP -= damage
		
		dialogue(f'{player.name} uses {self.name} on {enemy.name} for {damage} DMG.', speed=.01, right=True)
		player.current_SP -= self.cost
		if enemy.current_HP < 0:
			enemy.current_HP = 0

		dialogue(f"{enemy.name}'s HP dropped to {enemy.current_HP} ", speed=.01, right=True)
		
		
class HealingAbility(Ability):
	def __init__(self, name, cost, desc):
		super().__init__(name, cost, desc)

	def execute(self, player, enemy):
		player.current_HP = player.base_HP
		player.current_SP -= self.cost
		dialogue(self.description, speed=.1, right=True)
		

class StealPotion(Ability):
	def __init__(self, name, cost, desc):
		super().__init__(name,cost,desc)
		
	def execute(self, player, enemy):
		chance = randint(0, 1)
		player.current_SP -= self.cost
		if chance == 0:
			player.items['Potions'] += 1
			dialogue(self.description, speed=.1, right=True)
		else:
			dialogue("Failed to steal a potion.", speed=.01, right=True) 


if __name__ == '__main__':
	pass