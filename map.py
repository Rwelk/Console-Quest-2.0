# map.py

from math import atan2, pi
from PIL import Image as PIL_Image
from random import choice, randint, seed
from time import sleep

from enemy import *
import globals as glbl
from globals import dialogue, pause_menu

from graphics import Point, Rectangle, Text, Image, color_rgb
from level_creation_tool import fetch_level
from random_encounters import rat_w_hat, shopbro

from actor import Rogue

import pygame
from pygame import mixer

pygame.init()


class Player_Icon:
	def __init__(self, level, overworld_objects, level_x, level_y, facing):
		self.level = level
		self.overworld_objects = overworld_objects
		self.level_x = level_x
		self.level_y = level_y
		self.map_x = level_x - 1
		self.map_y = level_y - 1

		self.idx = 0
		self.facing = facing
		cc = glbl.player.character_class
		self.level_up = [glbl.CHARACTERS / f"{cc}_up_0.png", glbl.CHARACTERS / f"{cc}_up_1.png", glbl.CHARACTERS / f"{cc}_up_2.png", glbl.CHARACTERS / f"{cc}_up_3.png"]
		self.level_down = [glbl.CHARACTERS / f"{cc}_down_0.png", glbl.CHARACTERS / f"{cc}_down_1.png", glbl.CHARACTERS / f"{cc}_down_2.png", glbl.CHARACTERS / f"{cc}_down_3.png"]
		self.level_left = [glbl.CHARACTERS / f"{cc}_left_0.png", glbl.CHARACTERS / f"{cc}_left_1.png", glbl.CHARACTERS / f"{cc}_left_2.png", glbl.CHARACTERS / f"{cc}_left_3.png"]
		self.level_right = [glbl.CHARACTERS / f"{cc}_right_0.png", glbl.CHARACTERS / f"{cc}_right_1.png", glbl.CHARACTERS / f"{cc}_right_2.png", glbl.CHARACTERS / f"{cc}_right_3.png"]
		
		if facing == "up": self.level_sprite = Image(Point(250, 250), self.level_up[0])
		elif facing == "down": self.level_sprite = Image(Point(250, 250), self.level_down[0])
		elif facing == "left": self.level_sprite = Image(Point(250, 250), self.level_left[0])
		else: self.level_sprite = Image(Point(250, 250), self.level_right[0])
		self.level_sprite.draw(glbl.gw)
		self.level_sprite.lower(glbl.load_overlay)

		self.map_up = glbl.MAP / "pointer_up.png"
		self.map_down = glbl.MAP / "pointer_down.png"
		self.map_left = glbl.MAP / "pointer_left.png"
		self.map_right = glbl.MAP / "pointer_right.png"
		if facing == "up": self.map_sprite =  Image(Point((self.map_x * 15) + 544, (self.map_y * 15) + 43), self.map_up)
		elif facing == "down": self.map_sprite =  Image(Point((self.map_x * 15) + 544, (self.map_y * 15) + 43), self.map_down)
		elif facing == "left": self.map_sprite =  Image(Point((self.map_x * 15) + 544, (self.map_y * 15) + 43), self.map_left)
		else: self.map_sprite =  Image(Point((self.map_x * 15) + 544, (self.map_y * 15) + 43), self.map_right)
		
		self.map_sprite.draw(glbl.gw)
		self.map_sprite.lower(glbl.load_overlay)
			

	def turn_up(self):
		if self.facing == "up": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "up", 1
		self.level_sprite = swap_image(self.level_sprite, self.level_up[self.idx])
		self.map_sprite = swap_image(self.map_sprite, self.map_up)
	def move_up(self, amt=1):
		self.level.move(0, 48 * amt)
		for i in self.overworld_objects: i.icon.move(0, 48 * amt)
		self.level_y -= 1 * amt
		self.map_sprite.move(0, -15 * amt)
		self.map_y -= 1 * amt
		
		
	def turn_down(self):
		if self.facing == "down": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "down", 1
		self.level_sprite = swap_image(self.level_sprite, self.level_down[self.idx])
		self.map_sprite = swap_image(self.map_sprite, self.map_down)
	def move_down(self, amt=1):
		self.level.move(0, -48 * amt)
		for i in self.overworld_objects: i.icon.move(0, -48 * amt)
		self.level_y += 1 * amt
		self.map_sprite.move(0, 15 * amt)
		self.map_y += 1 * amt


	def turn_left(self):
		if self.facing == "left": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "left", 1
		self.level_sprite = swap_image(self.level_sprite, self.level_left[self.idx])
		self.map_sprite = swap_image(self.map_sprite, self.map_left)
	def move_left(self, amt=1):
		self.level.move(48 * amt, 0)
		for i in self.overworld_objects: i.icon.move(48 * amt, 0)
		self.level_x -= 1 * amt
		self.map_sprite.move(-15 * amt, 0)
		self.map_x -= 1 * amt


	def turn_right(self):
		if self.facing == "right": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "right", 1
		self.level_sprite = swap_image(self.level_sprite, self.level_right[self.idx])
		self.map_sprite = swap_image(self.map_sprite, self.map_right)
	def move_right(self, amt=1):
		self.level.move(-48 * amt, 0)
		for i in self.overworld_objects: i.icon.move(-48 * amt, 0)
		self.level_x += 1 * amt
		self.map_sprite.move(15 * amt, 0)
		self.map_x += 1 * amt


class OverworldObject():
	def __init__(self, type, x, y, pnt, icon_directions):

		self.type = type

		self.x = x
		self.y = y

		self.up = icon_directions[0]
		self.down = icon_directions[1]
		self.left = icon_directions[2]
		self.right = icon_directions[3]
		self.icon = Image(pnt, icon_directions[1])
		
		self.activated = False

	def turn(self, direction):
		if direction == 'up': self.icon = swap_image(self.icon, self.up, True)
		if direction == 'down': self.icon = swap_image(self.icon, self.down, True)
		if direction == 'left': self.icon = swap_image(self.icon, self.left, True)
		if direction == 'right': self.icon = swap_image(self.icon, self.right, True)
	
	def move(self, direction):
		if direction in ["up", "w"]:
			self.y -= 1
			self.turn('up')
			self.icon.move(0, -48)
		elif direction in ["down", "s"]:
			self.y += 1
			self.turn('down')
			self.icon.move(0, 48)
		elif direction in ["left", "a"]:
			self.x -= 1
			self.turn('left')
			self.icon.move(-48, 0)
		elif direction in ["right", "d"]:
			self.x += 1
			self.turn('right')
			self.icon.move(48, 0)



	# All these methods will be overwritten.
	def check_activation(self, player_x, player_y):
		pass

	def activation(self):
		pass


class Captain(OverworldObject):
	def __init__(self, id, pnt, x, y):
		enemy_type = id.split('_')[0]
		if enemy_type == 'goblin':
			sprites = ['goblin_up.png', 'goblin_down.png', 'goblin_left.png', 'goblin_right.png',]
			self.e = Goblin(captain=True)
		elif enemy_type == 'rat':
			sprites = ['rat_up.png', 'rat_down.png', 'rat_left.png', 'rat_right.png',]
			self.e = Rat(captain=True)
		elif enemy_type == 'wolf':
			sprites = ['wolf_up.png', 'wolf_down.png', 'wolf_left.png', 'wolf_right.png',]
			self.e = Wolf(captain=True)
		elif enemy_type == 'slime':
			sprites = ['slime_up.png', 'slime_down.png', 'slime_left.png', 'slime_right.png',]
			self.e = Slime(captain=True)
		elif enemy_type == 'spider':
			sprites = ['spider_up.png', 'spider_down.png', 'spider_left.png', 'spider_right.png',]
			self.e = Spider(captain=True)
		elif enemy_type == 'snake':
			sprites = ['snake_up.png', 'snake_down.png', 'snake_left.png', 'snake_right.png',]
			self.e = Snake(captain=True)
		elif enemy_type == 'bear':
			sprites = ['bear_up.png', 'bear_down.png', 'bear_left.png', 'bear_right.png',]
			self.e = Bear(captain=True)
		elif enemy_type == 'goblin_warrior':
			sprites = ['goblin_warrior_up.png', 'goblin_warrior_down.png', 'goblin_warrior_left.png', 'goblin_warrior_right.png',]
			self.e = Goblin_Warrior(captain=True)
		elif enemy_type == 'goblin_shaman':
			sprites = ['goblin_shaman_up.png', 'goblin_shaman_down.png', 'goblin_shaman_left.png', 'goblin_shaman_right.png',]
			self.e = Goblin_Shaman(captain=True)
		elif enemy_type == 'goblin_rider':
			sprites = ['goblin_rider_up.png', 'goblin_rider_down.png', 'goblin_rider_left.png', 'goblin_rider_right.png',]
			self.e = Goblin_Rider(captain=True)

		sprites = [glbl.FOLDER / 'captain_active.png', glbl.FOLDER / 'captain_active.png', glbl.FOLDER / 'captain_active.png', glbl.FOLDER / 'captain_active.png']
		
		super().__init__('captain', x, y, pnt, sprites)
		self.id = id
		self.alive = True
		self.start_x = x
		self.start_y = y

		self.icon = swap_image(self.icon, glbl.FOLDER / 'captain_passive.png')

	def route_to_player(self, level, player_x, player_y):

		potential_paths = ["  "]

		while potential_paths:

			path = potential_paths.pop(0)
			path_end_x, path_end_y = self.x, self.y
			
			for i in path[2:]:
				if i == "w": path_end_y -= 1
				elif i == "s": path_end_y += 1
				elif i == "a": path_end_x -= 1
				else: path_end_x += 1

			if path_end_x == player_x and path_end_y == player_y:
				return path[2]
			
			else:
				# Arbitrarily I've chosen a max path length of 7.
				# If it takes more than ten steps to reach the glbl.player, then chasing them just
				# 	isn't worth it.
				if len(path) < 9:

					# If the next step isn't a wall and neither of the last two steps were
					# 	moves that would negate this next step, add it as a potential path
					if level[path_end_y - 1][path_end_x] not in glbl.not_walkable + ['d'] and path[-2:].count('s') == 0:
						potential_paths.append(path + "w")
					if level[path_end_y + 1][path_end_x] not in glbl.not_walkable + ['u'] and path[-2:].count('w') == 0:
						potential_paths.append(path + "s")
					if level[path_end_y][path_end_x - 1] not in glbl.not_walkable + ['r'] and path[-2:].count('d') == 0:
						potential_paths.append(path + "a")
					if level[path_end_y][path_end_x + 1] not in glbl.not_walkable + ['l'] and path[-2:].count('a') == 0:
						potential_paths.append(path + "d")

		# If this point was reached, that means no paths were able to be found.
		return ""


	def check_activation(self, level, player_x, player_y):
		if not self.alive:
			return

		distance = (((self.x - player_x) ** 2) + ((self.y - player_y) ** 2)) ** .5\

		if 1 < distance < 4.1:

			if self.activated:
				route = self.route_to_player(level, player_x, player_y)

				if route == "":
					self.icon = swap_image(self.icon, glbl.FOLDER / "captain_passive.png")
					self.activated = False
				else: self.move(route)
				

			else:

				if self.route_to_player(level, player_x, player_y) != "":
					# self.icon = swap_image(self.icon, self.down)
					self.icon = swap_image(self.icon, glbl.FOLDER / "captain_active.png")
					self.activated = True

		# Because the Captain could have moved in the previous step, we have to recalculate distance.
		# If the glbl.player is on an adjacent space to the captain, then they will fight.
		distance = (((self.x - player_x) ** 2) + ((self.y - player_y) ** 2)) ** .5
		if distance == 1:

				dialogue(f"It's a {self.e.name} Captain!")
				self.e.name += ' Captain'
				glbl.player.battle(self.e)
				self.alive = False
				self.icon.undraw()


class RatHat(OverworldObject):
	def __init__(self, pnt, x, y, activated):
		super().__init__('reginald', x, y, pnt,
			[glbl.CHARACTERS / "reginald_up.png", glbl.CHARACTERS / "reginald_down.png", glbl.CHARACTERS / "reginald_left.png", glbl.CHARACTERS / "reginald_right.png"])
		self.id = 'reginald'
		self.path = ['']
		self.talked = False

		if activated:
			self.activated = True
			self.talked = True
			self.icon = swap_image(self.icon, self.right)
			
			

	
	def talk(self, player_x, player_y):
		
		self.talked = True

		# Turn Reginald to face the glbl.player:
		# If the glbl.player and Reginald are on the same x level, they must have approched from above.
		if player_x == self.x:
			if player_y < self.y:
				self.turn('up')
				self.path.append('up')
				player_icon.turn_down()
				player_icon.turn_down()

			elif player_y > self.y:
				self.turn('down')
				self.path.append('down')
				player_icon.turn_up()
				player_icon.turn_up()

		# Else if the glbl.player is to the left of Reginald:
		elif player_x < self.x:
			self.turn('left')
			self.path.append('left')
			player_icon.turn_right()
			player_icon.turn_right()

		# Else if the glbl.player is to the right of Reginald
		elif player_x > self.x:
			self.turn('right')
			self.path.append('right')
			player_icon.turn_left()
			player_icon.turn_left()

		# Play the dialogue from rat_w_hat() in random_encounters.py
		option = rat_w_hat() 

		# If that conversation returns "fight", the glbl.player will fight Reginald.
		if option == 'fight':
			glbl.game_stats['reginald'] = 4
			glbl.player.battle(Reginald())
		
		# Else if the glbl.player has told Reginald to follow them, set activated to True.
		elif option == 'follow':
			self.activated = True

		# Else if the glbl.player has told Reginald to stay in his place, set activated to False.
		elif option == 'stay':
			self.activated = False


	def check_activation(self, level, player_x, player_y):

		distance = (((self.x - player_x) ** 2) + ((self.y - player_y) ** 2)) ** .5
			
		# If the glbl.player told Reginald to follow them:
		if self.activated:

			# If the glbl.player is more than 2 spaces away from Reginald:
			if distance > 2.3:

				self.talked = False
				x = player_x - self.x
				y = player_y - self.y
				angle = atan2(y, x) + pi

				# On the unit circle:
				# From (-1, 0) to (-1, 1):
				if 5.497787143782138 <= angle < 6.283185307179586: order = ['a', 's', 'w', 'd']
				
				# From (-1, 1) to (0, 1):
				elif 4.71238898038469 <= angle < 5.497787143782138: order = ['s', 'a', 'd', 'w']
				
				# From (0, 1) to (1, 1):
				elif 3.9269908169872414 <= angle < 4.71238898038469: order = ['s', 'd', 'a', 'w']
				
				# From (1, 1) to (1, 0):
				elif 3.141592653589793 <= angle < 3.9269908169872414: order = ['d', 's', 'w', 'a']
				
				# From (1, 0) to (1, -1):
				elif 2.356194490192345 <= angle < 3.9269908169872414: order = ['d', 'w', 's', 'a']
				
				# From (1, -1) to (0, -1):
				elif 1.5707963267948966 <= angle < 2.356194490192345: order = ['w', 'd', 'a', 's']
				
				# From (0, -1) to (-1, -1):
				elif 0.7853981633974483 <= angle < 1.5707963267948966: order = ['w', 'a', 'd', 's']
				
				# From (0, -1) to (-1, -1):
				else: order = ['a', 'w', 's', 'd']


				for i in order:
					if i == 'w' and level[self.y - 1][self.x] not in glbl.not_walkable + ['d']:
						self.move('up')
						break
					elif i == 's' and level[self.y + 1][self.x] not in glbl.not_walkable + ['u']:
						self.move('down')
						break
					elif i == 'a' and level[self.y][self.x - 1] not in glbl.not_walkable + ['r']:
						self.move('left')
						break
					elif i == 'd' and level[self.y][self.x + 1] not in glbl.not_walkable + ['l']:
						self.move('right')
						break
					
			# Else if the glbl.player is right next to Reginald:
			elif not self.talked and distance == 1:
				self.talk(player_x, player_y)


		# Else Reginald is standing still.
		else:

			# If the glbl.player is right next to Reginald and they haven't talked recently:
			if not self.talked and distance == 1:
				self.talk(player_x, player_y)

		# If the glbl.player moves two or more steps away, they haven't "recently" talked with Reginald.
		if distance >= 2:
			self.talked = False
			

class ShopBro(OverworldObject):
	def __init__(self, pnt, x, y):
		super().__init__('shopbro', x, y, pnt, [(glbl.MAP / '0.png'), (glbl.MAP / '0.png'), (glbl.MAP / '0.png'), (glbl.MAP / '0.png')])
		self.id = 'shopbro'
		self.talked = False
		self.alive = True

	def check_activation(self, player_x, player_y):

		distance = (((self.x - player_x) ** 2) + ((self.y - player_y) ** 2)) ** .5
		if distance == 1 and not self.talked:
			self.talked = True
			shopbro()

		elif distance >= 3:
			self.talked = False

		if glbl.game_stats['shopbro'] == 4:
			self.alive = False
			self.icon = swap_image(self.icon, glbl.FOLDER / "captain_passive.png")


class Fountain(OverworldObject):
	def __init__(self, pnt, x, y):
		super().__init__('fountain', x, y, pnt, [(glbl.MAP / '0.png'), (glbl.MAP / '0.png'), (glbl.MAP / '0.png'), (glbl.MAP / '0.png')])
		self.id = 'fountain'


# This method is used to swap images on glbl.gw.
# It is used primarily to swap the map icons.
# 	old_image is the Image() object that wil be replaced
# 	new_image is the file path to the image will be replacing old_image.
# 	level is a boolean that indicats that the original image was an object on the level, not the map.
# 		If that is the case, it needs to be lowered below the glbl.map_background.
def swap_image(old_image, new_image):
	img = Image(old_image.anchor, new_image)
	img.draw(glbl.gw)
	img.lower(old_image)
	old_image.undraw()
	return img


# This method is called every time the glbl.player tries to draw on the map.
# 	prior is the number of items that were on glbl.gw before exploring() was called.
# 	map_layout is the array that stores what the glbl.player's map looks like.
# 	item_id is the index of the map tile that will be changed.
# 	setting is the type of change that will occur.
def change_map(map_layout, x, y, setting):

	# If the item to change is a square's color and there wasn't a square at those x-y coordinates yet:
	if y < 25 and (not map_layout[y][x][1]):
		square_x, square_y = (x * 15) + 536, (y * 15) + 35
		map_layout[y][x][1] = Rectangle(Point(square_x, square_y), Point(square_x + 15, square_y + 15))

	# Else if the item to change is an icon and there wasn't an icon at those x y coordinates yet:
	elif not map_layout[y][x][1]:
		icon_x, icon_y = (x * 15) + 544, ((y - 25) * 15) + 43
		map_layout[y][x][1] = Image(Point(icon_x, icon_y), glbl.MAP / "null_icon.png")
		map_layout[y][x][1].draw(glbl.gw)

	# If the glbl.player is trying to color the square:
	if setting == "g": map_layout[y][x][1].setFill(color_rgb(80, 192, 146))
	elif setting == "b": map_layout[y][x][1].setFill(color_rgb(100, 164, 203))
	elif setting == "o": map_layout[y][x][1].setFill(color_rgb(246, 147, 28))
	elif setting == "y": map_layout[y][x][1].setFill(color_rgb(255, 217, 102))
	elif setting == "e": map_layout[y][x][1].setFill(color_rgb(147, 147, 147))

	# If the glbl.player is trying to draw in an icon:
	elif setting == "s": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "star.png")
	elif setting == "i": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "important.png")
	elif setting == "/": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "stairs_down.png")
	elif setting == "|": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "stairs_up.png")
	elif setting == "k": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "key.png")
	elif setting == "c": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "chest.png")
	elif setting == "u": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "arrow_up.png")
	elif setting == "d": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "arrow_down.png")
	elif setting == "l": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "arrow_left.png")
	elif setting == "r": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "arrow_right.png")
	elif setting == "0": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "0.png")
	elif setting == "1": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "1.png")
	elif setting == "2": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "2.png")
	elif setting == "3": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "3.png")
	elif setting == "4": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "4.png")
	elif setting == "5": map_layout[y][x][1] = swap_image(map_layout[y][x][1], glbl.MAP / "5.png")
	

	# Else the glbl.player is trying to erase:
	else:
		setting = "."
		map_layout[y][x][1].undraw()
		map_layout[y][x][1] = None
		
	# Change map_layout to reflect the change, and if the item wasn't erased, draw it onto the graphwin.
	map_layout[y][x][0] = setting
	if map_layout[y][x][1]:
		map_layout[y][x][1].draw(glbl.gw)


# This method is for updating out the background that displays the floor.
# When scrolls are used or something is harvested, the image that the background comes from
# 	needs to be changed.
# This will create that change and swap out the old image for the new updated one.
# 	floor_num is the floor number that the glbl.player has been exploring.
# 	player_icon is the object that stores where the glbl.player is on the level and map and their 
# 		sprites
# 	square is the file path for the image that will be pasted on top of the background to cause
# 		the change
# 	x will shift the x-coordinate of the upper-left corner where the image should be pasted.
# 	y will shift the y-coordinate of the upper-left corner where the image should be pasted.
def change_floor_background(floor_num, square, x=0, y=0):
	floor_background = PIL_Image.open(glbl.MAPS / f"floor_{floor_num}.png")
	floor_background.paste(PIL_Image.open(square), ((player_icon.level_x + x) * 48, (player_icon.level_y + y) * 48))
	floor_background.save(glbl.MAPS / f"floor_{floor_num}.png")
	player_icon.level = swap_image(player_icon.level, glbl.MAPS / f"floor_{floor_num}.png")
	player_icon.level.lower()


# This is the main method of the file.
# It is called every time the glbl.player enters or changes levels in the forest.
# 	floor_num is the floor number that the glbl.player will explore.
# 	start determines whether the glbl.player is heading up or down the forest.
#   	If start is True, they are heading up, False means they are heading down.
def exploring(floor_num, start="/", facing="right"):

	# Keep track of how many items are on glbl.gw before we start drawing new things.
	prior = len(glbl.gw.items)

	# Draw a black "mask" that will be placed over the screen to hide everything loading in behind it.
	glbl.load_overlay.draw(glbl.gw)

	# Update the global glbl.FOLDER to the biome type depending on the floor_num.
	# This will tell the code which folder in glbl.SPRITES it should look into.
	if floor_num < 6: glbl.FOLDER = glbl.SPRITES / "forest"
	elif floor_num < 11: glbl.FOLDER = glbl.SPRITES / "swamp"
	else: glbl.FOLDER = glbl.SPRITES / "mountain"

	# If the glbl.player is waiting for the Weapon Maker to finish their weapon, coming to the forest is a valid way to stall for time.
	if glbl.game_stats["magic_weapon_status"] == 2: glbl.game_stats["magic_weapon_status"] = 3

	# Both rect and map_setting will be used later
	rect = Rectangle(Point(0, 0), Point(0, 0))
	map_setting = None

	# battle_counter is used to keep track of the last time the player had to fight a normal enemy.
	battle_counter = 10


	# Using the fetch_level method from level_creation_tool.py, we get the level and save the coordinates of the starting stairs.
	level_layout, map_layout, overworld, level_x, level_y = fetch_level(floor_num, start)
	level_width, level_height = len(level_layout[0]), len(level_layout)

	# The Captains and whatnot are saved in overworld.
	# This converts them into objects.
	overworld_objects = []
	
	for i in range(len(overworld)):
		if overworld[i][3] == 0:
			p1 = Point(249 - (48 * (level_x - overworld[i][1])), 249 - (48 * (level_y - overworld[i][2])))
			save_tuple = (overworld[i][0], p1, overworld[i][1], overworld[i][2])

			if save_tuple[0] == "reginald":
				overworld_objects.append(RatHat(*save_tuple[1:], True if glbl.game_stats['reginald'] == 2 else False))
			elif save_tuple[0] == "shopbro":
				overworld_objects.append(ShopBro(*save_tuple[1:]))
			elif save_tuple[0] == "fountain":
				overworld_objects.append(Fountain(*save_tuple[1:]))
			else:
				overworld_objects.append(Captain(*save_tuple))

	# Read in the floor image and save it as the background layer.
	floor_background = Image(Point(249 + (48 * ((level_width // 2) - level_x)), 259 + (48 * ((level_height // 2) - level_y))), (glbl.MAPS / f"floor_{floor_num}.png"))
	
	# We need to move the background to slightly different places depending on the parity of 
	# 	level_x and level_y.
	# By default it is loaded into the position when level_width and level_height are odd, 
	# 	so check for everything else:
	if level_width % 2 != 0:
		# If level_width is odd but level_height is even:
		if level_height % 2 == 0:
			floor_background.move(0, -24)
			floor_background.draw(glbl.gw)
	else:
		# If level_width is even but level_height is odd:
		if level_height % 2 != 0:
			floor_background.move(-24, 0)
		# If both level_width and level_height are even:
		else:
			floor_background.move(-24, -24)
	floor_background.draw(glbl.gw)
	floor_background.lower(glbl.load_overlay)
	for i in overworld_objects: 
		i.icon.draw(glbl.gw)
		i.icon.lower(glbl.load_overlay)

	# Draw in the background for the map.
	glbl.map_background.draw(glbl.gw)
	glbl.map_background.lower(glbl.load_overlay)

	# Draw the squares for the map.
	for i in range(25):
		for j in range(30):
			map_color = map_layout[i][j][0]
			if map_color != ".":
				change_map(map_layout, j, i, map_color)
				map_layout[i][j][1].lower(glbl.load_overlay)

			map_color = map_layout[i + 25][j][0]
			if map_color != ".":
				change_map(map_layout, j, i + 25, map_color)
				map_layout[i + 25][j][1].lower(glbl.load_overlay)

	# Finally, draw in the icon that indicates the floor number on top.
	map_overlay = Image(Point(750, 250), glbl.MAP / "map_overlay.png")
	map_num = Image(Point(522, 21), glbl.MAP / f"map_{floor_num}_overlay.png")
	map_overlay.draw(glbl.gw)
	map_overlay.lower(glbl.load_overlay)
	map_num.draw(glbl.gw)
	map_num.lower(glbl.load_overlay)

	# Create the glbl.player as a Player object so we can keep track of where they are when they move around in the arrays.
	global player_icon
	player_icon = Player_Icon(floor_background, overworld_objects, level_x, level_y, facing)

	# Remove the loading screen:s
	glbl.load_overlay.undraw()

	# When the glbl.player enters the dungeon for the first time, glbl.game_stats["level_tutorial"] is True.
	# This means they have not completed the tutorial, which should now happen.
	# Afterwards, we change it to False so it won't trigger again.
	if glbl.game_stats["level_tutorial"]:
		glbl.game_stats["level_tutorial"] = False
		map_tutorial()


	# The game loop.
	while True:

		direction = glbl.gw.checkKey().lower()
		click = glbl.gw.checkMouse()

		# If the glbl.player clicked somewhere on the screen:
		if click:

			x, y = click.getX(), click.getY()

			# If the click was somewhere on the grid:
			if 537 < x < 987 and 35 < y < 410:

				x = int((x - 537) // 15)
				y = int((y - 36) // 15)

				# Change the map in accordance with the tool.
				# If the change is to a square:
				if map_setting in ["g", "b", "o", "y", "e", "erase_square"]:
					change_map(map_layout, x, y, map_setting)

					# If there's an icon on top, lower this square underneath it.
					if map_layout[y + 25][x][1] and map_layout[y][x][1]: map_layout[y][x][1].lower(map_layout[y + 25][x][1])
				
				# Else the change is to an icon.
				else:
					change_map(map_layout, x, y + 25, map_setting)
					# if map_layout[y + 25][x][1]: map_layout[y + 25][x][1].lower(map_overlay)
				


			# Else, if the click was on the lower palette:
			else:

				rect.undraw()

				# Square Color:
				if 424 < y < 442:
					if 533 < x < 565: map_setting, rect = "g", Rectangle(Point(534, 425), Point(564, 441))
					elif 569 < x < 601: map_setting, rect = "b", Rectangle(Point(570, 425), Point(600, 441))
				if 446 < y < 464:
					if 533 < x < 565: map_setting, rect = "o", Rectangle(Point(534, 447), Point(564, 463))
					elif 569 < x < 601: map_setting, rect = "y", Rectangle(Point(570, 447), Point(600, 463))
				if 468 < y < 486 and 551 < x < 583: map_setting, rect = "e", Rectangle(Point(552, 469), Point(582, 485))

				# Trashcans:
				if 439 <= y <= 471:
					if 605 <= x <= 637: map_setting, rect = "erase_square", Rectangle(Point(606, 440), Point(636, 470))
					if 648 <= x <= 680: map_setting, rect = "erase_icon", Rectangle(Point(649, 440), Point(679, 470))

				# Upper Row of Placable Icons:
				if 421 <= y <= 453:
					if 684 <= x <= 716: map_setting, rect = "s", Rectangle(Point(685, 422), Point(715, 452))
					if 720 <= x <= 752: map_setting, rect = "i", Rectangle(Point(721, 422), Point(751, 452))
					if 756 <= x <= 788: map_setting, rect = "k", Rectangle(Point(757, 422), Point(787, 452))
					if 792 <= x <= 824: map_setting, rect = "u", Rectangle(Point(793, 422), Point(823, 452))
					if 828 <= x <= 860: map_setting, rect = "d", Rectangle(Point(829, 422), Point(859, 452))
					if 864 <= x <= 896: map_setting, rect = "0", Rectangle(Point(865, 422), Point(895, 452))
					if 900 <= x <= 932: map_setting, rect = "1", Rectangle(Point(901, 422), Point(931, 452))
					if 936 <= x <= 968: map_setting, rect = "2", Rectangle(Point(937, 422), Point(967, 452))
					
				# Lower Row of Placeable Icons:
				if 457 <= y <= 489:
					if 684 <= x <= 716: map_setting, rect = "/", Rectangle(Point(685, 458), Point(715, 488))
					if 720 <= x <= 752: map_setting, rect = "|", Rectangle(Point(721, 458), Point(751, 488))
					if 756 <= x <= 788: map_setting, rect = "c", Rectangle(Point(757, 458), Point(787, 488))
					if 792 <= x <= 824: map_setting, rect = "l", Rectangle(Point(793, 458), Point(823, 488))
					if 828 <= x <= 860: map_setting, rect = "r", Rectangle(Point(829, 458), Point(859, 488))
					if 864 <= x <= 896: map_setting, rect = "3", Rectangle(Point(865, 458), Point(895, 488))
					if 900 <= x <= 932: map_setting, rect = "4", Rectangle(Point(901, 458), Point(931, 488))
					if 936 <= x <= 968: map_setting, rect = "5", Rectangle(Point(937, 458), Point(967, 488))

				# Redraw the Rectangle rect to give the simulation of transformation.
				rect.setOutline(color_rgb(59, 204, 255))
				rect.setWidth(3)
				rect.draw(glbl.gw)


		# If any key was pressed:
		if direction:

			# If the key was for moving in a direction:
			# These for directions are basically identical with minor changes, so they will only
			# 	be explained once here.
			if direction in ["up", "w"]:

				# Run turn_up(), which animates the glbl.player turning or moving on the level and map.
				player_icon.turn_up()

				# For readability, save the space that will be checked for eligibility to "space".
				space = level_layout[player_icon.level_y - 1][player_icon.level_x]
				
				# If the space the glbl.player is going to move to is a walkable space, and not an 
				# 	attempt to climb a ledge, move the glbl.player.
				if space not in glbl.not_walkable + ["d"]:
					player_icon.move_up()

				# Wait a split second before calling turn_up() again to complete the walking animation.
				sleep(.1)
				player_icon.turn_up()

				# Because movement occured, decrement battle_counter.
				# If this number hits 0, the glbl.player will battle a small enemy.
				if randint(0, 4) > 1: battle_counter -= 1

			elif direction in ["down", "s"]:
				player_icon.turn_down()
				space = level_layout[player_icon.level_y + 1][player_icon.level_x]
				if space not in glbl.not_walkable + ["u"]:
					player_icon.move_down()
				sleep(.1)
				player_icon.turn_down()
				if randint(0, 4) > 1: battle_counter -= 1
			elif direction in ["left", "a"]:
				player_icon.turn_left()
				space = level_layout[player_icon.level_y][player_icon.level_x - 1]
				if space not in glbl.not_walkable + ["r"]:
					player_icon.move_left()
				sleep(.1)
				player_icon.turn_left()
				if randint(0, 4) > 1: battle_counter -= 1
			elif direction in ["right", "d"]:
				player_icon.turn_right()
				space = level_layout[player_icon.level_y][player_icon.level_x + 1]
				if space not in glbl.not_walkable + ["l"]:
					player_icon.move_right()
				sleep(.1)
				player_icon.turn_right()
				if randint(0, 4) > 1: battle_counter -= 1

			# If the glbl.player is trying to open the pause menu:
			elif direction in ["m", "shift_l"]:
				pause_menu(False)
			
			# If the glbl.player wants to use a scroll:
			elif direction in ["e"]: use_item(level_layout, floor_num)


			# To speed up the below code, I initialize an x and y.			
			x, y = player_icon.level_x, player_icon.level_y

			# If the square the glbl.player just moved to is not colored on their map, color that spot green:
			if map_layout[player_icon.map_y][player_icon.map_x][0] == ".":
				change_map(map_layout, player_icon.map_x, player_icon.map_y, "g")
				map_layout[player_icon.map_y][player_icon.map_x][1].draw(glbl.gw)

				if map_layout[player_icon.map_y + 25][player_icon.map_x][1]:
					map_layout[player_icon.map_y][player_icon.map_x][1].lower(map_layout[player_icon.map_y + 25][player_icon.map_x][1])
				else: map_layout[player_icon.map_y][player_icon.map_x][1].lower(map_overlay)

			# If the glbl.player is standing on a special square:
			if level_layout[y][x] != ".":

				# If the glbl.player is standing on the square for the stairs up:
				if level_layout[y][x] == "|":
					
					# Ask to confirm if the glbl.player wants to head up:
					if dialogue("Would you like to continue on?", ["Yes", "No"]) == 0:

						# Save any changes that may have been made on the floor, like burnt trees.
						# Also remove all items from the graphwin that were drawn when exploring() was called.
						save_and_close(floor_num, level_layout, map_layout, overworld, overworld_objects, prior)
						exploring(floor_num + 1)
						break

				# Else if the glbl.player is standing on the square for the stairs back down:
				elif level_layout[y][x] == "/":

					# If the glbl.player is on any of the floors that are the first for the biome, they can elect to head straight back home.
					if floor_num in [1, 6, 11]:
						if dialogue("Do you want to return to town?", ["Yes", "No"]) == 0:
							if glbl.game_stats['reginald'] == 2:
								glbl.game_stats['reginald'] = 5
								rat_w_hat()

							elif glbl.game_stats['reginald'] == 6:
								rat_w_hat()
								return

							save_and_close(floor_num, level_layout, map_layout, overworld, overworld_objects, prior)
							return

					# Else ask if they would like to return to the floor directly under the current one.
					elif dialogue("Would you like to head down?", ["Yes", "No"]) == 0:
						save_and_close(floor_num, level_layout, map_layout, overworld, overworld_objects, prior)
						exploring(floor_num - 1, "|")
						break

				# If the glbl.player is standing on a harvestable square:
				elif level_layout[y][x] == "A":
					gather_items(level_layout, floor_num)

				# If the glbl.player is standing on the chest or its key:
				elif level_layout[y][x] in ["k", "K"]:
					level_layout[y][x] = chest(level_layout[y][x], floor_num)

				# If the glbl.player is standing on a teleport square:
				elif level_layout[y][x] in glbl.teleport_chars:
					dialogue("This magic circle will teleport you somewhere up or down the mountain.")
					if dialogue("Are you sure you want to use it?", ["Yes", "No"]) == 0:
						to_floor = link_portal(floor_num, level_layout, x, y)
						save_and_close(floor_num, level_layout, map_layout, overworld_objects, prior)
						exploring(to_floor, glbl.teleport_chars[floor_num], player_icon.facing)
						break

			# Check to see if any of the overworld objects are activated:
			for i in overworld_objects:
				i_type = i.type

				if i_type == 'captain':
					i.check_activation(level_layout, x, y)

				elif i_type == 'reginald':
					i.check_activation(level_layout, x, y)					

				else:
					i.check_activation(x, y)


			# If the battle_counter is at 0, the glbl.player battles a small enemy.
			if battle_counter == 0:
				battle_counter = 10
				if floor_num < 6: e = choice([Goblin(), Rat(), Wolf()])
				elif floor_num < 11: e = choice([Slime(), Spider(), Snake()])
				else: e = choice([Bear(), Goblin_Warrior(), Goblin_Shaman(), Goblin_Shaman()])
				
				dialogue(e.appearance)
				battle_music = pygame.mixer.music.load("Battle_Music.wav")
				pygame.mixer.music.play(-1)
				glbl.player.battle(e)


# This is the method used to link together the portal from this floor to its floor.
# 	floor_num is the floor number that the glbl.player is exploring
# 	character is the character that indicates what floor this portal leads to
def link_portal(cur_floor, cur_level, cur_x, cur_y):
	
	if cur_level[cur_y][cur_x] == "`":
		to_floor = 0	

		floors_linked = True
		while floors_linked:
			floors_linked = False
			
			to_floor = randint(cur_floor - 3, cur_floor + 2)
			if to_floor < 1:
				to_floor = 1
			elif to_floor > 15:
				to_floor = 15

			for i in glbl.game_stats["portals"]:
				if to_floor == i[0] and cur_floor == i[1]:
					floors_linked = True


		glbl.game_stats["portals"].append((cur_floor, to_floor))

		new_level, new_map, _, _ = fetch_level(to_floor)

		while True:
			to_x, to_y = randint(1, len(new_level[0]) - 1), randint(1, len(new_level) - 1)
			if new_level[to_y][to_x] == ".":
				break

		cur_level[cur_y][cur_x] = glbl.teleport_chars[to_floor]
		new_level[to_y][to_x] = glbl.teleport_chars[cur_floor]

		file = open(glbl.MAPS / f"floor_{to_floor}.txt", "w")
		file.write(("\n".join("".join(j[0] for j in i) for i in new_map)) + "\n")
		file.write("\n".join("".join(i) for i in new_level))
		file.close()

		floor_background = PIL_Image.open(glbl.MAPS / f"floor_{to_floor}.png")
		floor_background.paste(PIL_Image.open(glbl.SPRITES / glbl.FOLDER / "teleport.png"), (to_x * 48, to_y * 48))
		floor_background.save(glbl.MAPS / f"floor_{to_floor}.png")



	else:
		to_floor = glbl.teleport_chars.index(cur_level[cur_y][cur_x])
		
		
	return to_floor
	
		

# This method is called when the glbl.player walks over a harvestable space.
# 	level_layout is the array that stores the level
# 	floor_num is the floor number that the glbl.player is exploring
# 	player_icon is the object that stores where the glbl.player is on the level and map and their sprites
def gather_items(level_layout, floor_num):

	dialogue("Discovered some items!")
	level_layout[player_icon.level_y][player_icon.level_x] = choice(["C", "D", "E"])
	change_floor_background(floor_num, glbl.SPRITES / glbl.FOLDER / "harvest0.png")



# This method is called when the glbl.player walks over a level's chest or its key:
# 	space is the space the glbl.player is standing on
# 	floor_num is the floor number that the glbl.player is exploring
def chest(space, floor_num):

	# If the glbl.player is standing on a key:
	if space == "k":
		dialogue(f"Discovered the Floor {floor_num} Chest Key!")
		dialogue(f"Find the corresponding Chest to get its contents.")
		glbl.game_stats["floor_key"][floor_num] = True
		change_floor_background(floor_num, glbl.SPRITES / glbl.FOLDER / "path0.png")

	# If the glbl.player is standing on a chest:
	if space == "K":

		# If the glbl.player has the level's key:
		if glbl.game_stats["floor_key"][floor_num] == True:
			dialogue("You used the key and found several items and EXP!")
			change_floor_background(floor_num, glbl.SPRITES / glbl.FOLDER / "chest_open.png")

		# Else they don't have the level's key:
		else:
			dialogue(f"Discovered the Floor {floor_num} Chest!")
			dialogue("Find the corresponding Key to get its contents.")

			# Return "K" so the glbl.player can still unlock the chest later.
			return "K"
	
	# Return "." so the glbl.player won't recollect an already obtained key or reopen an opened chest.
	return "."



# This method is called when the glbl.player tries to use an item.
# 	level_layout is the array that stores the level
# 	floor_num is the level number
# 	prior is the number of objects in the graphwin prior to drawing with explore()
# 	glbl.player is the glbl.player object
# 	player_icon is the object that stores where the glbl.player is on the level and map and their sprites
def use_item(level_layout, floor_num):

	facing, level_x, level_y = player_icon.facing, player_icon.level_x, player_icon.level_y
	floor_background = PIL_Image.open(glbl.MAPS / f"floor_{floor_num}.png")

	while True:
		items = []

		weapon = "Use Storm Blade" if glbl.player.character_class == "Warrior" else "Use Blaze Rod" if glbl.player.character_class == "Sorcerer" else "Use Vorpal Daggers"
		if glbl.game_stats["magic_weapon_status"] == 4:
			items.append(weapon)

		if glbl.player.items["Fire Scroll"] + glbl.player.items["Ice Scroll"] + glbl.player.items["Thunder Scroll"] > 0:
			items.append("Scroll")

		items.append("Cancel")


		x = dialogue("Which item do you want to use?", items, return_arg=True)

		if x == "Cancel":
			return

		if x.count("Use") == 1:
			if x == "Use Storm Blade":
				for i in range(-1, 2):
					print()


			if x == "Use Blaze Rod":
				print("Blaze Rod")

			# Else, the glbl.player is using the Vorpal Daggers
			else:

				# x0 and y0 are the base coordinates, while x1 and y1 are how much they'll change by.
				x0, y0, x1, y1 = level_x, level_y, 0, 0
				if facing == "up" and level_layout[y0 - 1][x0] in ["W", "I"]:
					y1 = -1
				elif facing == "down" and level_layout[y0 + 1][x0] in ["W", "I"]:
					y1 = 1
				elif facing == "left" and level_layout[y0][x0 - 1] in ["W", "I"]:
					x1 = -1
				elif facing == "right" and level_layout[y0][x0 + 1] in ["W", "I"]:
					x1 = 1
				# If the glbl.player is not facing water or ice, this dialogue will play.
				else:
					dialogue("You are not facing water or ice.")
					return

				# If this is reached, the glbl.player is facing water or ice and is able to warp.
				# distance will be how far the glbl.player warps.
				distance = 0
				while True:
					x0, y0 = x0 + x1, y0 + y1
					if level_layout[y0][x0] in ["W", "I"]:
						distance += 1
					elif level_layout[y0][x0] in [".", "A", "B", "C", "D", "E"]:
						distance += 1
						break
					else:
						dialogue("There isn't enough space on the other side to warp.")
						return

				if facing == "up":
					player_icon.move_up(amt=distance)
				elif facing == "down":
					player_icon.move_down(amt=distance)
				elif facing == "left":
					player_icon.move_left(amt=distance)
				else:
					player_icon.move_right(amt=distance)

				return

		
		elif x == "Scroll":

			while True:

				scrolls = []

				if glbl.player.items["Fire Scroll"] > 0:
					scrolls.append(f"Fire Scroll ({glbl.player.items['Fire Scroll']})")
				if glbl.player.items["Ice Scroll"] > 0:
					scrolls.append(f"Ice Scroll ({glbl.player.items['Ice Scroll']})")
				if glbl.player.items["Thunder Scroll"] > 0:
					scrolls.append(f"Thunder Scroll ({glbl.player.items['Thunder Scroll']})")
				scrolls.append("Cancel")

				x = dialogue("Which scroll?", scrolls, return_arg=True)

				if x == "Cancel":
					break

				if x.count("Fire") > 0:
					wall, line = "T", "are no trees"
					glbl.player.items["Fire Scroll"] -= 1
					square = glbl.SPRITES/ glbl.FOLDER / "stump.png"

				elif x.count("Ice") > 0:
					wall, line = "W", "is no water"
					glbl.player.items["Ice Scroll"] -= 1
					square = glbl.SPRITES/ glbl.FOLDER / "ice.png"

				else:
					wall, line = "R", "are no rocks"
					glbl.player.items["Thunder Scroll"] -= 1
					square = glbl.SPRITES/ glbl.FOLDER / "pebbles.png"

				if facing == "up" and level_layout[level_y - 1][level_x] == wall:
					level_layout[level_y - 1][level_x] = "."
					change_floor_background(floor_num, square, y=-1)
				elif facing == "down" and level_layout[level_y + 1][level_x] == wall:
					level_layout[level_y + 1][level_x] = "."
					change_floor_background(floor_num, square, y=1)
				elif facing == "left" and level_layout[level_y][level_x - 1] == wall:
					level_layout[level_y][level_x - 1] = "."
					change_floor_background(floor_num, square, x=-1)
				elif facing == "right" and level_layout[level_y][level_x + 1] == wall:
					level_layout[level_y][level_x + 1] = "."
					change_floor_background(floor_num, square, x=1)

				else:
					if wall != "T": glbl.player.items["Fire Scroll"] += 1
					elif wall != "W": glbl.player.items["Ice Scroll"] += 1
					else: glbl.player.items["Thunder Scroll"] += 1
					dialogue(f"There {line} there.")
				
				
				return



# This method saves the level and map layouts to file, as well as removes all items from the screen.
# 	floor_num is the floor number that the glbl.player was exploring
# 	level_layout is the array that was storing the level
# 	map_layout is the array that was storing the glbl.player's map
# 	prior is the index after the last drawn item on the graphwin prior to starting the exploring() method
def save_and_close(floor_num, level_layout, map_layout, overworld, overworld_objects, prior):

	# Bring back the loading screen:
	glbl.load_overlay.draw(glbl.gw)

	# Open up "floor_{floor_num}.txt" (where floor_num is the floor number) so it can be overwritten.
	file = open(glbl.MAPS / f"floor_{floor_num}.txt", "w")

	# map_layout is the first thing that must be written into the file.
	# A newline must be added at the very end because so the level_layout starts off on a new line.
	file.write(("\n".join("".join(j[0] for j in i) for i in map_layout)) + "\n")
	
	# Now write in level_layout.
	file.write("\n".join("".join(i) for i in level_layout) + "\n")

	# Grab all the names of the objects still in the overworld.
	names = []
	for i in overworld_objects:
		if i.id == 'reginald':
			if glbl.game_stats['reginald'] in [1, 3]:
				file.write(f'reginald {i.x} {i.y} {0} ')

		if i.id == 'shopbro':
			if glbl.game_stats['shopbro'] != 4:
				file.write(f'shopbro {i.x} {i.y} {0} ')

		# Else the object is a captain.
		else:
			file.write(f'{i.id} {i.start_x} {i.start_y} {0 if i.alive else 3} ')


	# Close the file so everything is changed.
	file.close()

	# Since the file saving is done, we now remove everything currently on the graphwin.
	for i in glbl.gw.items[prior:]: i.undraw()



# All this method is is a bunch of dialogue that plays only the first time the glbl.player enter the forest.
# It simple explains that the left side of the screen is the level, and the right side is the map.
def map_tutorial():
	dialogue("Welcome to the forest!")
	dialogue("This is your first time, so let me explain some things.")
	dialogue("Here on the left is the level, which is randomly generated upon entering")
	dialogue("Over on the right is your map.")
	dialogue("Feel free to draw it however you see fit.")
	dialogue("Your goal in every level is to find the stairs up as you work your way towards the mountain and the orc's den.")
	dialogue("To return to town, you will have to head back down the Floor 1 stairs.")
	dialogue("If you ever get lost or stuck, talk to the Librarian.")
	dialogue("Good luck!")



if __name__ == "__main__":

	seed(0)
	
	glbl.player = Rogue()
	glbl.player.items['Potions'] = 3
	glbl.player.items['Fire Scroll'] = 3
	glbl.player.current_EXP += 3


	glbl.game_stats["magic_weapon_status"] = 4
	glbl.game_stats["level_tutorial"] = False
	glbl.game_stats['reginald'] = 1
	glbl.game_stats['shopbro'] = 1
	
	exploring(1)

	glbl.gw.getKey()