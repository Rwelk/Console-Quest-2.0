# town.py
# The program here is for exploring the town, and, when ready, leaving for the forest.
# The glbl.player can visit the shop to buy a shiled and potions, the inn to heal up, and the Weapon Maker to make the upgraded weapon.
# They can also drink a potion in safety, 

from pathlib import Path
from PIL import Image as PIL_Image
from random import randint, random
from time import sleep

from map import exploring, save_and_close
import globals as glbl
from globals import dialogue
from graphics import Point, Rectangle, Text, Image, color_rgb
from level_creation_tool import fetch_level

from actor import Warrior

import pygame
from pygame import mixer


class Gold_Box:
	def __init__(self, gold):
		self.gold = gold
		self.line = f"You currently have: {self.gold}G"

		self.items = []
		self.items.append(Rectangle(Point(11, 11), Point(len(self.line) * 17 + 22, 50)))
		self.items[0].setFill(color_rgb(50, 50, 50))
		self.items[0].setWidth(3)

		
		self.items.append(Text(Point(22, 16), self.line))
		self.items[1].setAnchor("nw")
		self.items[1].setTextColor("yellow2")

	def show(self):	
		for i in self.items:
			i.draw(glbl.gw)

	def update(self, gold):
		sleep(.3)
		line = self.line
		self.gold = gold

		self.line = f"You currently have: {self.gold}G"
		if len(line) != len(self.line):
			self.items[0] = Rectangle(Point(11, 11), Point(len(self.line) * 17 + 22, 50))
			self.items[0].setFill(color_rgb(50, 50, 50))
			self.items[0].setWidth(3)

		self.items[1].setText(line)
		sleep(1)

	def hide(self):
		for i in self.items:
			i.undraw()


# This is the function that triggers when the glbl.player goes to the shop to buy stuff.
def shop(gold_box):

	color = "turquoise"
	gold_box.show()

	# The default price of potions. This changes if you meet and help the shopkeep's brother Daniel in the forest.
	pprice = 10

	# If the glbl.player succeeded the shopbro quest, they will see this special dialogue when they enter the shop.
	if glbl.game_stats['shopbro'] == 1 or glbl.game_stats['shopbro'] == 3:
		pprice = 7

		if glbl.game_stats['shopbro'] != 3:
			glbl.game_stats['shopbro'] = 3

			dialogue("Hey there! I heard you bumped into my brother in the forest.", [], color)
			dialogue("He might not be as awesome as me, but I still love the guy.", [], color)
			dialogue("I'll lower their price a little for you.", [], color)

	# However, if the glbl.player failed to save Daniel, the Shopkeep has this dialogue instead.
	elif glbl.game_stats['shopbro'] == 4:
		glbl.game_stats['shopbro'] = 5

		dialogue("Hey there. It's been a rough day.", [], color)
		dialogue("I just heard my brother Daniel was found dead in the forest.", [], color)
		dialogue("Since he was the one that made my potions, I don't have many left.", [], color)
		dialogue("I'll try to keep acting chipper though.", [], color)
		dialogue("Thanks for hearing me out.", [], color)


	# The shopkeep David introduces himself the first time the glbl.player comes to his shop.
	# glbl.game_stats["shopbro"] is used to keep track of if this is the first time the glbl.player has visited the shop.
	# There is more dialogue that plays for the first time the glbl.player leaves the shop, so it is updated there rather than here.
	if glbl.game_stats['shopbro'] == -1 or glbl.game_stats['shop_visits'] == 0:
		glbl.game_stats['shopbro'] = 0
		dialogue("Welcome to my shop!", [], color)
		dialogue("You must be that adventurer the town's been buzzing about.", [], color)
		dialogue("I'm the shopkeep, and town's best-looking dude. The name's David.", [], color)
		line = "What can I do for you?"

	# If the glbl.player has come before, David just gives this short line:
	else:
		line = "Welcome back to my shop! Is there anything you want?"


	
	glbl.game_stats['shop_visits'] += 1
		
	# Placing while loop to keep glbl.player in the menus until they want to leave.
	while True:

		x = dialogue(line, ["Buy", "Sell", "Leave"], color)

		# This part here is for buying stuff.  
		if x == 0:

			while True:
				
				x = dialogue("Here's what I have in stock.",[
					"Shield: 30G",
					f"Potions: {pprice}G{' ' + str(glbl.game_stats['p_left']) if glbl.game_stats['shopbro'] == 4 else ''}",
					"Information",
					"Back",
				], color)

				# Getting a shield.
				if x == 0:
					# The glbl.player doesn't have enough money
					if glbl.player.gold < 30: dialogue("You'll need more money for that.", [], color)
					# The glbl.player already has a shield in their inventory.
					elif glbl.player.items["Shield"] == 1:
						dialogue("Looks like you already have a mighty fine shield there.", [], color)
						dialogue("Whoever gave you it must've been a really handsome dude.", [], color)
					# The glbl.player buys a shield.
					else:
						glbl.player.gold -= 30
						gold_box.update(glbl.player.gold)
						glbl.player.items["shield"] = 1
						glbl.player.DEF += 3
						dialogue("Thanks for your purchase!", [], color)
						dialogue("DEF just rose by 3!")

				# Getting potions.
				elif x == 1:

					# The glbl.player failed the shopbro quest and the shop is out of stock.
					if glbl.game_stats['shopbro'] == 2 and glbl.game_stats['p_left'] == 0:
						dialogue("Sorry, I'm all out of potions.")

					# The glbl.player doesn't have enough money.
					elif glbl.player.gold < pprice: dialogue("You'll need more money for that.", [], color)
					
					# The glbl.player buys a potion.
					else:
						glbl.player.gold -= pprice
						gold_box.update(glbl.player.gold)		
						glbl.player.items["Potions"] += 1
						dialogue("Thanks for your purchase!", [], color)
						
						# If the glbl.player failed the shopbro quest, take away a potion from stock.
						if glbl.game_stats['shopbro'] == 2: glbl.game_stats['p_left'] -= 1

				# Getting information.
				elif x == 2:
					while True:

						x = dialogue("What do you wanna know about?", ["Shield", "Potions", "Fire Scrolls", "Ice Scrolls", "Thunder Scrolls", "Back"], color)

						if x == 0:
							dialogue("The shield will increase your your DEF some.", [], color)
						elif x == 1:
							dialogue("Potions will restore your HP by several points.", [], color)
						elif x == 2:
							dialogue("Fire Scrolls will burn up any trees.", [], color)
						elif x == 3:
							dialogue("Ice Scrolls will freeze bodies of water.", [], color)
						elif x == 4:
							dialogue("Thunder Scrolls will shatterer rocks.", [], color)
						# Return to the Buy Menu
						else:
							break

				# Return to the Buy/Sell Menu		
				else:
					break


		# The part for selling stuff.  
		# Note that the glbl.player cannot actually sell anything, since this is, you know, a shop.
		# As such, this area is completely for humor.
		elif x == 1:
			while True:

				line = []
				sell_amount = {
					"Shield": "15G", "Potions": "3G",
					"Fire Scroll": "5G", "Ice Scroll": "5G", "Thunder Scroll": "5G", 
					"Apples": "1G", "Herbs": "2G", "magic_item": "7G" 
				}

				for i in glbl.player.items:
					i_count = glbl.player.items[i]
					if i_count != 0:
						if i == "magic_item":
							item = "Magic Wood" if glbl.player.character_class == "Sorcerer" else "Magic Ore"
							line.append(f"{item} ({i_count}): {sell_amount[i]}")
						else: line.append(f"{i} ({i_count}): {sell_amount[i]}")
				line.append("Back")


				x = dialogue("What would you like to sell?", line, color, True)

				if x == "Shield":
					dialogue("That's a really nice shield you have there.") 
					if dialogue("Are you sure you want to get rid of it?", ["Yes", "No"]) == 0:	
						if dialogue("Are you really sure?", ["Yes", "No"]) == 0:
							if dialogue("I mean, it's a really nice shield, and there's no real reason to.", ["Yes", "No"]) == 0: 
								if dialogue("Your stats'll go down...", ["Just do it.", "No"]) == 0:
									if  dialogue("...and you don't really get much money back for it.", ["Sell my shield!", "No"]) == 0:
										if dialogue("I'm not sure I want to, with that tone of voice.", ["I'm sorry. Please?", "No"]) == 0:
											dialogue("Alright, since you're so sure.")
											dialogue("Just don't come crying to me if you die because you're DEF was so low you got hit a bunch of times.")
											dialogue("You want to return this shield?", [], color)
											dialogue("Sorry, but I don't take refunds.", [], color)

				elif x == "Potions":
					dialogue("Look man, don't take this personally, but I'm trying to run a business here.", [], color)
					dialogue("Why the heck would I buy some strange liquid from a rando adventurer I only met like, a few days ago?", [], color)
					dialogue("Also, I'm pretty sure at least some of this is my own stock.", [], color)

				elif x.find("Scroll") != -1:
					dialogue("Sorry, I already have plent of parchment.", [], color)

				elif x == "Apples":
					dialogue("TODO: Write Apple Stuff")
				
				elif x == "Herbs":
					dialogue("TODO: Write Herb Stuff")

				elif x == "Magic Ore" or x == "Magic Wood":
					dialogue(f"I have no use for magic items, but I think the {'Wizard' if glbl.player.character_class == 'Sorcerer' else 'Blacksmith'} might need it for a certain project she's been working on.", [], color)
				
				else:
					break


		# Let the glbl.player leave the shop.
		elif x == 2:
			break

		line = "Anything else?"

	
	gold_box.hide()
	dialogue("See you around!", [], color)

	# As mentioned above, this is the dialogue that play the first time the glbl.player leaves the shop.
	# It starts the Daniel questline, in which the glbl.player has to find the shopkeep's brother in the forest.
	if glbl.game_stats['shopbro'] == -1:
		glbl.game_stats['shopbro'] = 0
		dialogue("By the way, my brother Daniel has been missing for several days.", [], color)
		dialogue("He's actually the one who makes my potions.", [], color)
		dialogue("Every now and then he goes up the mountain to gather materials.", [], color)
		dialogue("It isn't uncommon for him to disappear for days at a time, but I just have a bad feeling.", [], color)
		dialogue("If you see him, tell him his more handsome brother's worried.", [], color)


# This is the code that plays when the glbl.player goes to the inn to sleep and heal.
# It also begins the fairy sidequest, as the glbl.player is unable to meet them before meeting the Innkeep.
def inn(gold_box):

	color = "SpringGreen"
	staying = False

	# This part plays when the glbl.player comes to the inn for the first time.
	if glbl.game_stats["inn_stays"] == -1:
		glbl.game_stats["inn_stays"] = 0
		dialogue("Welcome to my inn.", [], color)
		dialogue("You're the adventurer here to beat the orc, right?", [], color)
		dialogue("Would you like to stay the night?", [], color)
		dialogue("It'll cost 4G.", [], color)
		gold_box.show()
		x = dialogue("Staying the night will recover all your lost health.",  ["Yes (7G)", "No"])

	# This part plays every other time the glbl.player visits the inn.
	else:
		gold_box.show()
		x = dialogue("Welcome back! Here for the night again?", ["Yes (4G)", "No"], color)
	
	if x == 0:
		# If their health is already at max, they are reminded, just in case they don't want to waste 7G.
		if glbl.player.current_HP == glbl.player.base_HP:
			x = dialogue("Are you sure? Your HP is already at max.", ["Yes", "No"])
			if x == 1:
				dialogue("See you later!", [], color)
				gold_box.hide()
				return

		# Check to see if the glbl.player has enough money.
		if glbl.player.gold < 4:

			# If the glbl.player is short on cash, but has stayed at the inn seven other times, the fee is waved.
			# All remaining money is taken, but they can still heal up.
			if glbl.game_stats["inn_stays"] > 8:
				dialogue("You've been such a good customer, I'll waive the fee for tonight.", [], color)
				dialogue(" Just give me what you can, and I'll put the rest on your tab.", [], color)
				staying = True

			else:
				dialogue("You don't have enough money to stay right now.", [], color)

		else:
			staying = True


	# If the glbl.player has deicided to stay, or the Innkeep has allowed them to.
	if staying:
		glbl.game_stats["inn_stays"] += 1
		glbl.player.gold -= 4
		if glbl.player.gold < 0:
			glbl.player.gold = 0

		gold_box.update(glbl.player.gold)

		# This line for the final part of the Magic Weapon Quest.
		# The glbl.player has to go do something else to give the Weapon Maker some time to make the weapon.
		if glbl.game_stats["magic_weapon_status"] == 2: glbl.game_stats["magic_weapon_status"] = 3


		# Just a small touch, the glbl.player is directed to 1 of 4 rooms to sleep in.
		x = randint(1,4)
		if x == 1: dialogue("Your room is right down the hall, second on the left.", [], color)
		elif x == 2: dialogue(" Your room is up the stairs, third on the right.", [], color)
		elif x == 3: dialogue(" Your room is right down the hall, first on the right.", [], color)
		elif x == 4: dialogue(" Your room is up the stairs, third on the left.", [], color)


		# The HP is restored to max, and a short sleep cycle is played.
		glbl.player.current_HP = glbl.player.base_HP

		dialogue("Zzz...", [])
		dialogue("Zzzzz...", [])
		dialogue("Zzzzzzz...", [])
		dialogue("Health fully restored!", [])

	# If the glbl.player has not talked to the Innkeep about the fairies yet, this section will begin that sidequest for the thrid part of the game.
	if glbl.game_stats['fairies'] == -1 and glbl.game_stats["inn_stays"] > 1:
		glbl.game_stats['fairies'] = 0
		dialogue("As you're about to leave, the Innkeep waves you down.", [])
		dialogue(" You haven't heard of the mischievous fairies, have you?", [], color)
		dialogue(" My father used to tell me tales of how deep in the forest, he and his adventuring party discovered a cave with fairies in it.", [], color)
		dialogue(" When offered a brightly colored juice, some of them became stronger than ever before.", [], color)
		dialogue(" However, a couple others oddly turned weaker.", [], color)
		dialogue(" The other villagers always mocked him for that story, all the way to his grave.", [], color)
		dialogue(" It's always been a dream of mine to prove him right.", [], color)
		dialogue(" If you ever do see them, please tell me where they are.", [], color)
		dialogue(" Alright, see you later!", [], color)
		return
		
	dialogue("See you around!", [], color)
	gold_box.hide()
	return


# This is the code that plays when the glbl.player goes to their Weapon Maker to make a better weapon.
def weapon_maker(gold_box):

	color = 'magenta'

	# Based on the character's class, they might see the Blacksmith, or the Wizard.
	# Both has slightly different dialogue, so the changes are loaded in here.
	blacksmith = False if glbl.player.character_class == 'Sorcerer' else True
	cue = ["forge", "Ore", "3", "hammer out"] if blacksmith else ["shop", "Wood", "5", "carve up"]

	# Show the gold_box if the glbl.player is on either of the first two steps of this quest.
	if glbl.game_stats["magic_weapon_status"] < 2: gold_box.show()
	

	# This plays the first time the glbl.player meets the Weapon Maker.
	if glbl.game_stats["magic_weapon_status"] == 0:

		glbl.game_stats["magic_weapon_status"] = 1

		dialogue(f"Hello there! Welcome to my {cue[0]}.", [], color)
		dialogue("You must be that adventurer who's here to kill that orc.", [], color)
		dialogue(f"{glbl.player.name}, was it?", [], color)
		dialogue("I'm the one who makes the shields that the shop sells.", [], color)
		dialogue("I'm currently working on a project you might be able to help with.", [], color)

		# It's possible the glbl.player has already found magic items in the forest before meeting the Weapon Maker.
		# If so, this instance of dialogue will have a line that the glbl.player can say, with a response from the Weapon Maker.
		x = dialogue(f"In the forest you might come across some Magic {cue[1]}.", ["Like this?"] if glbl.player.items['magic_item'] > 0 else [], color)
		if x == 0:
			dialogue("Yes, that's it!", [], color)
		

		# The Sword and Daggers only need 3 Ore, while the Staff needs 5 Wood.
		dialogue(f"If you can gather up {cue[2]} of 'em and 25G, I'll be able to {cue[3]} a special weapon.", ["You can count on me!"], color)
		dialogue(f"Great! I'll see you later!", [], color)


	# When the glbl.player returns to the Weapon Maker, this dialogue plays.
	elif glbl.game_stats["magic_weapon_status"] == 1:

		x = dialogue("How's the search coming?", ["Got everything right here.", "Still searching."], color)
			
		# If they claim to have everything, the Weapon Maker checks.
		if x == 0:

			# In case the glbl.player is missing some ore and/or gold, she will tell them what they need.
			if (blacksmith and glbl.player.items[3][1] < 3) or ((not blacksmith) and glbl.player.items[3][1] < 5) or glbl.player.gold < 25:
				
				# The Weapon Maker's line starts out with the following text, and will be built from here.
				string = " Hold on, you're still missing "
				also = False

				# If the glbl.player is missing magic items, that is appended to "string".
				# Also, for proper grammar the boolean "also" is set to true.
				if blacksmith and glbl.player.items[3][1] < 3:
					string += f"{3 - glbl.player.items[3][1]} Ore"
					also = True
				elif (not blacksmith) and glbl.player.items[3][1] < 5:
					string += f"{5 - glbl.player.items[3][1]} Wood"
					also = True

				# If the above append triggered, and the glbl.player is also missing gold, append the word "and" to "string"
				if also == True and glbl.player.gold < 25: string += " and "

				# If the glbl.player is missing gold, append the amount to "string".
				if glbl.player.gold < 25: string += f"{25 - glbl.player.gold}G"

				# Finally, append a period for proper punctuation.
				string += "."

				# Now that the full line has been built, pass that in as the Weapon Maker's dialogue.
				dialogue(string, [], color)
				dialogue("Come back when you've gotten everything. I'm itching to get started!", [], color)


			# Else if everything is in order, the Weapon Maker will start making the weapon.
			else:
				glbl.game_stats["magic_weapon_status"] = 2
				if blacksmith: glbl.player.items[3][1] -= 3
				else: glbl.player.items[3][1]-= 5
				glbl.player.gold -= 25

				gold_box.update(glbl.player.gold)

				dialogue("Sweet! I'll get right to it.", [], color)
				dialogue("Come back a little later, and it should be done!", [], color)


		# Else the glbl.player tells the Weapon Maker they don't have everything, thereby leaving the area and returning to town.
		# The Weapon Maker will remind the glbl.player what they need.
		else:
			dialogue("Well then I'll leave you to it.", [], color)
			dialogue(f"Remember, you need {cue[2]} {cue[1]} and 25 G.", [], color)


	# The Weapon Maker needs time to make the weapon, and if not given it, this dialogue will play.
	# The glbl.player will have to either explore the forest once, or sleep off the night to get past this point.
	elif glbl.game_stats["magic_weapon_status"] == 2:
		dialogue("Hey there! Progress on your weapon is going good.", [], color)
		dialogue("Give me a little more time, and I should be finished.", [], color)
		dialogue("I can't wait for you to see it!", [], color)


	# Once the glbl.player has given the Weapon Maker time, they'll award the new weapon.
	elif glbl.game_stats["magic_weapon_status"] == 3:
		glbl.game_stats["magic_weapon_status"] = 4
		dialogue("Welcome back! I'm finally done!", [], color)
		weapon = "Storm Blade" if glbl.player.character_class == "Warrior" else "Blaze Rod" if glbl.player.character_class == "Sorcerer" else "Vorpal Daggers"
		dialogue(f"I present to you: the {weapon}!", [], color)
		dialogue("ATT rose by 7!")

		if glbl.player.character_class == "Warrior":
			dialogue("I imbued that sword with the power of thunder, so it should be able to break any rocks you come across!", [], color)
		elif glbl.player.character_class == "Wizard":
			dialogue("I imbued that staff with extra firepower, so it should be able to burn any trees you come across!", [], color)
		else:
			dialogue("I imbued those daggers with void magic, so you should be able to teleport across any bodies of water you come across!", [], color)
			
		# Explain how to use the weapon's special ability.
		# This should be slightly different depending on whether or not the glbl.player has finished the Librarian's sidequest.
		if glbl.game_stats["librarian"] > 2:
			dialogue(f"The {weapon} can be used in the forest the same way you use scrolls.")
		else: dialogue(f"To use the {weapon}'s special ability, press the [E] key in the field.")



		# Since the rogue recieves the Vorpal Daggers as a pair, gramatically the Weapon Maker should refer to "them" rather than "it".
		dialogue(f"Hope you like {'them' if glbl.player.character_class == 'Rogue' else 'it'}!", [], color)


	# If the glbl.player ever returns afterwards, this short dialogue plays.
	elif glbl.game_stats["magic_weapon_status"] == 4:
		dialogue("So, how's my magnum opus treating ya?", [], color)
		dialogue("I don't have anything else I can help you with, so get out there and beat that orc!", [], color)


	# If the glbl.player was shown the gold_box, hide it now.
	if glbl.game_stats["magic_weapon_status"] < 2:
		gold_box.hide()


def librarian(gold_box):

	color = 'DarkOrange'

	# This plays the first time the glbl.player meets the librarian.
	if glbl.game_stats["librarian"] == 0:
		dialogue("Oh. Hello...", [], color)
		dialogue("What brings you around here?", ["Just checking things out."], color)
		dialogue("Oh, that's cool...", [], color)
		dialogue("Wait, are you that new adventurer?", [], color)
		dialogue("I... need your help.", [], color)
		dialogue("As you may have heard... the other adventurers can't find the orc.", [], color)
		dialogue("I think it's because it moves around so much...", [], color)
		dialogue("So I thought, why not... map out the local area?", [], color)
		dialogue("That way, you guys won't get lost...", [], color)
		dialogue("I've been... asking all the adventurers to help me out.", [], color)
		x = dialogue("Will you help too...?", ["Eh, why not?", "Heck yeah!", "No thanks!"], color)

		if x == 2:
			glbl.game_stats["librarian"] = 1
			dialogue("Oh, okay then...", [], color)
			dialogue("Well, if you change your mind, I'm right here.", [], color)
		
		else:
			glbl.game_stats["librarian"] = 2
			dialogue("Wait, really? Thanks!", [], color)
			dialogue("Okay, so let's start by getting the first two areas...", [], color)
			dialogue("Sketch down wherever you find the stairs up.", [], color)
			dialogue("Then bring your maps back here...", [], color)
			dialogue("I'll grab your reward in the meantime.", [], color)
			dialogue("Okay, I'll see you later.", [], color)


	elif glbl.game_stats["librarian"] == 1:
		glbl.game_stats["librarian"] = 2
		dialogue("Oh, welcome back...", [], color)
		x = dialogue("Are you here to help now?", ["Fiiiiine", "Nope!"], color)

		if x == 1:
			dialogue("Are you just bullying me?", [], color)
			dialogue("If so, please stop it.", ["Sorry, sorry."], color)
			dialogue("Hmph.", [], color)

		dialogue("I want you to start with the first two areas of the forest.", [], color)
		dialogue("Make sure to write down where you found both pairs of stairs.", [], color)
		dialogue("Even though you've been really mean, I'll try to prepare some reward in the meantime.", [], color)
		dialogue("Okay, I'll see you later.", [], color)


	elif glbl.game_stats["librarian"] == 2:
		dialogue("Welcome back.", [], color)
		dialogue("How's it coming along?", ["Here you go."], color)

		if not (glbl.MAPS / "map_1.txt").exists():
			dialogue("Wait, you haven't even gone into the forest yet?", [], color)
			dialogue("Stop messing with me and at least do the bare minimum.", [], color)

		elif not (glbl.MAPS / "map_2.txt").exists():
			dialogue("You still haven't made it to the second floor?", [], color)
			dialogue("Come back after at least trying.", [], color)

		else:
			f1 = open(glbl.MAPS / "map_1.txt", "r")
			f2 = open(glbl.MAPS / "map_2.txt", "r")

			missing_1 = False
			if f1.read().count("|") < 1:
				missing_1 = True
				dialogue("You forgot to write down where the first stairs up are...", [], color)
			if f2.read().count("|") < 1:
				dialogue(f"You{' also' if missing_1 else ''} forgot to write down where the second set of stairs are...", [], color)
				dialogue("Do that then come back here.", [], color)

			if f1.read().count("|") < 1 or f2.read().count("|") < 1:
				glbl.game_stats["librarian"] = 3
				dialogue("This looks great...", [], color)
				dialogue("For your reward, I found these scrolls.", ["Scrolls?"], color)
				dialogue("Yeah. While exploring, sometimes trees and junk might block your path.", [], color)
				dialogue("You can use a scroll to clear them out of the way.", [], color)
				explain_scrolls()
				dialogue("If you ever need any more, come back here and I'll sell you some.", [], color)
				dialogue("Okay, good luck out there.", [], color)

				glbl.player.items['Fire Scroll'] += 1
				glbl.player.items['Ice Scroll'] += 1
				glbl.player.items['Thunder Scroll'] += 1
				
	elif glbl.game_stats["librarian"] > 2:
		if glbl.game_stats["librarian"] == 3:
			glbl.game_stats["librarian"] = 4
			dialogue("Welcome back...", [], color)
			dialogue("I forgot to mention this earlier, but if you're ever well and truly stuck, come back here.", [], color)
			dialogue("There's several paths up the mountain, and we can always start over from a new spot.", [], color)
			line = "Anyways, what can I help you with?"


		else:
			line = "Welcome back. What can I do?"

		gold_box.show()
		
		# Placing while loop to keep glbl.player in the menus until they want to leave.
		while True:

			x = dialogue(line, ["Buy Scrolls", "Start Over", "What scrolls do what?", "Leave"], color)

			# This part here is for buying srolls.  
			if x == 0:

				line = "Which one? They all cost 15G."

				while True:
					x = dialogue(line, ["Fire Scroll", "Ice Scroll", "Thunder Scroll", "Never mind."], color)
					if x != 3:
						if glbl.player.gold < 15: dialogue("That's not enough gold. These things are expensive, you know.", [], color)
						else:
							glbl.player.gold -= 15
							gold_box.update(glbl.player.gold)
							dialogue("Here you are.", [], color)
							if x == 0: glbl.player.items["Fire Scroll"] += 1
							elif x == 1: glbl.player.items["Ice Scroll"] += 1
							elif x == 2: glbl.player.items["Thunder Scroll"] += 1

					# Return to the Buy/Start Over/Explanation Menu		
					else:
						break

					line = "Any others?"


			# The part for Starting Over
			elif x == 1:
				if dialogue("Are you sure? This will reset all progress made while exploring, sending you back to Floor 1.", ["Yes", "No"]) == 0:
					x = dialogue("Okay, just hand me your old maps, and we can try to find a new spot to start.", ["Actually, never mind.", "Sure thing."], color)
					if x == 0:
						dialogue("Oh. Okay then.", [], color)
					else:
						for i in range(1, 16):
							try:
								(glbl.MAPS / f"floor_{i}.png").unlink()
								(glbl.MAPS / f"map_{i}.txt").unlink()
							except:
								pass

						dialogue("You hand over the maps and together look for a new starting location.")
						while True:
							dialogue("...")
							dialogue("...")
							dialogue("...!")
							dialogue("The Librarian points at a spot on the map you two were looking over.")
							if dialogue("Wait, what about here?", ["Looks good to me.", "'Bout as good as any other.", "Let's keep searching."], color) != 2:
								
								
								
								dialogue("Okay, I think an old adventurer already had something from here.", [], color)
								if random() < .5: dialogue("Here's a copy of her old map for you.", [], color)
								else: dialogue("Here's a copy of his old map for you.", [], color)
							
								level_layout, level_x, level_y = fetch_level(1, True)
								padding = level_layout.pop()
								level_layout = level_layout[1:]
								map_layout = []

								for i in range(len(level_layout)):
									row = level_layout[i]
									map_lower, map_upper = [], []
									for j in row:

										if j == "x":
											pass

										elif j == "|":
											map_lower.append("g")
											map_upper.append("|")
										elif j == "/":
											map_lower.append("g")
											map_upper.append("/")
										else:
											if j == ".":
												map_lower.append("g")
											elif j == "W":
												map_lower.append("b")
											elif j == "X":
												map_lower.append("o")
											elif j == "R":
												map_lower.append("y")
											map_upper.append(".")

									for j in range(15):
										map_lower.append(".")
										map_upper.append(".")
									
									map_layout.insert(i, map_lower)
									map_layout.append(map_upper)

								for i in range(15, 25):
									map_layout.insert(i, ["." for j in range(30)])
									map_layout.append(["." for j in range(30)])

								level_layout.insert(0, padding)
								level_layout.append(padding)
									
								save_and_close(1, level_layout, map_layout, len(glbl.gw.items))
								break
							
							
							
							else:
								dialogue("Okay then.", [], color)


			# Explain scrolls again.
			elif x == 2:
				explain_scrolls()

			# Let the glbl.player leave the library.
			else:
				break


			line = "Anything else?"

		
		gold_box.hide()
		dialogue("See you around!", [], color)


def explain_scrolls():

	dialogue("Press the [E] key to use a scroll.")
	dialogue("The Fire Scroll will burn up trees...", [], 'DarkOrange')
	dialogue("The Ice Scroll will freeze water...", [], 'DarkOrange')
	dialogue("And the Thunder Scroll will break rocks.", [], 'DarkOrange')
	dialogue("You can also use them in fights for massive damage.", [], 'DarkOrange')


def town_tutorial():
	dialogue("Welcome to the world of Console Quest!")
	dialogue("You work at the Adventurer's Guild in the city of Krocus.")
	dialogue("After gaining experience completing small quests, it's time your first major one.")
	dialogue("A small village in the backcountry has been forced to pay tributes to an orc for several years.")
	dialogue("It regulaly moves around, so others have had trouble finding and slaying it.")
	dialogue("Up until now, the villagers were able to keep the orc satisfied.")
	dialogue("But recently, it's been asking for ever larger tributes, and the villagers' pockets aren't deep.")
	dialogue("Find the orc, and kill him before he attacks and kills the townsfolk.")
	dialogue("You just arrived in town the other day, so many of the villagers only know rumors of you.")
	dialogue("Feel free to introduce yourself, or head straight into the forest to start your adventure!")


# There are certain random things and choices that the glbl.player is given before exploring the mountain.
# This method is called before the exploring() method in map.py to run those changes.
def prep_exploration():
	i = 0
	while True:
		try:
			i += 1
			x = Path(glbl.MAPS / f"level_{i}.txt").read_text().split("\n")
			

			background = PIL_Image.open(glbl.MAPS / f"level_{i}.png")
			flower = PIL_Image.open(glbl.MAPS / "sprites" / "harvest1.png")

			for j in range(50, len(x) - 1):
				line = list(x[j])

				for k in range(len(line)):

					if line[k] in ["B", "C", "D", "E"]:
						if randint(0, 2) == 0:
							line[k] = chr(ord(x[j][k]) - 1)
							if line[k] == "A":
								background.paste(flower, (k * 48, j * 48))

				x[j] = "".join(line)

			overworld_objects = x[-1].split()
			for i in range(len(1, overworld_objects), 2):
				if int(i) > 0:
					overworld_objects[i] = str(int(i) - 1)
			
			background.save(glbl.MAPS / f"level_{i}.png")

			file = open(glbl.MAPS / f"level_{i}.txt", "w")
			file.write("\n".join(x))
			file.close()
		except:
			break
	
	choices = []
	if (glbl.MAPS / "level_15.txt").exists():
		choices.append("Go to Floor 15")
	if (glbl.MAPS / "level_11.txt").exists():
		choices.append("Go to Floor 11")
	if (glbl.MAPS / "level_6.txt").exists():
		choices.append("Go to Floor 6")
		choices.append("Go to Floor 1")

	if choices:
		x = dialogue("Where would you like to go?", choices, return_arg=True, right=True)
		if x.count("15") > 0:
			exploring(15)
		elif x.count("11") > 0:
			exploring(11)
		elif x.count("6") > 0:
			exploring(6)
		else:
			exploring(1)
		
	else: exploring(1)


# This is the code called from play_game.py.
# It first does a quick check to see if the glbl.player has defeated the orc.
# It then lets the glbl.player explore the town and use any of the above functions.
# They can also explore the forest, drink potions, check their stats, and save and quit the game.
def town():

	prior = len(glbl.gw.items)


	gold_box = Gold_Box(glbl.player.gold)

	background = Image(Point(750, 250), glbl.MAPS / "sprites" / "village.png")
	background.draw(glbl.gw)

	#musicplays here
	#pygame.mixer.music.stop()
	
	if glbl.game_stats["town_tutorial"]:
		glbl.game_stats["town_tutorial"] = False
		town_tutorial()

	while True:
		pygame.mixer.music.stop()
		town_music = pygame.mixer.music.load("Town_Music.mp3")
		pygame.mixer.music.play(-1)
		if glbl.game_stats['orc_dead'] == "Dead":
			for i in glbl.gw.items[prior:]: i.undraw()
			return

		x = dialogue("Where would you like to go?", [
			"Inn", 
			"Wizard" if glbl.player.character_class == "Sorcerer" else "Blacksmith",
			"Shop",
			"Librarian",
			"Explore Forest"], right=True)

		if x == 0:
			pygame.mixer.music.stop()
			town_music = pygame.mixer.music.load("inn.mp3")
			pygame.mixer.music.play(-1)
			inn(gold_box)

		if x == 1:
			pygame.mixer.music.stop()
			shop_music = pygame.mixer.music.load("shop.mp3")
			pygame.mixer.music.play(-1)
			weapon_maker(gold_box)

		if x == 2:
			shop(gold_box)

		if x == 3:
			pygame.mixer.music.stop()
			librarian(gold_box)
		
		if x == 4:
			pygame.mixer.music.stop()
			town_music = pygame.mixer.music.load("Overworld_Music.mp3")
			pygame.mixer.music.play(-1)
			prep_exploration()
			if glbl.game_stats['reginald'] == 6:
				glbl.game_stats['reginald'] = 7
			if glbl.game_stats['reginald'] == 7:
				raise glbl.GameOver('Rat Invasion')
					



# The function for testing the town, to make sure everything works.
if __name__ == '__main__':

	glbl.player = Warrior()

	glbl.game_stats["librarian"] = 4
	glbl.game_stats["town_tutorial"] = False
	glbl.game_stats["level_tutorial"] = False
	glbl.game_stats["shopbro"] = 0
	glbl.game_stats['shop_visits'] = 0

	town()
	glbl.gw.getKey()