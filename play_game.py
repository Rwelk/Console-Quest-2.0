# play_game.py
# This is the file the glbl.player will call to play the game.

from ast import literal_eval
from base64 import b64decode
from pathlib import Path
from time import sleep

import globals as glbl
from globals import dialogue
from graphics import *
from town import town
from actor import Warrior, Sorcerer, Rogue


#possible music
import pygame
from pygame import mixer


def main():

	skip_menu = False

	while True:

		if not skip_menu:

			title = Text(Point(500, 125), """
             _____                                                                   
            |  _  |       ___   ___   _   _    ____   ___   _     ____        / \    
            | |_| |      /  _| | _ | |  \| |  |  __| | _ | | |   | ___|      / //    
            |_____|\     | |_  ||_|| | |\  |  _\ \   ||_|| | |_  | __|      / //     
                 \  \    \___| |___| |_| \_| |___/   |___| |___| |____|    / //      
                  \  \    --------------------------------------------    / //       
                   \  \        ___    _  _   ____    ____   _____        / //        
                    \  \      | _ |  | || | | ___|  |  __| |_   _|    __/_//         
                     \  \     ||_||_ | || | | __|   _\ \     | |     /___  \         
                      \  \    |____/ |____| |____| |___/     |_|      /\/\_|         
                       \  \    ----------------------------------    /\/             
                        \__\                                        /_/              """)
			title.setAnchor("c")
			title.setSize(10)
			title.draw(glbl.gw)


			# If the glbl.player has a previous save state, they have the option of loading it in to skip the introduction, glbl.player creation, and story.
			if Path('save_state.txt').exists():
				
				# By default load in the last saved game:
				load_game()

				# Everything for the Character Information
				info_box = Rectangle(Point(551, 100), Point(959, 400))
				info_box.setFill(color_rgb(50, 50, 50))
				info_box.setWidth(3)
				info_box.draw(glbl.gw)

				# The Character Icon
				info_icon = Image(Point(613, 163), glbl.MAPS / "characters" / f"{glbl.player.character_class}_portrait.png")
				info_icon.draw(glbl.gw)

				# Shows the Header that includes the glbl.player's name and level.
				info_header = Text(Point(572, 179))
				info_header.setAnchor("w")
				info_header.setSize(22)
				info_header.setText(f"      {glbl.player.name + f'LV: {glbl.player.lvl}'.rjust(16)[len(glbl.player.name):]}\n      HP:\n      EXP:\nItems:")
				info_header.draw(glbl.gw)

				# Draw the HP bar.
				hp_bar = glbl.Bar(glbl.player.current_HP, glbl.player.base_HP, "red", Point(750, 149), Point(948, 173))
				hp_bar.show()


				# Draws the EXP bar
				exp_bar = glbl.Bar(glbl.player.current_EXP, glbl.player.next_EXP, "green", Point(750, 179), Point(948, 203))
				exp_bar.show()

				# Lists off the glbl.player's current glbl.inventory.
				info_header_underline = Line(Point(573, 240), Point(937, 240))
				info_header_underline.setWidth(1)
				info_header_underline.setOutline("white")
				info_header_underline.draw(glbl.gw)
				info_footer = Text(Point(573, 246))
				info_footer.setAnchor("nw")
				info_footer.setSize(14)
				info_footer.setText(glbl.inventory())
				info_footer.draw(glbl.gw)

				hide_character = Rectangle(Point(498, -2), Point(1002, 502))
				hide_character.setFill('black')
				hide_character.setWidth(1)
				hide_character.draw(glbl.gw)
				title.lift()
				
				while True:
					menu_background = Rectangle(Point(15, 325), Point(485, 485))
					menu_background.setFill(color_rgb(50, 50, 50))
					menu_background.draw(glbl.gw)

					menu_text = Text(Point(60, 405), "")
					menu_text.setText("New Game\nLoad Game\nQuit")
					menu_text.setSize(28)
					menu_text.draw(glbl.gw)

					selector = Polygon(Point(30, 354), Point(30, 374), Point(50, 364))
					selector.setFill("red")
					selector.draw(glbl.gw)
					selection = 0

					while True:
						key = glbl.gw.checkKey().lower()

						if key != "":
							if key in ["space", "return"]:
								break

							elif key in ["up", "w"]:
								selection = (selection - 1) % 3
								if selection != 2:
									selector.move(0, -40)
								else:
									selector.move(0, 80)


							elif key in ["down", "s"]:
								selection = (selection + 1) % 3
								if selection != 0:
									selector.move(0, 40)
								else:
									selector.move(0, -80)

							if selection == 1:
								title.lower()						
								hide_character.lower(title)
							else:
								title.lift()
								hide_character.lower(title)


					for i in glbl.gw.items[1:]: i.undraw()

					# Start new game
					if selection == 0:
						# Because they already have a save file, and making a new one would would overwrite it, ask for certainty
						menu_background.draw(glbl.gw)
						certainty_text1 = Text(Point(30, 335), "Are you sure?\nThis may overwrite the old \nsave file!")
						certainty_text1.setAnchor('nw')
						certainty_text1.draw(glbl.gw)

						certainty_text2 = Text(Point(30, 464), "    Yes		No")
						certainty_text2.setAnchor('w')
						certainty_text2.draw(glbl.gw)

						certainty_selector = Polygon(Point(60, 454), Point(60, 474), Point(80, 464))
						certainty_selector.setFill("red")
						certainty_selector.draw(glbl.gw)
						certainty_selection = True

						while True:
							key = glbl.gw.checkKey().lower()

							if key != "":
								if key in ["space", "return"]:
									break

								elif key in ["up", "w", "left", "a", "down", "s", "right", "d"]:
									# The glbl.player was hovering over "Yes"
									if certainty_selection:
										certainty_selector.move(190, 0)
									# The glbl.player was hovering over "No"
									else:
										certainty_selector.move(-190, 0)
									certainty_selection = not certainty_selection



						if certainty_selection:
							glbl.gw.clear()
							new_game()
							break

					# Pretend to load the saved game.
					if selection == 1:
						pygame.mixer.music.stop()
						break

					# Quit out of the game
					if selection == 2:
						return


			# Else, the glbl.player is opening the game for the first time, and we need to go through glbl.player creation and story.
			else:
				pygame.mixer.music.stop()
				new_game()

		try:
			glbl.gw.clear()
			town()
		except glbl.GameOver as reason:
			color = 'red'

			if reason.type == 'Lost Battle':
				dialogue('You died!', color=color)
				dialogue('The villagers ran out of tributes for the orc.', color=color)
				dialogue("With no adventurers to protect them, the orc finally killed everybody.", color=color)
				if dialogue('Continue?', ['Yes', 'No'], color=color) == 0:
					load_game()
					skip_menu = True
				else: return

			elif reason.type == 'Rat Invasion':
				dialogue('Upon returning to the town, you notice all of the buildings have been damaged.', color=color)
				dialogue('All the villagers are dead, their corpses gnawed apart, while rats line the streets.', color=color)
				dialogue('Additionally, several rat corpses line the road.', color=color)
				dialogue('What possibly could have happened here?', color=color)
				dialogue("With no other options, you head back to the Adventurer's guild to report this failure.", color=color)
		
				if dialogue('Continue?', ['Yes', 'No'], color=color) == 0:
					load_game
					skip_menu = True
				else: return


			if reason.type == 'Orc Dead':
				goodbyes()
				hall_of_fame()
				final_message()
				return

			
			elif reason.type == 'Town Quit':
				return

			elif reason.type == 'Mountain Quit':
				return
				

		# except:
		# 	dialogue("Something has gone horribly wrong.")
		# 	dialogue("Luckily your game was able to be saved.")

	# Once the glbl.player has beaten the orc, town return the control back to here, to end the game.
	
def goodbyes():
	if glbl.player.current_HP < (glbl.player.base_HP / 4):
		dialogue("After a close battle, you've finally defeated the orc!")
	else:
		dialogue("At long last, the village is free from its enemy.")

	dialogue(" When you return with the news, you are showered with gratitude.")
	sleep(3)
	dialogue(" A big party is put on in your honor!")
	sleep(2)
	dialogue(" Afterwards, you fall asleep in the inn, perhaps for the last time.")
	sleep(3)
	dialogue("\n Z",end=""), sleep(.8), dialogue("z",end=""), sleep(.8), dialogue("z",end=""), sleep(.8), dialogue(".",end=""), sleep(.8), dialogue(".",end=""), sleep(.8), dialogue(".\n\n",end=""), sleep(1.2)
	dialogue(" Upon waking up, you decide to say some final goodbyes before leaving.\n")
	sleep(2.75)

	# The glbl.player is given the option to talk to some, all, or none of the important villagers they've met to say some final goodbyes.
	shopkeep = False
	innkeep = False
	weaponer = False
	w = glbl.game_stats['magic_weaponer']
	while True:
		if shopkeep == False: dialogue(" [S]hopkeep")
		else: dialogue(" [S]hopkeep", end="")

		if innkeep == False: dialogue("    [I]nnkeep")
		else: dialogue("    [I]nnkeep", end="")

		if weaponer == False: dialogue("    ["+w[0]+']'+w[1:])
		else: dialogue("    ["+w[0]+']'+w[1:], end="")

		dialogue("    [L]eave\n")
		x = input(' >>> ').lower()
		dialogue()


		if x=='s':
			if shopkeep == False:
				shopkeep = True
				dialogue(" Gotta say, you've been one fine customer, "+glbl.game_stats['p_name']+".\n")
				sleep(3)
				dialogue(" We'll all forever be in you're gratitude.\n")
				sleep(3)

				if glbl.game_stats['shopbro'] == 1 or glbl.game_stats['shopbro'] == 3:
					dialogue("\n Me especially, the handsomer brother.\n")
					sleep(2.75)
					dialogue(" We both know I'm more handsome.\n")
					sleep(2)
					dialogue(" No, I clearly am.\n")
					sleep(2)
					dialogue(" Nu uh!\n")
					sleep(1)
					dialogue(" Ya huh!\n")
					sleep(1)
					dialogue(" Nu uh!\n")
					sleep(1)
					dialogue(" Ya huh!\n")
					sleep(1)
					while True:
						dialogue(" Nu uh!\n")
						sleep(1)
						dialogue(' [G]uys!\n')
						x = input(' >>> ').lower()
						dialogue()
						if x=='g':
							break
						dialogue(" Ya huh!\n")
						sleep(1)
						dialogue(' [G]uys!\n')
						x = input(' >>> ').lower()
						dialogue()
						if x=='g':
							break
					dialogue(" Sorry.") 
				dialogue(" Thanks again for everything. Don't be a stranger!\n\n")
				sleep(4)

			else:
				dialogue(" You've already said your goodbyes to the Shopkeep.\n")
				sleep(1)


		elif x=='i':
			if innkeep == False:

				innkeep = True
				dialogue(" Thanks for everything, "+glbl.game_stats['p_name']+"!\n")
				sleep(2.5)
				dialogue(" Hey, did you ever find those fairies?\n")
				while True:
					dialogue(" [I] did!    [N]ope, never.\n")
					x = input(' >>> ').lower()
					dialogue()

					if x=='i':
						dialogue(" Really? I guess my dad really was telling the truth.\n")
						sleep(2)
						dialogue(" I've been thinking about going out on my own adventure to look for\n")
						dialogue(" them myself.\n")
						sleep(4.5)
						dialogue(" Now that I know they're out there, I want to see them with my own eyes.\n")
						sleep(4)
						break

					else:
						dialogue(" Well, I still hold out hope they're out there.\n")
						sleep(3)
						dialogue(" I've actually been preparing for my own excursion into the forest.\n")
						sleep(3)
						dialogue(" Now that the orc's gone, I want to try to find those fairies myself.\n")
						sleep(3)
						dialogue(" You've inspired me to go out and prove my father's tale was true.\n")
						sleep(3)

						break

				dialogue(" Anyways, if you ever find yourself in the neighborhood, let me put\n")
				dialogue(" you up for the night!\n\n")
				sleep(4)

			else:
				dialogue(" You've already said your goodbyes to the Innkeep.\n")
				sleep(1)


		elif x==w[0].lower():
			if weaponer == False:
				weaponer = True
				dialogue(" Welcome back, "+glbl.game_stats['p_name']+"!\n")
				sleep(2)
				dialogue(" Last night was some party, huh?\n")
				sleep(2)
				if glbl.game_stats['mwc'] == True:
					if glbl.game_stats['magic_weapon'] == "Vorpal Daggers": dialogue(" Listen, I've been thinking, and I think I have a theory on how to make\n those")
					else: dialogue(" Listen, I've been thinking, and I think I have a theory on how to make\n that")
					dialogue(" "+glbl.game_stats['magic_weapon']+" even better.\n")
					sleep(4.5)
					dialogue(" I'll need a lot more time to research about it, though.\n")
					sleep(3)
					dialogue(" Come back in a few years, and I know I'll have something good!\n\n")
					sleep(3)
				else:
					dialogue(" I'm still working on figuring out that new weapon.\n")
					sleep(3)
					dialogue(" If you ever find youself back here, drop on by.\n")
					sleep(3)
					dialogue(" It might finally be done then!\n\n")
					sleep(3)
				
			else:
				dialogue(" You've already said your goodbyes to the ", w, ".\n")
				sleep(1)


		else:
			if innkeep == False and shopkeep == False and weaponer == False:
				dialogue(" Deciding not to trouble the villagers any longer,", glbl.game_stats['p_name'], "suits up and")
				dialogue(" heads off for the next adventure!")
			else:
				dialogue(" Having said their final goodbyes, the villagers wave as", glbl.game_stats['p_name'], "heads on")
				dialogue(" to the next adventure!")
			
			break


def hall_of_fame():
	# When the glbl.player beats the game for the first time, a file titled "Hall of Fame.txt" is created that saves the character data.
	# All the stats as of the end of the orc battle, like potions and whatnot, are saved.
	# It is opened with 'a' so the previous wins are not overwritten.
	halloffame = open(glbl.ROOT / 'Hall of Fame.txt','a')


	while len(glbl.game_stats['p_name']) < 8:
		glbl.game_stats['p_name'] = glbl.game_stats['p_name']+" "

	y = "Lv. "+str(glbl.game_stats['p_LV'])
	while len(y)<6:
		y = " "+y

	z = glbl.game_stats['p_class']
	while len(z)<15:
		z = z+" "
		if len(z)<15:
			z = " "+z

	a = str(glbl.game_stats['current_exp'])+"/"+str(glbl.game_stats['next_level_exp'])
	while len(a) <5:
		a = " "+a
	b = str(glbl.game_stats['current_HP'])+"/"+str(glbl.game_stats['base_HP'])
	while len(b) <5:
		b = " "+b
	c = str(glbl.game_stats['p_DEF'])
	while len(c) <2:
		c = " "+c
	d = str(glbl.game_stats['potions'])
	if len(d) <2:
		d = " "+d
	e = str(glbl.game_stats['p_G'])
	if len(e) <2:
		e = " "+e
		
	if glbl.game_stats['magic_weapon'] == 'Damascus Sword': f =" Dam. Sword: "
	elif glbl.game_stats['magic_weapon'] == "Warlock Staff": f =" War. Staff: "
	else: f = " V. Daggers: "

	if glbl.game_stats['mwc'] == True: g = "X"
	else: g = "-"

	if glbl.game_stats['shield'] == True: h = "X"
	else: h = "-"

	if glbl.game_stats['rathat'] == True: i = "X"
	else: i = "-"

	if glbl.game_stats['shopbro'] == 1 or glbl.game_stats['shopbro'] == 3: j = "X"
	else: j = "-"

	if glbl.game_stats['fairies'] > 1: k = "X"
	else: k = "-"

	halloffame.write(
	"  _________________________________________________________\n"+
	" |                                                         |\n"+
	" |  "+glbl.game_stats['p_name']+" "+y+"    Inventory"+"         Side Quests       |"+
	"\n |  ---------------    --------------    ----------------- |"+
	"\n |  "+z+"    Potion:     "+d+"    Beat Reginald?  "+i+" |"+
	"\n |  EXP:      "+a+"    Gold:       "+e+"    Saved Daniel?   "+j+" |"+
	"\n |  HP:       "+b+"    "+str(glbl.game_stats['magic_item_type'])+":	    "+str(glbl.game_stats['magic_item'])+"    Found Fairies?  "+k+" |"+
	"\n |  ATT:         "+str(glbl.game_stats['ATT'])+"   "+f+" "+g+"                      |"+
	"\n |  DEF:         "+c+"    Shield:      "+h+"                      |"+
	"\n |_________________________________________________________|\n\n")

	glbl.game_stats['p_name'] = glbl.game_stats['p_name'].replace(" ", "")
	halloffame.close()

	# After everything, the old save file is deleted so the glbl.player can start a new game.
	# Since "Hall of Fame.txt" now exists, the glbl.player can skip the tutorial and go straight into character creation.
	try:
		os.remove(Path('save_state.txt'))

	except FileNotFoundError:
		pass


def final_message():
	# If this is the second, third, or nth time playing the game, this dialogue directly from me will play.
	if Path('Hall of Fame.txt').exists():
		dialogue("Hey, it's Jeffrey again!")
		dialogue(" I can't believe you cared so much that you'd play my game start to")
		dialogue(" finish again.")
		dialogue(" I don't really have anything special for you this time around.")
		dialogue(" Oh! How about this?")

		# Here, I give the glbl.player a gold star with the graphics library.
		p1 = Point(750, 32)
		p2 = Point(799, 183)
		p3 = Point(957, 183)
		p4 = Point(829, 278)
		p5 = Point(878, 427)
		p6 = Point(750, 333)
		p7 = Point(622, 427)
		p8 = Point(671, 278)
		p9 = Point(543, 183)
		p10 = Point(701, 183)

		star = Polygon(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
		star.setWidth(5)
		star.setFill('gold')
		star.draw(glbl.gw)
		
		dialogue("It's a gold star for your efforts!")
		dialogue("I hope it made this all worthwhile.")
		dialogue("...", speed=(1.5))
		dialogue("So... when I said to go out on your own adventure, I didn't mean to just start a new game.")
		dialogue("Go out and DO something.")
		dialogue("Personally, as a Boy Scout, I recommend camping.")
		dialogue("Get some friends to go with you, and it can be a great experience.")
		dialogue("What are you waiting for?")
		dialogue("The world is an oyster, and it's your job to crack it open!")
		sleep(5)


	# If this is the first time the glbl.player has beaten the game, this dialogue from me will play.
	else:
		dialogue(f" Thanks for playing this game, {glbl.game_stats['user']}.")
		dialogue(" I'm the creator, Jeffrey.")
		dialogue(" Making this game has been a real experience for me, and I'm so happy I got to share it with you.")
		dialogue(" This started out as a small project for one of my classes, and spiraled WAY out of control!")
		dialogue(" I just want to thank you for taking the time to play all of it.")
		dialogue(" If you want to dive into the code, I have a ton of comments that make up a running commentary of my experiences.")
		dialogue(f" Oh, and before I forget, in the folder this is contained in, there'll be a file that contains {glbl.game_stats['p_name']}'s stats after beating the orc.")
		dialogue("It's in 'Hall of Fame.txt'")
		dialogue(f"There, {glbl.game_stats['p_name']} will be immortalized, for as long as this file exists and you don't go changing it.")
		dialogue(" Anyways, this is truly good bye.")
		dialogue(" I hope you have a wonderful rest of the day, as you head on to you're own next adventure!")


def new_game():
	tutorial()
	character_select()
	glbl.game_stats = {
		"magic_weapon_status": 0,
		'reginald': -1,
		'rat_name': 'Fief',
		'shopbro': -1,
		'p_left': 0,
		'fairies': -1,
		'inn_stays': -1,
		'orc_dead': False,
		'user': 'None',
		"town_tutorial": True,
		"level_tutorial": True,
		"librarian": 0,
		"floor_key": [False, False, False, False, False, False, False, False,
					  False, False, False, False, False, False, False, False],
		"portals": []}

# The tutorial that introduces the glbl.player to the "system" and hold to play the game.
def tutorial():

	# If the glbl.player had a previous save state, or has completed the game, they have the option to skip the tutorial.
	if Path('Hall of Fame.txt').exists() or Path('save_state.txt').exists():
		if dialogue("Skip tutorial?", ["Yes", 'No']) == 0:
			return

	# Else, meet "System".
	dialogue("Hello! I am the game system.")
	dialogue("I'll be with you every step of the way as you play this game.\n")

	# Create the dialogue box
	name = dialogue('First, what is your name?', type_length=13)
	for i in glbl.punctuation + [' ']:
		if name.count(i):
			dialogue("Cheeky, ain't ya?")
			dialogue("I'll put you down as Charles.")
			name = 'Charles'
	else: glbl.game_stats['user'] = name
	dialogue(f"Hi there {name}!")
	dialogue("Use [W][A][S][D] or the arrow keys to change selections/dialogue options.")
	dialogue("Then, use [SPACEBAR] or [ENTER] to complete the selection.")
	dialogue("You can also at any time press the [M] key to open the menu.")
	line = "Got it?"
	

	# These loops are what allow the glbl.player to input their actions.
	# It accounts for both upper and lower case, and prevents the glbl.player from inputing an invalid action.
	# There are a few like this one in this document, so I will only explain how it works here.
	while True:
		if dialogue(line, ["Nope, not at all.", "Got it."]) == 1:
			dialogue(" Coolio.")
			break

		else:
			line = "Are you sure? Because you're doing it just fine right now."

	
	dialogue("Alright, let's get the game underway!")


# In this portion, the glbl.player chooses what class the want to play, as well as their names.
def character_select():
	
	prior = len(glbl.gw.items)
	
	# Create the dialogue box
	dialogue_box = Rectangle(Point(11, 403), Point(489, 488))
	dialogue_box.setFill(color_rgb(50, 50, 50))
	dialogue_box.setWidth(3)
	dialogue_box.draw(glbl.gw)

	# Create the Text object that will display dialogue.
	dialogue_text = Text(Point(25, 418), "")
	dialogue_text.setSize(20)
	dialogue_text.setAnchor("nw")
	dialogue_text.draw(glbl.gw)

	# If the array of choices that is passed in isn't empty, the glbl.player is supposed to make a
	#	 selection.
	p = (658, 250)

	character_chart_background = Rectangle(Point(533, 61), Point(928, 439))
	character_chart_background.setFill(color_rgb(50, 50, 50))
	character_chart_background.setWidth(3)
	character_chart_background.draw(glbl.gw)

	selector = Polygon(Point(p[0] - 95, p[1] - 125), Point(p[0] - 95, p[1] - 101), Point(p[0] - 61, p[1] - 113))
	selector.setFill("red")
	selector.draw(glbl.gw)

	warrior_portait = Image(Point(p[0], p[1] - 113), glbl.CHARACTERS / 'Warrior_portrait.png')
	warrior_portait.draw(glbl.gw)

	warrior_text_1 = Text(Point(p[0] + 58, p[1] - 113), "Warrior\nHP:       \nATT: Average\nDEF: Average")
	warrior_text_1.setSize(17)
	warrior_text_2 = warrior_text_1.clone()
	warrior_text_2.setText('\n    Higher\n\n')
	warrior_text_2.setTextColor('SpringGreen')
	warrior_text_1.draw(glbl.gw)
	warrior_text_2.draw(glbl.gw)

	sorcerer_portait = Image(Point(p[0], p[1]), glbl.CHARACTERS / 'Sorcerer_portrait.png')
	sorcerer_portait.draw(glbl.gw)

	sorcerer_text_1 = Text(Point(p[0] + 58, p[1]), "Sorcerer\nHP:\nATT:\nDEF:")
	sorcerer_text_1.setSize(17)
	warrior_text_2 = sorcerer_text_1.clone()
	warrior_text_2.setText('\n    Higher\n\n     Higher')
	warrior_text_2.setTextColor('SpringGreen')
	warrior_text_3 = sorcerer_text_1.clone()
	warrior_text_3.setText('\n\n     Lower\n')
	warrior_text_3.setTextColor('IndianRed')
	sorcerer_text_1.draw(glbl.gw)
	warrior_text_2.draw(glbl.gw)
	warrior_text_3.draw(glbl.gw)

	rogue_portait = Image(Point(p[0], p[1] + 113), glbl.CHARACTERS / 'Rogue_portrait.png')
	rogue_portait.draw(glbl.gw)

	rogue_text_1 = Text(Point(p[0] + 58, p[1] + 113), "Rogue\nHP:\nATT:\nDEF:")
	rogue_text_1.setSize(17)
	warrior_text_2 = rogue_text_1.clone()
	warrior_text_2.setText('\n\n     Higher\n')
	warrior_text_2.setTextColor('SpringGreen')
	warrior_text_3 = rogue_text_1.clone()
	warrior_text_3.setText('\n    Lower\n\n     Lower')
	warrior_text_3.setTextColor('IndianRed')
	rogue_text_1.draw(glbl.gw)
	warrior_text_2.draw(glbl.gw)
	warrior_text_3.draw(glbl.gw)
	
	selection = 0
	options = ['Warrior', 'Sorcerer', 'Rogue']

	while True:
		
		dialogue_text.setText('')
		skip = False
		for i in 'What class would you like to \nplay?':

			key = glbl.gw.checkKey().lower()
			if key in ["return", "space", "escape"]:
				skip = True

			dialogue_text.setText(dialogue_text.getText() + i)

			if not skip:
				sleep(.02)
			
		while True:
			key = glbl.gw.checkKey().lower()

			if key != "":
				if key in ["space", "return"]:

					if dialogue(f'Are you sure you want to play as a {options[selection]}?', ['Yes', 'No']) == 0:
						break

				elif key in ["escape"]:
					while selection > 0:
						selector.move(0, -113)
						selection -= 1

				if key in ["up", "w", "left", "a"]:
					selection = (selection - 1) % 3
					if selection != 2:
						selector.move(0, -113)
					else:
						selector.move(0, 226)


				elif key in ["down", "s", "right", "d"]:
					selection = (selection + 1) % 3
					if selection != 0:
						selector.move(0, 113)
					else:
						selector.move(0, -226)

		name = dialogue(f"What is the {options[selection]}'s name?", type_length=8)
		if name in ['', ' ', '  ', '   ', '    ', '     ', '      ', '       ', '        ']:
			if selection == 0: name = 'Grog'
			elif selection == 1: name = 'Magnus'
			else: name = 'Fief'

		if dialogue(f"You're certain you want to play as `{name} the {options[selection]}`?", ['Yes', 'No'], ['white', 'SpringGreen', 'white']) == 0:
			break

	if selection == 0:
		glbl.player = Warrior(name=name)
	elif selection == 1:
		glbl.player = Sorcerer(name=name)
	else:
		glbl.player = Rogue(name=name)

	glbl.gw.clear(prior)


def load_game():

	file = open("save_state.txt", 'r')
	content = file.readline()
	file.close()


	decoded_contents = b64decode(content.encode("UTF-8")).decode("UTF-8").split('\n')
	for i in range(2, 12): decoded_contents[i] = int(decoded_contents[i])

	character_class = decoded_contents[0]
	character_stats = decoded_contents[1:12]
	character_stats.append(literal_eval(decoded_contents[12]))
	glbl.game_stats = literal_eval(decoded_contents[13])

	if character_class == 'Warrior':
		glbl.player = Warrior(*character_stats)
	elif character_class == 'Sorcerer':
		glbl.player = Sorcerer(*character_stats)
	elif character_class == 'Rogue':
		glbl.player = Rogue(*character_stats)
	else:
		dialogue('Wuh oh, looks like your save file got corrupted.')


if __name__ == "__main__":
	# try:
	# 	main()
	# except:
	# 	save_state = open("save_state.txt", "w")  
			
	# 	stats_to_save = [glbl.player.character_class, glbl.player.name, glbl.player.lvl, glbl.player.attack, glbl.player.defense, 
	# 		glbl.player.current_HP, glbl.player.base_HP, glbl.player.current_SP, glbl.player.base_SP, glbl.player.current_EXP, glbl.player.next_EXP,
	# 		glbl.player.gold, glbl.player.items, glbl.game_stats
	# 	]

	# 	line_to_save = ''
	# 	for i in stats_to_save:
	# 		line_to_save = line_to_save + str(i) + "\n"

	# 	save_state.write(base64.b64encode(line_to_save.encode("UTF-8")).decode("UTF-8"))
	# 	save_state.close()

	# 	dialogue("Wuh-oh, something went horribly wrong!")
	# 	dialogue("I saved your game for you before everything crashed, so it should be all good.")

	main()