# update_save_state.py
import base64

class Actor:
	
	def __init__(self, name, attack=0, defense=0, lvl=0, hp=0, exp=0, gold=0):
		self.name = name	# player.name
	
		# Stats	
		self.hp = hp	   #player.max_hp
		self.max_hp = hp   #
		self.attack = attack
		self.defense = defense
		self.level = lvl
		self.exp = exp
		self.gold = gold
		self.abilities = []

class Player(Actor):

	def __init__(self, name, lvl, attack, defense, current_HP, base_HP, current_SP, base_SP, current_EXP, next_EXP, gold, items):
		super().__init__(name, attack, defense, lvl, base_HP, current_EXP, gold)
		
		self.name = name
		self.lvl = lvl
		self.attack = attack
		self.defense = defense
		self.current_HP = current_HP
		self.base_HP = base_HP
		self.current_SP = current_SP
		self.base_SP = base_SP
		self.current_EXP = current_EXP
		self.next_EXP = next_EXP
		self.gold = gold
		self.items = items

class Rogue(Player):
	def __init__(self, name='Fief', lvl=3, attack=6, defense=7, current_HP=15, base_HP=15,
		current_SP=8, base_SP=8, current_EXP=0, next_EXP=4, gold=2, 
		items={'Shield': 0, 'Potions': 0, 'Apples': 1, 'Herbs:': 4, 'magic_item': 0,
				'Fire Scroll': 0, 'Thunder Scroll': 0, 'Ice Scroll': 0}):

		super().__init__(name, lvl, attack, defense, current_HP, base_HP, current_SP, base_SP, current_EXP, next_EXP, gold, items)	
		
		self.character_class = 'Rogue'
	
		# Attacks/Weaponry
		self.attack_type = 'stabs'
		self.magic_weapons = 'Vorpal Daggers'
		
		# Inventory
		self.gold = 2
		self.p_left = 4
		
		# DAG = DamageAbility('Dastardly Dagger!', 2, 'You execute whatever', 1.3)
		# POK = DamageAbility('Precious Poke', 8, 'You execute whatever', 1.9)
		# STE = StealPotion('Quick Quiet Movement', 13, 'steals a potion behind the enemie's back')
		
		# self.abilities = [DAG, POK, STE]

player = Rogue('Fief', 5, 10, 15, 8, 20, 13, 13, 100, 200, 50, {
	'Shield': 1,
	'Potions': 3,
	'Apples': 3,
	'Herbs': 4,
	'magic_item': 1,
	'Fire Scroll': 3,
	'Thunder Scroll': 2,
	'Ice Scroll': 3
	})

game_stats = {
	'magic_weapon_status': 0,
	'reginald': -1,
	'rat_name': None,
	'shopbro': -1,
	'p_left': 0,
	'fairies': 4,
	'inn_stays': -1,
	'orc_dead': False,
	'user': 'None',
	'town_tutorial': True,
	'level_tutorial': True,
	'librarian': 0,
	'floor_key': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
	'portals': [],
	}


if __name__ == '__main__':

	save_state = open('save_state.txt', 'w')  
			
	stats_to_save = [player.character_class, player.name, player.lvl, player.attack, player.defense, 
		player.current_HP, player.base_HP, player.current_SP, player.base_SP, player.current_EXP, player.next_EXP,
		player.gold, player.items, game_stats
	]

	line_to_save = ''
	for i in stats_to_save:
		line_to_save = line_to_save + str(i) + '\n'

	save_state.write(base64.b64encode(line_to_save.encode('UTF-8')).decode('UTF-8'))
	save_state.close()

	print('Game saved.')