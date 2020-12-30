# enemy.py
from random import randint, uniform

from actor import Actor
from globals import dialogue

# Enemy Group 1 is going to go here
class Goblin(Actor):
	def __init__(self, captain=False):
		lvl = randint(1,7)
		if captain: lvl += 2
		hp = ((lvl+1) // 2) + 4
		super().__init__('Goblin', 10, lvl, hp, randint(2,8), randint(1,2))
		self.appearance = 'A goblin appeared!'

class Rat(Actor):
	def __init__(self, captain=False):
		lvl = randint(3,7)
		if captain: lvl += 2
		hp = ((lvl+1) // 2) + 8
		super().__init__('Rat', 5, lvl, hp, randint(6,11), randint(1,2))
		self.appearance = 'Oh shoot, a rat!'

class Wolf(Actor):
	def __init__(self, captain=False):
		lvl = randint(3,5)
		if captain: lvl += 2
		hp = ((lvl + 1) / 2) + 9
		super().__init__('Slime', 16, lvl, hp, randint(6,11), randint(0,3))
		self.appearance = 'A wolf howls!'

class Reginald(Actor):
	def __init__(self, captain=False):
		lvl = 9
		hp = 30
		super().__init__('Reginald', 5, lvl, hp, randint(10,15), randint(7,10))


# Enemy Group 2 is going to go here
class Slime(Actor):
	def __init__(self, captain=False):
		lvl = randint(8,12)
		if captain: lvl += 2
		hp = ((lvl - 8) * 4) + 15
		super().__init__('Wolf', 20, lvl, hp, randint(12,18), randint(1,4))
		self.appearance = 'A slime squelches up!'

class Spider(Actor):
	def __init__(self, captain=False):
		lvl = randint(8,12)
		if captain: lvl += 2
		hp = ((lvl - 8) * 4) + 15
		super().__init__('Large Spider', 20, lvl, hp, randint(12,18), randint(1,4))
		self.appearance = "Webs are everywhere. It's a giant spider!"

class Snake(Actor):
	def __init__(self, captain=False):
		lvl = randint(8,12)
		if captain: lvl += 2
		hp = ((lvl - 8) * 4) + 15
		super().__init__('Snake', 22, lvl, hp, randint(12,18), randint(1,4))
		self.appearance = 'Sneaking up behind you, a snake appears!'


# Enemy group 3 is going to go below here
class Bear(Actor):
	def __init__(self, captain=False):
		lvl = randint(13,17)
		if captain: lvl += 2
		hp = ((lvl - 13) * 2) + 36
		super().__init__('Bear', 20, lvl, hp, randint(26,36), randint(1,4))
		self.appearance = 'An enraged bear crashes throught the trees!'

class Goblin_Warrior(Actor):
	def __init__(self, captain=False):
		lvl = randint(13,17)
		if captain: lvl += 2
		hp = ((lvl - 13) * 2) + 30
		super().__init__('Goblin Warrior', 22, lvl, hp, randint(26,36), randint(4,7))
		self.appearance = 'With armor and sword in hand, a gobin attacks!'

class Goblin_Shaman(Actor):
	def __init__(self, captain=False):
		lvl = randint(13,17)
		if captain: lvl += 2
		hp = ((lvl - 13) * 2) + 29
		super().__init__('Goblin Shaman', 23, lvl, hp, randint(26,36), randint(5,9))
		self.appearance = 'A goblin shaman fires magic at you!'

class Goblin_Rider(Actor):
	def __init__(self, captain=False):
		lvl = randint(13,17)
		if captain: lvl += 2
		hp = ((lvl - 13) * 2) + 33
		super().__init__('Goblin Rider', 24, lvl, hp, randint(26,36), randint(2,6))
		self.appearance = 'Riding a wolf, a goblin fires his bow!'


# Orc Boss
class Orc(Actor):
	def __init__(self):
		super().__init__('Orc', 29, 18, 84, randint(6,11), randint(1,2))
		self.superattack = 0
		self.should_be_dead = False
		self.heavy_attack = False

	def take_turn(self, player):
		if self.heavy_attack == True:
			self.heavy_attack = False
			damage = round(player.max_hp/uniform(2, 2.5))
			f = player.current_HP
			player.current_HP -= damage
			if player.current_HP < 0:
				damage = f
				player.current_HP = 0

				# A short line that triggers 1 time only.
				# If the player has taken the super attack and the damage is more than a third of their health, AND they would have died from it,...
				# the player is given a bit of amnesty with one HP remaining to drink a potion.
				if self.should_be_dead == False and damage>int(f/3):
					self.should_be_dead = True
					damage -= 1
					player.hp = 1


			dialogue(f'The orc takes a big swing, dealing `{damage} DMG.', color=['white', 'red'], right=True)
			dialogue(f"{player.name}'s HP dropped to {player.hp}.", color=['white', 'red'], right=True)


		orc_move = randint(1,4)

		# If the orc's health is below 28 and it rolled a 3, the orc will heal itself.
		if orc_move == 3 and self.hp < 28:
			heal = round(randint(4,7)* 4.2)
			self.hp += heal
			dialogue(f"The orc grabs and eats a nearby hunk of meat, restoring {heal} health.", right=True)

		# The orc has a 2 turn heavy attack that deals massive damage.
		# This is where the first turn would be triggered.
		if orc_move == 4:
			self.heavy_attack = True
			print("The orc readies his club.", right=True)

		else:
			normal_attack = True
