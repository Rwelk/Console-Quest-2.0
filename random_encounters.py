# random_encounters.py
# This is where the different random encounters the glbl.player can find in the forest are stored.
# It also contains exploring(glbl.game_stats)

import globals as glbl
from globals import dialogue

# The "Rat with Hat"event is the first of 3 one time encounters, and happens in phase 1.
# The glbl.player meets Reginald the Rat, the leader of a swarm of monsters.
def rat_w_hat():

	# This plays if this is the first time the glbl.player has met Reginald.
	if glbl.game_stats['reginald'] == 1:

		glbl.game_stats['reginald'] = 2
		dialogue('You notice a rat wearing a top hat and a monocle.')
		dialogue('It also seems to be holding a cane in its tail.')

		# I like to imagine Reginald has a British accent here.
		if dialogue("Pip pip cheerio old chap! Wonderful weather we have this noon, wouldn't you say?", ["Yes", "No"], "red") == 1:
			dialogue("Ah, you're a glass half empty type of fellow, I see.", color="red")

		name = dialogue("If I may ask, good sir, what is your name?", [glbl.player.name, 'Ratt Slayir', 'Dave'], "red", True)
		glbl.game_stats["rat_name"] = name

		# If the glbl.player gives the first fake name:
		if name == 'Ratt Slayir':
			dialogue("The rat visibly sudders.")
			dialogue('Ratt Slayir? Tis an, uh, "interesting"name.', color='red')

		# If the glbl.player gives the other fake name:
		elif name == 'Dave':
			dialogue("""Huh. I've never had the pleasure of meeting a "Dave"before.""", color="red")

		# If the glbl.player gives their real name:
		else:
			dialogue(f"{name}, eh? That's a splendid name.", color='red')

		
		# Here the glbl.player learns Reginald's name, and gets an inkling of his nefarious goals.
		dialogue('Well, my friends call me Reginald.', color="red")
		dialogue("Say, you wouldn't happen to know where the nearest town is, would you?", color="red")
		dialogue("Reginald twirls his(?) cane and smiles menacingly.")

		# If the glbl.player selects this, they are eventually taken to the battle with Reginald.
		if dialogue("""I need a place to feed- er, "rest", after my strenuous travels.""", ["Aren't you a talking rat?", "Yeah, follow me."], "red") == 0:
			dialogue('No, no, I am most definitely a human.', color='red')
			dialogue("Reginald's tail flicks around.", ['You look like a rat.'])
			dialogue(f"Now that's quite a rude thing to say, {name}. I've always been rather sensitive about my appearance.", color='red')
			dialogue("The hat droops a little.", ["What pointy ears you have!"])
			dialogue("The better to hear you with.", ['What beady eyes you have!'], 'red')
			dialogue("The better to see you with.", ['What gnarly teeth you have!'], 'red')
			dialogue("The better to... bah! Forget it!", color='red')
			dialogue("Saw through my ingenious disguise, eh?", color='red')
			dialogue("Well, you're not leaving here alive! Muahaha!", color='red')
			dialogue("Reginald brandishes the cane.")
			return 'fight'


	if glbl.game_stats['reginald'] == 5:
		glbl.game_stats['reginald'] = 6
		dialogue('Thank you kindly for taking me all the way here.', color='red')
		dialogue("I'm going to rest for a little bit before heading on.", color='red')
		dialogue('Must uh... look presentable for the villagers, right?', color='red')
		dialogue(f'I do hope we have the chance to run into each other again some day, {glbl.game_stats["rat_name"]}.', color='red')
		dialogue("I bid you adieu.", color='red')


	# This dialogue plays when the glbl.player has selected for Reginald to follow them.
	# It lets them change their mind and fight Reginald anyways before reaching the town.	
	else:
		dialogue("Reginald darts his eyes around nervously.")
		x = dialogue("Is something the matter?", ['Stay here.' if glbl.game_stats['reginald'] == 2 else 'Follow me.', "I don't trust you.", 'Nevermind.'], 'red', return_arg=True)
		if x.count('Stay') > 0:
			glbl.game_stats['reginald'] = 3
			return 'stay'
		elif x.count('Follow') > 0:
			glbl.game_stats['reginald'] = 2
			return 'follow'
		
		if x.count('I') > 0:
			if dialogue("What ever could you mean? I've been nothing if not trustworthy!", ["Sounds pretty sus.", 'Forget about it.'], 'red') == 0:
				dialogue("I swear I'm not... bah! Forget it!", color='red')
				dialogue("Saw through my ingenious disguise, eh?", color='red')
				dialogue("I've been a rat all along and you didn't even know!", color='red')
				dialogue("I'll just find another fool to take me to the village.", color='red')
				dialogue("En guarde!")
				return 'fight'



# The shopbro event occurs in the 2nd phase of the game.
# It gives the glbl.player the chance to save the Shopkeep's brother, Daniel.
# If they fail it, the Shopkeep will only have 4 potions left in stock before his supply runs out.
# The only other way to get potions is through the Caravan event.
# If they do succeed, however, the Shopkeep's potions are forever discounted.
def shopbro():

	color = 'deepskyblue'
	
	# The first time talking with Daniel.
	if glbl.game_stats['shopbro'] == 1:

		dialogue("As you walk through the forest, you notice a handsome man riddled with arrows.")
		dialogue("Beside his pool of blood is a large basket with a few plant leaves.")
		x = dialogue("Good day... fellow traveler. What brings you out here?", ["Just out for a stroll.", "I'm looking for the Orc.", "Nunya business."], color=color)
		if x == 0:
			dialogue("Well you chose quite the day to come out.", color=color)

		elif x == 1:
			dialogue("You're the new adventurer, eh? Thank goodness.", color=color)

		elif x == 2:
			dialogue("Well then. Little rude of you.", color=color) 


		x = dialogue("Hey, you wouldn't happen to have something to fix all of... this, would you?", ['What can I do to help?', 'Sorry, I have things to do.'], color)
		if x == 1:
			glbl.game_stats['shopbro'] = 4
			dialogue("Oh, I guess we all have our troubles.", color=color)
			dialogue("Sorry to take up your time.", color=color)
			dialogue("You walk away from the dying man, ignoring the tears rolling down his face.")
			return

		dialogue("Oh, I dunno, if you had a couple spare potions, that'd be pretty nifty.", color=color)

		options = ['Fresh out.', 'No, these are mine.']
		if glbl.player.items['Potions'] > 0:
			options.insert(0, 'Sorry, I only have 1.')
		if glbl.player.items['Potions'] > 1:
			options.insert(0, 'Yeah, take these.')
			

		x = dialogue(f'You have {glbl.player.items["Potions"]} Potions.', options, return_arg=True)
		if x.count('Yeah') > 0:
			glbl.game_stats['shopbro'] = 3
			glbl.player.items['Potions'] -= 2

			dialogue('Thank you so much friend!', color=color)
			dialogue('The stranger immediately drinks one of the potions.', color=color)
			dialogue("It'll take me a while to get all my strength back in between removing these arrows.", color=color)
			dialogue("Meet me at the shop when you get back to town.", color=color)
			dialogue("I'll see you then!", color=color)


		elif x.count('Sorry') > 0:
			dialogue("No... don't apologize yet!", color=color)
			dialogue("If I drink that now, it should... keep me stable for a little while.", color=color)
			dialogue("In the meantime, you can try... to find the other one from somewhere.", color=color)
			y = dialogue('What do you say? Willing to... do this random stranger a massive solid?', ['Here you go.', 'Mmmm, nah.'], color)

			if y == 0:
				glbl.game_stats['shopbro'] = 2
				glbl.player.items['Potions'] -= 1
				dialogue('You hand over the potion, and the man drinks it in a flash.')
				dialogue("Oooh, I'm feeling better already.", color=color)
				dialogue("Good luck. I'll just... chill here for now.", color=color)

			else:
				glbl.game_stats['shopbro'] = 4
				dialogue('The man looks flabergasted.')
				dialogue("Oh. Um, okay then.", color=color)
				dialogue("Well... didn't think my last moments... would be with such a jerk.", color=color)
				dialogue("Hope and life literally drain out of the man's eyes as he slumps over dead.")


		else:
			glbl.game_stats['shopbro'] = 4
			
			if x.count('Fresh') > 0:
				dialogue("The hope that had touched the man's face as you arrived just as quickly drains away.")
				dialogue("Well, that's a real pickle, huh.", color=color)
				dialogue("Can you at least stay here... so I don't die alone?", ['Of course.'], color=color)
				dialogue("Once the man draws his last breath, you continue somberly on your way.")

			else:
				dialogue("The man sticks up his middle finger in your general direction.")
				dialogue("Some help you turned out to be ya selfish jerk.", color=color)
				dialogue("The stranger then slumps over dead.")



	elif glbl.game_stats['shopbro'] == 2:
		dialogue("Oh hey, welcome back.", color=color)
		options = ["Still searching."]
		if glbl.player.items['Potions'] > 0: options.insert(0, 'Here you go.')

		x = dialogue("Do you... have that extra potion I need?", options, color, True)
		if x.count('Here') > 0:
			glbl.game_stats['shopbro'] = 3
			glbl.player.items['Potions'] -= 1

			dialogue('Thank you so much, stranger.', color=color)
			dialogue("It'll take me a while to get all... my strength back in between removing these arrows.", color=color)
			dialogue("Meet me at the shop when you get back to town.", color=color)
			dialogue("I'll see you then!", color=color)

		else:
			dialogue('Well I wish you luck, but try to be quick.', color=color)
			dialogue('I can already feel that first potion losing its effects.', color=color)




	elif glbl.game_stats['shopbro'] == 3:
		dialogue("Oh hey, welcome back.", color=color)
		if dialogue("The name's Daniel, by the way.", [f"My name's {glbl.player.name}.", "Say Nothing"], color) == 0:	
			dialogue(f"Well, it was nice meeting you, {glbl.player.name}.", color=color)
		dialogue("I should be fine here on my own. I'll see you back at the village!", color=color)
		dialogue("You leave Daniel in high spirits.", color=color)



# The "Magic Item" event lets the glbl.player find a Magic Ore for the Blacksmith sidequest or Magic Wood for the Sage sidequest.
# It is also used as currency for the fairies to run their glbl.game_stats roulette.
def magic_item():

	
	print("Next to the path, you notice something glimmering in the sunlight.")
	sleep(3)
	print("It appears to be Magic ", glbl.game_stats['magic_item_type'], ".", sep="")
	sleep(1.5)

	if glbl.game_stats['quest'] == 1:
		print("This must be what the", glbl.game_stats['magic_weaponer'], "was talking about!")
		sleep(2)
	elif glbl.game_stats['fairies'] == 2:
		print("The fairies wanted it for their potions.")
		sleep(1.25)
	else:
		print("It might have some importance later.")
		sleep(1.25)

	glbl.game_stats['magic_item'] += 1
	print("You gained 1 Magic ", glbl.game_stats['magic_item_type'], ".", sep="")
	sleep(1.5)

	return glbl.game_stats


# The Fairy Fountain Event happens in Phase 3 of the game.
# In it, the glbl.player has the option of trading their excess magical resources for a chance to raise their stats.
# However, fairies are mischeivous, and have a 1:4 chance of lowering the glbl.game_stats as well.
# At least the glbl.player can choose which glbl.game_stats they want to wager, right?
# This one was the most difficult to plot out, as you have to first hear about the Fountain from the Inn, then find it in the forest.
# After that, I wanted the glbl.player to be able to come back at any time while exploring the forest.
# However, the glbl.player can decline to drink the first offered potion, so I had to come up with a way that would let them redrink it, if they wanted.
# The way the exploration system is set up, I had to also have a complete(glbl.game_stats) message if they ever stumbled back onto in when exploring the forest.
# And all this is stupidly done through 1 variable, because I felt that the dictionary was getting too long.
# That's basically how everything else in the game happened though: I'd start off with a medium sized item, then get ideas and expand it.
# 5 hours later, I'd finally be done coding all the odds and ends I thought the game needed.
# Anyways, rant over. On to the code.
def fairies():

	# This part is for when the glbl.player has found the Fountain for the first time.
	if glbl.game_stats['fairies'] == 1:
		os.system('clear')

		print("A gentle song fills your ears from a nearby cave.")
		sleep(2.5)
		print("Following it, you find a fountain with several fairies.")
		sleep(2.5)
		print("One of them flitters up to you, speaking quickly:")
		sleep(2.5)
		print_magenta("Hi welcome to our fountain wanna drink?!")
		sleep(2)

		print("The fairy proffers up a small bowl with blue liquid.")
		while True:
			print_yellow("[D]rink    [B]ad idea.")
			x = input(' >>> ').lower()
			print()
			if x!='d' and x!='b':
				invalid()

			# If the glbl.player decides not to drink the Kool Aid:	
			elif x=='b':
				glbl.game_stats['fairies'] = 2
				print("In a wise decision, you decide not to drink the sketchy juice given")
				print("to you by some hyperactive rando you just met in the woods.")
				sleep(4.5)
				return

			# Else if they do:
			elif x=='d':
				glbl.game_stats['fairies'] = 3
				print("Readying yourself, you gulp it down in one swig.")
				sleep(2)
				print("Suddenly, your body feels as though it is on fire!")
				sleep(2.25)
				print(".",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!"), sleep(1)
				
				# Here, you can see the gambling at work.
				# I chose DEF to be the glbl.game_stats effect the first time, since there are the least consequences if the glbl.player looses it.
				# As previously mentioned, there 3:1 chance of gaining:losing stats.
				# Overall, I'd say it's still worth the risk.
				if random.randint(0,3)==0:
					t = random.randint(3,5)
					glbl.game_stats['p_DEF'] -= t
					print_white("Your DEF just "), print_red("dropped by "+str(t)+"!")
					sleep(1.5)
					break
				else:
					if random.randint(1,3) == 3: t = 2
					else: t = 1
					glbl.game_stats['p_DEF'] += t
					print_white("Your DEF just "), print_green("rose by "+str(t)+"!")
					sleep(1.5)
					break

		print_magenta("We have more if you want!")
		sleep(1.5)
		print_magenta("Enough for all stats!")
		sleep(2)
		print_magenta("Just bring magic stuff!")
		sleep(1.5)
		print_magenta("Okay bye now.")
		sleep(1)
		glbl.game_stats['fairies'] == 3


	# This section plays when the glbl.player returns to the Fountain via the exploration menu having not yet drunk their first potion.
	elif glbl.game_stats['fairies'] == 2:

		os.system('clear')
		print("The fairy from before comes up, holding the same strange blue liquid.")
		sleep(2.75)

		print_magenta("Oh you came back wanna drink now?!")
		sleep(1.5)
		while True:
			print_yellow("[D]rink    [S]till a bad idea.")
			x = input(' >>> ').lower()
			print()
			if x!='d' and x!='s' :
				invalid()

			# The glbl.player can still deny drinking the potion. If they ever come back, it'll just loop throught this part again.
			elif x=='s':
				glbl.game_stats['fairies'] = 2
				print("You decide that taking drugs'd be a bad call.")
				sleep(1.5)
				print_magenta("Okay well see you later!")
				sleep(1.5)
				return

			# Once they finally do drink, though, thee glbl.player can finally progress through this... sidequest?
			elif x=='d':
				glbl.game_stats['fairies'] = 3
				print("Readying yourself, you gulp it in one swig.")
				sleep(2)
				print("Suddenly, your body feels as though it is on fire!")
				sleep(2.25)
				print(".",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!"), sleep(1)
				if random.randint(0,3)==0:
					t = random.randint(3,5)
					glbl.game_stats['p_DEF'] -= t
					print_white("Your DEF just "), print_red("dropped by "+str(t)+"!")
					sleep(1.5)
					break
				else:
					if random.randint(1,3) == 3: t = 2
					else: t = 1
					glbl.game_stats['p_DEF'] += t
					print_white("Your DEF just "), print_green("rose by "+str(t)+"!")
					sleep(1.5)
					break

		print_magenta("We have more if you want!")
		sleep(1.5)
		print_magenta("Enough for all stats!")
		sleep(2)
		print_magenta("Just bring magic stuff!")
		sleep(1.5)
		print_magenta("Okay bye now.")
		sleep(1)
		glbl.game_stats['fairies'] == 3

	# And this is the part for when the glbl.player has finally caved. At this point, they can wager any of their stats.
	# The random level up chance is rarer, as the benefits are more beneficial.
	elif glbl.game_stats['fairies'] == 3:
		os.system('clear')

		print_magenta("Welcome back wadaya want?!")
		while True:

			print_white("You currently have: "), print_green(str(glbl.game_stats['magic_item'])+""+ glbl.game_stats['magic_item_type'])
			print()
			print_yellow("[A]TT Juice    [D]EF Juice    [H]P Juice    [L]evel Juice    [N]one")
			y = input(">>> ").lower()
			print()
			if y!='l' and y!='h' and y!='a' and y!='d' and y!='n':
				invalid()

			# This part is for if the glbl.player wants to raise only their ATT glbl.game_stats.
			# It mirrors the DEF raising section below.
			elif y=='a':
				print("The fairy hands you a red liquid.")
				sleep(1.75)
				print("Are you sure you want to drink it?")
				while True:
					print_yellow("[Y]es    [N]o")
					u = input(">>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()
					elif u=='n':
						print("You hand back the liquid.")
						sleep(1)
						break
					elif u=='y':
						glbl.game_stats['magic_item'] -= 1
						print("After readying yourself, you take a large gulp.")
						sleep(2)
						print("The familiar fire burns within your body.")
						sleep(2.25)
						print(".",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!"), sleep(1)
						if random.randint(0,3)==0:
							t = random.randint(3,5)
							glbl.game_stats['ATT'] -= t
							print_white("Your ATT just"), print_red("dropped by "+str(t)+"!")
							sleep(1.5)
						else:
							if random.randint(1,3) == 3: t = 2
							else: t = 1
							glbl.game_stats['ATT'] += t
							print_white("Your ATT just"), print_green("rose by "+str(t)+"!")
							sleep(1.5)
						print()
						break

			# This part is for if the glbl.player wants to raise only their DEF glbl.game_stats.
			# It mirrors the ATT raising section above.
			elif y=='d':
				print("The fairy hands you a blue liquid.")
				sleep(1.75)
				print("Are you sure you want to drink it?")
				while True:
					print_yellow("[Y]es    [N]o")
					u = input(">>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()
					elif u=='n':
						print("You hand back the liquid.")
						sleep(1)
						break
					elif u=='y':
						glbl.game_stats['magic_item'] -= 1
						print("After readying yourself, you take a large gulp.")
						sleep(2)
						print("The familiar fire burns within your body.")
						sleep(2.25)
						print(".",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!"), sleep(1)
						if random.randint(0,3)==0:
							t = random.randint(3,5)
							glbl.game_stats['p_DEF'] -= t
							print_white("Your DEF just"), print_red("dropped by "+str(t)+"!")
							sleep(1.5)
						else:
							if random.randint(1,3) == 3: t = 2
							else: t = 1
							print_white("Your DEF just"), print_green("rose by "+str(t)+"!")
							sleep(1.5)
						print()
						break

			# This part is for if the glbl.player wants to raise only their HP.
			# It works like a potion in that it raises both the base and the current the same amount at the same time.
			# Or lowers, if the glbl.player has bad luck.
			elif y=='h':
				print("The fairy hands you a green liquid.")
				sleep(1.75)

				print("Are you sure you want to drink it?")
				while True:
					print_yellow("[Y]es    [N]o")
					u = input(">>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()
					elif u=='n':
						print("You hand back the liquid.")
						sleep(1)
						break
					elif u=='y':
						glbl.game_stats['magic_item'] -= 1
						print("After readying yourself, you take a large gulp.")
						sleep(2)
						print("The familiar fire burns within your body.")
						sleep(2.25)
						print(".",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!"), sleep(1)
						if random.randint(0,3)==0:
							t = random.randint(6,10)
							glbl.game_stats['current_HP'] -= t
							glbl.game_stats['base_HP'] -= t
							print_white("Your base HP just"), print_red("dropped by "+str(t)+"!")
							sleep(1.5)
						else:
							t = random.randint(5,7)
							glbl.game_stats['current_HP'] += t
							glbl.game_stats['base_HP'] += t
							print_white("Your base HP just"), print_green("rose to "+str(glbl.game_stats['base_HP'])+"!")
							sleep(1.5)
						print()
						break

			# If they want to try to get an easy level up:
			# Note that this uses a truncated version of the leveling system from leveling_system.py on Line 660 and 684.
			elif y=='l':
				print("The fairy hands you a yellow liquid.")
				sleep(1.75)

				print("Are you sure you want to drink it?")
				while True:
					print_yellow("[Y]es    [N]o")
					u = input(">>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()

					# This part lets the glbl.player return the potion in case they didn't mean to pick this one, or is having second thoughts.
					elif u=='n':
						print("You hand back the liquid.")
						sleep(1)
						break

					elif u=='y':
						glbl.game_stats['magic_item'] -= 1
						print("After readying yourself, you take a large gulp.")
						sleep(2)
						print("The familiar fire burns within your body.")
						sleep(2.25)
						print(".",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!"), sleep(1)
						if random.randint(0,1)==0:
							glbl.game_stats['p_LV'] -= 1
							print_red("You lost a level!")
							sleep(1.5)
							glbl.game_stats['current_exp'] = 0
							glbl.game_stats['next_level_exp'] = round((6 * (glbl.game_stats['p_LV']**.769))-7.182)
							glbl.game_stats['ATT'] -= random.randint(1, 2)
							HP = random.randint(1, 2)
							glbl.game_stats['current_HP'] -= HP
							glbl.game_stats['base_HP']  -= HP
							x = random.randint(1, 8)
							if x == 7:
								glbl.game_stats['p_DEF'] -= 1
								x = -1

							print_white("HP"), print_red("dropped to: "+str(glbl.game_stats['base_HP']))
							print()
							print_white("ATT"), print_red("dropped to: "+str(glbl.game_stats['ATT']))
							print()
							if x == -1:
								print_white("DEF"), print_red("dropped to: "+str(glbl.game_stats['p_DEF']))
								print()
							sleep(1.5)
						
						else:
							glbl.game_stats['p_LV'] += 1
							print_green("You gained a level!")
							sleep(1.5)
							glbl.game_stats['current_exp'] = 0
							glbl.game_stats['next_level_exp'] = round((6 * (glbl.game_stats['p_LV']**.769))-7.182)
							glbl.game_stats['ATT'] += random.randint(1, 2)
							HP = random.randint(1, 2)
							glbl.game_stats['current_HP'] += HP
							glbl.game_stats['base_HP']  += HP
							x = random.randint(1, 8)
							if x == 7:
								glbl.game_stats['p_DEF'] += 1
								x = -1

							print_white("HP"), print_green("rose to: "+str(glbl.game_stats['base_HP']))
							print()
							print_white("ATT"), print_green("rose to: "+str(glbl.game_stats['ATT']))
							print()
							if x == -1:
								print_white("DEF"), print_green("rose to: "+str(glbl.game_stats['p_DEF']))
								print()
							sleep(1.5)
						print()
						break

			# Once the glbl.player is ready to leave, or they no longer have any magic resources to trade with, they can head back out into the forest.
			if y=='n' or glbl.game_stats['magic_item'] == 0:
				print_magenta("Thanks bye bye!")
				sleep(.75)
				return glbl.game_stats

			# If the glbl.player has stocked up on magic resources, and wants to try again with the same or a different glbl.game_stats:
			if y=='l' or y=='h' or y=='a' or y=='d':
				print_magenta("Wanna drink another?!")
				while True:
					print_yellow("[Y]es ("+str(glbl.game_stats['magic_item'])+")    [N]o")
					y = input(">>> ").lower()
					print()
					if y!='y' and y!='n':
						invalid()
					elif y=='y':
						os.system('clear')
						print()
						break
					elif y=='n':
						print_magenta("Thanks bye bye!")
						sleep(.75)
						return glbl.game_stats
						
# This is the last single time encouter.
# It is very short, as it simply dictates that the glbl.player has found the orc, and can now go battle it at any time.
def orc_battle():
	if glbl.game_stats['orc'] == True:
		complete(glbl.game_stats)
		return glbl.game_stats

	else:
		glbl.game_stats['orc'] = True
		os.system('clear')
		print("You break out into a clearing. At the far side is a cave entrance.")
		sleep(3)
		print("Large footprints have trampled the ground all around.")
		sleep(2.8)
		print("This and the various animal corpses strewn about, lead to one conclusion.")
		sleep(3)
		print("At long last, you have discovered the orc.")
		sleep(4)
		print("After marking down this location, you leave to prepare for the upcoming")
		print("fight.")
		sleep(4)
		return glbl.game_stats


# Testing for all the different random encounters.
# It also lets me see if the one time encounters are working.
if __name__ == '__main__':

	print("Dont run this, silly!")