# globals.py
from base64 import b64encode
from pathlib import Path
from random import randint
from time import sleep

from graphics import GraphWin, Point, Line, Rectangle, Polygon, Text, Image, color_rgb

class GameOver(Exception):
	def __init__(self, arg):
		self.type = arg

class Bar:

	def __init__(self, numerator, denominator, color, p1, p2, show_text=True):
		self.numerator = numerator if numerator < denominator else denominator
		self.denominator = denominator
		self.color = color
		self.p1 = p1
		self.p2 = p2

		self.length = p2.x - p1.x
		self.height = p2.y - p1.y
		self.center = Point(self.p1.x + (self.length / 2), self.p1.y + (self.height / 2))
		
		self.items = []

		self.items.append(Rectangle(p1, Point(self.p1.x + (self.length * self.numerator / self.denominator), self.p2.y)))
		self.items[0].setFill(self.color)
		self.items.append(Rectangle(p1, p2))
		self.items[1].setWidth(2)

		self.show_text = False if self.height - 8 <= 5 else show_text
		
		if show_text:
			self.items.append(Text(self.center, f"{self.numerator}/{self.denominator}"))
			self.items[2].setAnchor("c")
			self.items[2].setSize(int(self.height - 8))
		


	def show(self):
		for i in self.items:
			i.draw(gw)

	def update(self, numerator, denominator=-1):

		for i in self.items:
				i.undraw()
		if denominator != -1:
			self.denominator = denominator

		self.numerator = numerator if numerator < self.denominator else self.denominator

		self.items[0] = Rectangle(self.p1, Point(self.p1.x + (self.length * self.numerator / self.denominator), self.p2.y))
		self.items[0].setFill(self.color)

		if self.show_text: self.items[2].setText(f"{self.numerator}/{self.denominator}")

		for i in self.items:
			i.draw(gw)		


	def hide(self):
		for i in self.items:
			i.undraw()


def dialogue(line, choices = [], color=["white"], return_arg=False, right=False, speed=.02, type_length=0):

	# Initialize variables that will be used later.
	start = 500 if right else 0
	selection = 0
	prior = len(gw.items)
	if type(color) == str: color=[color]

	# Create the dialogue box
	dialogue_box = Rectangle(Point(start + 11, 403), Point(start + 489, 488))
	dialogue_box.setFill(color_rgb(50, 50, 50))
	dialogue_box.setWidth(3)
	dialogue_box.draw(gw)

	# Create the Text objects that will display dialogue.
	texts = []
	for i in color:
		text = Text(Point(start + 25, 418), "") 
		text.setTextColor(i)
		text.setSize(20)
		text.setAnchor("nw")
		text.draw(gw)
		texts.append(text)

	line = line.split()
	
	text_num = 0
	num_texts = len(texts)
	line_length = 0
	overflow = 0
	skip = False
	for word in line:

		word_length = len(word)
		if line_length + word_length + 1 > 29:
			word = '\n' + word
			line_length = 0
			overflow += 1
		line_length += word_length + 1
		
		if overflow > 1:
			for j in texts: j.setText(j.getText()[j.getText().index("\n") + 1:])
			overflow = 1

		for j in word + ' ':
			if j == '`':
				text_num += 1

			else:				
				for k in range(num_texts):

					key = gw.checkKey().lower()
					if key in ["return", "space", "escape"]:
						skip = True

					if k == text_num:
						texts[k].setText(texts[k].getText() + j)
					elif j == '\n':
						texts[k].setText(texts[k].getText() + '\n')
					else:
						texts[k].setText(texts[k].getText() + ' ')

			if not skip: sleep(speed)

	
	# If type_length is 0 and the array of choices that is passed in isn't empty, the player is supposed
	# 	to make a selection from a list of choices.	
	length_choices = len(choices)
	if type_length == 0:
		center = 374 - (30 * (length_choices - 1))
		selector = Polygon(Point(start + 478, center - 6), Point(start + 478, center + 6), Point(start + 461, center))
		selector.setFill("red")

		if length_choices > 0:
			answer = ""
			longest_answer = 0
			for i in choices:
				answer += f"{i}\n"
				longest_answer = max(longest_answer, len(i))
			answer = answer[:-1]

			choice_box = Rectangle(Point(start + 473 - (16 * (longest_answer + 2)), 382 - (30 * length_choices)), Point(start + 489, 395))
			choice_box.setFill(color_rgb(50, 50, 50))
			choice_box.setWidth(3)
			choice_box.draw(gw)


			choice_text = Text(Point(start + 453, 390), "")
			choice_text.setAnchor("se")
			choice_text.setJustification("right")
			choice_text.setSize(20)
			choice_text.draw(gw)

			

			choice_text.setText(answer)
			selector.draw(gw)

			
		while True:
			key = gw.checkKey().lower()

			if key != "":
				if key in ["space", "return"]:
					break

				elif key in ["escape"]:
					while selection < length_choices - 1:
						selector.move(0, 30)
						selection += 1

				elif key in ["m", "shift_l"]:
					pause_menu(not right)


				elif length_choices > 0:
					if key in ["up", "w", "left", "a"]:
						selection = (selection - 1) % length_choices
						if selection != length_choices - 1:
							selector.move(0, -30)
						else:
							selector.move(0, 30 * (length_choices - 1))


					elif key in ["down", "s", "right", "d"]:
						selection = (selection + 1) % length_choices
						if selection != 0:
							selector.move(0, 30)
						else:
							selector.move(0, -30 * (length_choices - 1))


	# Else, the player is typing in some response.
	# This is only used a couple times in play_game.py		
	elif type_length > 0:

		selection = ""

		shown_name = Text(Point(250 - (16 * type_length) // 2, 467))
		shown_name.setText("")
		shown_name.draw(gw)

		text_underline = shown_name.clone()
		text_underline.setText("-" * type_length)
		text_underline.move(0, 13)
		text_underline.draw(gw)

		bar = shown_name.clone()
		bar.move(-7, 0)
		bar.setText('|')
		bar.draw(gw)
		bar_flash = 0
		bar_shown = True

		while True:
			key = gw.checkKey()			

			if key:

				if len(selection) < type_length and key in alphabet + punctuation:
					if key == 'space': selection += ' '
					else: selection += key

					bar.move(16, 0)

				elif len(selection) > 0 and key == 'BackSpace':
					selection = selection[:-1]
					bar.move(-16, 0)

				elif key == 'Return':
					break
				
				bar_flash = 0
				if not bar_shown:
					bar_shown = True
					bar.draw(gw)
				shown_name.setText(selection)

			else:
				bar_flash += 1

				if bar_flash == 40000:
					bar_flash = 0
					if bar_shown:
						bar_shown = False
						bar.undraw()
					else:
						bar_shown = True
						bar.draw(gw)



	gw.clear(prior)

	if length_choices == 0 and type_length == 0: return -1
	elif return_arg: return choices[selection].split(":")[0]
	else: return selection
		

def inventory():
	string = ""

	# Because the items are stored in a dictionary, to display all the player's items we need to run through all possible items step by step.
	if game_stats["magic_weapon_status"] == 4:
		weapon = "Storm Blade" if player.character_class == "Warrior" else "Blaze Rod" if player.character_class == "Sorcerer" else "Vorpal Daggers"
		string += weapon + "\t "
	if player.items["Shield"] != 0:
		string += "Shield"
	if string != "": string += "\n"

	if player.items["Potions"] != 0:
		string += f"Potions: {str(player.items['Potions']).rjust(6)}  "
	if player.items["Apples"] != 0:
		string += f"Apples: {str(player.items['Apples']).rjust(8)}"
	if string.count("Potions") != 0 or string.count("Apples") != 0:
		string += "\n"

	if player.items["magic_item"] != 0:
		string += f'{"Magic Wood" if player.character_class == "Warrior" else "Magic Ore"}: {str(player.items["magic_item"]).rjust(4)}  '
	if player.items["Herbs"] != 0:
		string += f"Herbs: {str(player.items['Herbs']).rjust(9)}"
	if string.count("Magic") != 0 or string.count("Herbs") != 0:
		string += "\n"


	if player.items["Fire Scroll"] != 0:
		string += f"Fire Scrolls: {str(player.items['Fire Scroll']).rjust(19)}\n"
	if player.items["Ice Scroll"] != 0:
		string += f"Ice Scrolls: {str(player.items['Ice Scroll']).rjust(20)}\n"
	if player.items["Thunder Scroll"] != 0:
		string += f"Thunder Scrolls: {str(player.items['Thunder Scroll']).rjust(16)}\n"

	return string


def pause_menu(right):

	start = 500 if right else 0
	prior = len(gw.items)

	pause_overlay = Image(Point(500, 250), MAP / "pause_overlay.png")
	pause_overlay.draw(gw)


	# Everything for the Character Information
	info_box = Rectangle(Point(551 - start, 100), Point(959 - start, 400))
	info_box.setFill(color_rgb(50, 50, 50))
	info_box.setWidth(3)
	info_box.draw(gw)

	# The Character Icon
	info_icon = Image(Point(613 - start, 163), MAPS / "characters" / f"{player.character_class}_portrait.png")
	info_icon.draw(gw)

	# Shows the Header that includes the player's name and level.
	info_header = Text(Point(572 - start, 179))
	info_header.setAnchor("w")
	info_header.setSize(22)
	info_header.setText(f"      {player.name + f'LV: {player.lvl}'.rjust(16)[len(player.name):]}\n      HP:\n      EXP:\nItems:")
	info_header.draw(gw)

	# Draw the HP bar.
	hp_bar = Bar(player.current_HP, player.base_HP, "red", Point(750 - start, 149), Point(948 - start, 173))
	hp_bar.show()


	# Draws the EXP bar
	exp_bar = Bar(player.current_EXP, player.next_EXP, "green", Point(750 - start, 179), Point(948 - start, 203))
	exp_bar.show()

	# Lists off the player's current inventory.
	info_header_underline = Line(Point(573 - start, 240), Point(937 - start, 240))
	info_header_underline.setWidth(1)
	info_header_underline.setOutline("white")
	info_header_underline.draw(gw)
	info_footer = Text(Point(573 - start, 246))
	info_footer.setAnchor("nw")
	info_footer.setSize(14)
	info_footer.setText(inventory())
	info_footer.draw(gw)

	
	# Lists off the pause menu options.
	choice_box = Rectangle(Point(start + 125, 165), Point(start + 370, 335))
	choice_box.setFill(color_rgb(50, 50, 50))
	choice_box.setWidth(3)
	choice_box.draw(gw)

	choice_text = Text(Point(start + 260, 250))
	choice_text.setAnchor("c")
	choice_text.setSize(20)
	choice_text.setText("Resume\nDrink Potion\nEat Apple\nSave Game\nQuit Game")
	choice_text.draw(gw)
	

	selector = Polygon(Point(start + 137, 183), Point(start + 137, 195), Point(start + 154, 189))
	selector.setFill("red")
	selector.draw(gw)

	selection = 0
	saved = False

	while True:
		
		while True:
			key = gw.checkKey().lower()

			if key != "":
				if key in ["space", "return"]:
					break

				elif key in ["escape"]:
					while selection > 0:
						selector.move(0, -30)
						selection -= 1


				if key in ["up", "w", "left", "a"]:
					selection = (selection - 1) % 5
					if selection != 4:
						selector.move(0, -30)
					else:
						selector.move(0, 120)


				elif key in ["down", "s", "right", "d"]:
					selection = (selection + 1) % 5
					if selection != 0:
						selector.move(0, 30)
					else:
						selector.move(0, -120)

		# Resume Game
		if selection == 0:
			for i in gw.items[prior:]: i.undraw()
			return

		# Drink Potion
		if selection == 1:
			if player.items["Potions"] == 0:
				dialogue("You have no more potions to drink.", right=right)
			elif player.current_HP == player.base_HP:
				dialogue("You are already at max HP", right=right)
			else:
				player.items["Potions"] -= 1
				player.current_HP += round(randint(4, 10) * 4.2)
				if player.current_HP > player.base_HP:
					player.current_HP = player.base_HP
				hp_bar.update(player.current_HP, player.base_HP)

		# Eat Apple
		if selection == 2:
			if player.items["Apples"] == 0:
				dialogue("You have no more apples to eat.", right=right)
			elif player.current_HP == player.base_HP:
				dialogue("You are already at max HP", right=right)
			else:
				player.items["Apples"] -= 1
				player.current_HP += randint(1, 4)
				if player.current_HP > player.base_HP:
					player.current_HP = player.base_HP
				hp_bar.update(player.current_HP, player.base_HP)

		# Save Game
		if selection == 3:
			saved = True
			save_state = open("save_state.txt", "w")  
			
			stats_to_save = [player.character_class, player.name, player.lvl, player.attack, player.defense, 
				player.current_HP, player.base_HP, player.current_SP, player.base_SP, player.current_EXP, player.next_EXP,
				player.gold, player.items, game_stats
			]

			line_to_save = ''
			for i in stats_to_save:
				line_to_save = line_to_save + str(i) + "\n"

			save_state.write(b64encode(line_to_save.encode("UTF-8")).decode("UTF-8"))
			save_state.close()

			dialogue("Game saved.", right=right)

		# Quit Game
		if selection == 4:

			if not saved:
				dialogue(f"You have not saved recently.")

			if dialogue("Are you sure you want to quit?", ["Yes", "No"], right=right) == 0:
				raise GameOver('Town Quit')

		info_footer.setText(inventory())


ROOT = Path(__file__).parent.absolute()
MAPS = ROOT / "maps"
MAP = MAPS / "map"
TILES = MAPS / "tiles"
SPRITES = MAPS / "sprites"
CHARACTERS = MAPS / "characters"
FOLDER = "forest"

player = None

game_stats = {
	'user': 'None',
	"town_tutorial": True,
	'shopbro': -1,
	'p_left': 0,
	"magic_weapon_status": 0,
	'fairies': -1,
	'inn_stays': -1,
	"librarian": 0,
	"level_tutorial": True,
	'reginald': -1,
	'rat_name': 'Fief',
	"floor_key": [False, False, False, False, False, False, False, False, 
				  False, False, False, False, False, False, False, False],
	"portals": [],
	'orc_dead': False
	}

found_items = {
	"Potions": 0, "Apples": 0, "Herbs": 0, "magic_item": 0, 
	"Fire Scroll": 0, "Thunder Scroll": 0, "Ice Scroll": 0}

load_overlay = Image(Point(500, 250), MAP / "load_overlay.png")
map_background = Image(Point(750, 250), MAP / "map_background.png")
# load_overlay = Image(Point(500, 250), MAP / "null_icon.png")

not_walkable = ['T', 'W', 'R', 'x']

teleport_chars = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", 'J', 'K', 'L', 'M', 
			'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
			'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

punctuation = ['space', '.', ',', "'", '"', '!', '?']

gw = GraphWin("Console Quest.py", 1000, 500)
gw.setBackground("black")

if __name__ == "__main__":

	gw.setBackground(color_rgb(100, 100, 100))

	# pause_menu(True)
	# dialogue("Green text.", ["That sounds pretty sus.", "What beady eyes you have!", "What gnarly teeth you have!"], "deep sky blue")
	# dialogue("This is supposed `to be a line of `dialogue that is not one, not two, but four lines long!", color = ['DeepSkyBlue2', 'SpringGreen', 'IndianRed'])
	# dialogue('start white `green text `white again', color=['white', 'green', 'white'])
	# dialogue("-------- max length -------- -------- max length --------", color='cyan')
	# print(dialogue("This is for testing the right-side dialogue box.", ["----", "Text", "More Text", "Something New", "Suuuuper Long Text", "Shorter Text", "Option 6"], right=True, return_arg=True))
	# gw.getKey()
	
	dialogue('What would you like to do?', choices=['Option 1', 'Option 2'], color='Yellow' )