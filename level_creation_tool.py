#level_creation_tool.py
from numpy import fliplr, full, loadtxt, rot90
from pathlib import Path
from PIL import Image
from random import choice, randint, sample

import globals as glbl

# This method attempts to retrieve the level array from the "maps" folder.
# If it is not found, the code generates a new array and a new background map using generate_level() and draw_level()
# 	floor_num is the level of the mountain that needs to be retrieved or generated.
# 	higher determines where the player is entering this level from.
# 		higher="/" means that the player is traveling from the floor below, and should start on the stairs down.
def fetch_level(floor_num, start="/"):

	start_x = 0
	start_y = 0

	try:
		# Grab the level file from the glbl.MAPS folder if it exists.
		file = Path(glbl.MAPS / f"floor_{floor_num}.txt").read_text().split("\n")

		# The first 50 lines are guaranteed to be for the map.
		# Almost the rest of the lines are for the level.
		# The second to last line stores the locations for gathering items.
		# The last line stores the location of the floor captains.
		map_arr = file[:50]
		level_arr = file[50:-1]
		overworld_arr = file[-1].split()

		# Loop over level_arr.
		# Each line starts out as a string.
		# If the starting icon calculated above is in that line of level_arr, assign its location to start_x and start_y
		# Additionally, convert the string into a list of characters and save that back into level_arr.
		for i in range(len(level_arr)):
			if start in level_arr[i]:
				start_x, start_y = level_arr[i].index(start), i
			level_arr[i] = list(level_arr[i])

		# Similar to above, every line of map_arr is a string that needs to be converted to a list of characters.
		for i in range(len(map_arr)):
			temp_map_arr = []
			for j in map_arr[i]:
				temp_map_arr.append([j, None])
			map_arr[i] = temp_map_arr
		
		# overworld_arr stores both strings and integers.
		# Specifically, it stores a list of 1 string and 3 integers in the order of:
		# 	str: The name of the object. Can be something like goblin_0 or reginald
		# 	int: The x coordinate of the object
		# 	int: The y coordinate of the object
		# 	int: A delay for when the object can be spawned back onto the floor.
		# This first line converts every 2nd 3rd and 4th string into an integer.
		# The second line packs together the 4 items into a list.
		overworld_arr = [int(overworld_arr[i]) if i % 4 != 0 else overworld_arr[i] for i in range(len(overworld_arr))]
		overworld_arr = [[overworld_arr[i], overworld_arr[i + 1], overworld_arr[i + 2], overworld_arr[i + 3]] for i in range(0, len(overworld_arr), 4)]

		# If the player has Reginald following them, he will spawn at the entrance point of the floor.
		# This line saves him into overworld_arr, since he wouldn't have been pulled from the file.
		if glbl.game_stats['reginald'] == 2: overworld_arr.append(['reginald', start_x, start_y, 0])



	except:
		
		# This would have triggered if the level file was not found in the glbl.MAPS folder.
		# Each level has a predetermined number of tiles that will make up the width and height of the level.
		# Those values are stored here in level_width and level_height.
		level_width =  [0,  3, 4, 3, 4, 4,  5, 3, 5, 4, 5,  5, 6, 6, 6, 6]
		level_height = [0,  3, 3, 4, 4, 4,  3, 4, 4, 5, 5,  5, 4, 5, 5, 5]

		# Call generate_level(), which will as expected generate the array that makes up the level.
		# It also returns the location of the starting stairs.
		level_arr, overworld_arr, start_x, start_y = generate_level(floor_num, level_width[floor_num], level_height[floor_num])

		# Next, generate a blank array for the map.
		# The location of the starting stairs is automatically placed on the map, so save that location as well.
		map_arr = [[[".", None] for j in range(30)] for i in range(50)]
		map_arr[start_y - 1][start_x - 1][0] = "g"
		map_arr[start_y + 24][start_x - 1][0] = "/"

		# Finally, create the image for the level's background that the player will explore.
		draw_level(level_arr, floor_num)

	# Return the level, map, and starting coordinates.
	return level_arr, map_arr, overworld_arr, start_x, start_y


# This method generates and populates the random level the player will explore.
# 	floor_num is the level of the mountain that needs to be retrieved or generated.
# 	x is the number of horizontal tiles that will make up the level.
# 	y is the number of vertical tiles that will make up the level.
def generate_level(floor_num, x, y):

	# Generate a generic array arr[] of x's that will be filled in later.
	# Add an extra 2 rows and columns to act as padding so the player cannot "escape" the array.
	arr = full(((y * 5) + 2, (x * 5) + 2), "x")

	# Initialize the walls[] and paths[] arrays.
	# These will be used to save which indecese of arr[] are walls and which are walkable paths for later.
	walls = []
	paths = []

	# The mountain is split up into three different "biomes" depending on which floor of the mountain the player is on.
	# Each biome has a specific type of wall that is most common, second most common, and least common to that biome.
	# They are the Primary Wall, Secondary Wall, and Tertiary Wall determined here.
	if floor_num < 6: primary_wall, secondary_wall, tertiary_wall = "T", "W", "R"
	elif floor_num < 11: primary_wall, secondary_wall, tertiary_wall = "W", "R", "T"
	else: primary_wall, secondary_wall, tertiary_wall = "R", "T", "W"

	# Iterate over x and y to grab the desired number of tiles for the map
	for i in range(y):
		for j in range(x):

			# Load in a random tile from the glbl.TILES folder.
			# Then, rotate the tile 90 degrees some number of times and/or vertically flip the tile.
			random_tile = loadtxt((glbl.TILES / f"{randint(1, 23)}.txt"), str)
			random_tile = rot90(random_tile, randint(0, 3))
			if randint(0, 1) == 0:
				random_tile = fliplr(random_tile)

			# Loop over the tile so that its layout can be saved to arr[].
			for k in range(5):
				for l in range(5):

					# If the index of random_tile is "X":
					if random_tile[k][l] == "X":

						# Save the coordinates of this spot to walls[].
						walls.append((i * 5 + k + 1, j * 5 + l + 1))
						
						# Change the wall to the Primary Wall determined above.
						random_tile[k][l] = primary_wall
						
					# Else the index is a walkable path, so its coordinates need to be saved into paths[]
					else: paths.append((i * 5 + k + 1, j * 5 + l + 1))

					# Update the index of arr[] with the index of random_tile[].
					arr[i * 5 + k + 1][j * 5 + l + 1] = random_tile[k][l]

	# Now, we place in the Secondary and Tertiary Walls where there were starting walls.
	# Start with the Tertiary Walls, as there is a potential for whichever goes first to be overwritten by the second dfs() call.
	# Create a random-length list of starting nodes selected from walls[].
	# Then loop over that list, performing a limited depth-first search using wall_dfs().
	tertiary_walls = sample(walls, randint(2, 4))
	for i in tertiary_walls: wall_dfs(arr, i[1], i[0], tertiary_wall, 2, 3)

	# Do the same as above for the Secondary Walls, again after in case any of the seeds where the walls are created overlap..		
	secondary_walls = sample(walls, randint(3, 6))
	for i in secondary_walls: wall_dfs(arr, i[1], i[0], secondary_wall, 2)

	
	# There is a 1 in 6 chance the Floor will have a chest.
	# The player will first have to find a key on the Floor, at which point they can open the chest.
	if randint(0, 5) == 0:

		# This portion is to make sure the edge case in which the key and chest spawn on the same 
		# 	square doesn't occur.
		chest = [None, None]
		while True:
			chest = sample(paths, 2)
			if chest[0] != chest[1]:
				break

		# The first item in chest[] is the chest key and needs the "k" denotation.
		# The second item in chest[] is the actual chest and needs the "K" denotation.
		arr[chest[0][0]][chest[0][1]] = "k"
		arr[chest[1][0]][chest[1][1]] = "K"

		# To make obtaining the key-chest pair just a little bit harder, surround one of them with walls.
		box = chest[0] if randint(0, 2) == 0 else chest[1]

		# However, to make it more interesting also allow a small chance for a wall to not appear.
		try:
			if randint(0, 9) == 0: arr[box[0] - 1][box[1] - 1] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0] - 1][box[1]] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0] - 1][box[1] + 1] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0]][box[1] - 1] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0]][box[1] + 1] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0] + 1][box[1] - 1] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0] + 1][box[1] + 1] = primary_wall
		except: pass
		try:
			if randint(0, 9) == 0: arr[box[0] + 1][box[1] + 1] = primary_wall
		except: pass


	# If the player is on Floor 3 onwards, they have a 1 in 6 chance of discovering a teleport tile.
	# This tile can teleport to a couple floors above or below.
	if floor_num > 2 and randint(0, 4) == 0:
		
		# The default teleport square is the "`" character.
		# It gets reassigned to a real portal later when the player steps on the square for the first time.
		teleport = choice(paths)
		arr[teleport[0]][teleport[1]] = "`"

	# The levels have locations where items can be harvested.
	# These harvest locations need to be walkable, so grab a few random spots from paths[].
	# A harvestable location is denoted by an "A".
	harvest = sample(paths, randint(1, 2))
	for i in harvest: arr[i[0]][i[1]] = "A"

	# There are a few special things that the player has to stand next to order for them to trigger.
	# These will be saved to the overworld array.
	overworld = []
	overworld_coords = sample(paths, randint(1 + (floor_num // 5), 2 + (floor_num // 5)))

	# On either floor 4 or 5, Reginald the Rat should appear.
	if floor_num > 3 and glbl.game_stats['reginald'] == 0 and randint(floor_num, 5):
		glbl.game_stats['reginald'] = 1
		rat = overworld_coords.pop()
		overworld.append(['reginald', rat[1], rat[0], 0])
	
	# On any of the swamp floors past the first, the shopkeep's brother should appear.
	# I want to save Floor 6 just in case the player faced Reginald on Floor 5 to better pace the sidequests.
	elif floor_num > 6 and glbl.game_stats['shopbro'] < 1 and randint(floor_num, 10):
		glbl.game_stats['shopbro'] = 1
		bro = overworld_coords.pop()
		overworld.append(['shopbro', bro[1], bro[0], 0])

	# On any of the mountain floors, the fairy fountain should appear.
	elif floor_num > 10 and glbl.game_stats['fairies'] == 0 and randint(floor_num, 15):
		glbl.game_stats['fairies'] = 1
		fountain = overworld_coords.pop()
		overworld.append(['fountain', fountain[1], fountain[0], 0])

	# The rest will be minibosses that roam the floor called "captains".
	for i in range(len(overworld_coords)):
		if floor_num < 6: captain = choice(['goblin', 'rat', 'wolf'])
		elif floor_num < 11: captain = choice(['slime', 'spider', 'snake'])
		else: captain = choice(['bear', 'goblin_warrior', 'goblin_shaman', 'goblin_rider'])
		overworld.append([f'{captain}_{i}', overworld_coords[i][1], overworld_coords[i][0], 0])

	# The floor has a chance of having ledge squares that can only be navigated from three directions.
	# The higher the floor, the more ledges may be created.
	ledge_spots = sample(paths, randint(0, (floor_num % 4) + 2))
	for i in ledge_spots:
		direction = choice(["u", "d", "l", "r"])
		arr[i[0]][i[1]] = direction

		# If the ledge is facing up or down:
		if direction in ["u", "d"]:

			# If the space directly to the left of the starting spot is empty and passes a random
			# 	1 in 2 flag, extend the ledge to the left.
			if arr[i[0]][i[1] - 1] == "." and randint(0, 1) == 0:
				arr[i[0]][i[1] - 1] = direction

				# Now, if the space 2 to the left of this starting spot is empty and passes a random
				# 	1 in 4 flag, extend the ledge to the left again.
				if arr[i[0]][i[1] - 2] == "." and randint(0, 3) == 0:
					arr[i[0]][i[1] - 2] = direction 

			# If the space directly to the right of the starting spot is empty and passes a random
			# 	1 in 2 flag, extend the ledge to the right.
			if arr[i[0]][i[1] + 1] == "." and randint(0, 1) == 0:
				arr[i[0]][i[1] + 1] = direction

				# Now, if the space 2 to the right of this starting spot is empty and passes a random
				# 	1 in 4 flag, extend the ledge to the right again.
				if arr[i[0]][i[1] + 2] == "." and randint(0, 3) == 0:
					arr[i[0]][i[1] + 2] = direction 

		# If the ledge is facing left or right:
		else:

			# If the space directly above the starting spot is empty and passes a random 1 in 2 flag, 
			# 	extend the ledge upwards.
			if arr[i[0] - 1][i[1]] == "." and randint(0, 1) == 0:
				arr[i[0] - 1][i[1]] = direction

				# If the space 2 above the starting spot is empty and passes a random 1 in 2 flag, 
				# 	extend the ledge upwards again.
				if arr[i[0 - 2]][i[1]] == "." and randint(0, 3) == 0:
					arr[i[0 - 2]][i[1]] = direction

			# If the space directly below the starting spot is empty and passes a random 1 in 2 flag, 
			# 	extend the ledge downwards.
			if arr[i[0] + 1][i[1]] == "." and randint(0, 1) == 0:
				arr[i[0] + 1][i[1]] = direction

				# If the space 2 below the starting spot is empty and passes a random 1 in 2 flag, 
				# 	extend the ledge downwards again.
				if arr[i[0] + 2][i[1]] == "." and randint(0, 3) == 0:
					arr[i[0] + 2][i[1]] = direction 
				

	# Finally, select spots where the stairs down and up are.
	# This is encompassed in a while loop because the stairs should be at least 7 spaces in the x or y direction away from each other.
	# This is because the player should have to explore the level to some extent before progressing.
	stairs = []
	while True:
		stair_down = choice(paths)
		stair_up = choice(paths)

		# If the selected stairs are far enough way, save them into stairs[] and break out of the loop.
		if abs(stair_down[0] - stair_up[0]) >= 7 or abs(stair_down[1] - stair_up[1]) >= 7:
			stairs.append(stair_down)
			stairs.append(stair_up)
			break

	# The first item in stairs[] is the starting stairs, and therefore needs the "/" denotation.
	# Similarly, the second item in stairs[] is the ending stairs and need the "|" denotation.
	arr[stairs[0][0]][stairs[0][1]] = "/"
	arr[stairs[1][0]][stairs[1][1]] = "|"

	# If the player is on the first 2 floors, the stairs must be reachable from each other
	# This is because the player will not have unlocked the ability to buy scrolls and destory walls yet.
	while floor_num < 3 and not stairs_bfs(arr, stairs[0]):
		arr[stairs[1][0]][stairs[1][1]] = "."
		stairs[1] = choice(paths)
		arr[stairs[1][0]][stairs[1][1]] = "|"	
	
	# Return the array arr[] as well as the coordinates for the starting stairs.
	return arr, overworld, stairs[0][1], stairs[0][0]


# This method performs a limited depth-first-search in order to vary the types of walls in the level.
# 	arr is the array generated by generate_level() that will be explored.
# 	x is the x coordinate of the space in arr that needs to be checked.
# 	y is the y coordinate of the space in arr that needs to be checked.
# 	wall is the type of wall that will be replacing the space dictated by x and y.
# 	num is how much more the wall will continue to spread out from the space dictated by x and y.
# 	spread_factor is used to randomly decide if a wall should spread out an extra amount or not.
def wall_dfs(arr, x, y, wall, num, spread_factor=4):

	# Start by immediately overwriting the space in arr with the provided wall type.
	arr[y][x] = wall

	# If num is greater than 1, than also perform wall_dfs() on the four cardinal points adjacent to arr[y][x].
	if num > 1:

		# Randomly generate a number between 1 and spread_factor.
		# If this number is 1, than the same num is passed into the next call of wall_dfs().
		# If it is not, instead pass in num - 1.
		if arr[y - 1][x] not in [".", "x", wall]: wall_dfs(arr, x, y - 1, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)
		if arr[y][x + 1] not in [".", "x", wall]: wall_dfs(arr, x + 1, y, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)		
		if arr[y + 1][x] not in [".", "x", wall]: wall_dfs(arr, x, y + 1, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)
		if arr[y][x - 1] not in [".", "x", wall]: wall_dfs(arr, x - 1, y, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)


# This method verifies that the ending stairs are accessible from the starting stairs.
# 	It will only run on the first 2 levels.
# 	It return True if they are reachable, otherwise False.
# 	arr is the array generated by generate_level() that will be explored.
# 	coord is a tuple consisting of the x and y coordinates of the starting stairs.
def stairs_bfs(arr, coord):
	
	# I use breadth first search here to find the stairs, because I can.
	# Thus, we need to initalize an array of visited nodes as well as a queue.
	visited = []
	queue = [coord]
 
	# While there are still nodes in queue that need to be checked:
	while queue:

		# Pop the first node in queue[].
		node = queue.pop(0)

		# If that popped node is the stairs up, return True.
		if arr[node[0]][node[1]] == "|":
			return True

		# Else if the node is not a wall, and isn't already in visited:
		elif arr[node[0]][node[1]] in [".", "/"] and node not in visited:

			# Add the node to visited, then add all its cardinally adjacent spaces to queue[]
			visited.append(node)
			queue.append((node[0] - 1, node[1]))
			queue.append((node[0], node[1] + 1))
			queue.append((node[0] + 1, node[1]))
			queue.append((node[0], node[1] - 1))

	# If we reach here, all the spaces radiating out from the starting stairs were explored and the stairs up weren't found.
	# We then should return False.
	return False


# This method draws the level background that the player will see.
# 	level_arr is the array generated by generate_level().
# 	floor_num is the floor of the mountain the player is about to explore.
def draw_level(level_arr, floor_num):

	# Initialize square size to 48, and map_width and map_height to the horizontal length and vertical height of level_arr[][].
	square_size = 48
	map_width = len(level_arr[0])
	map_height = len(level_arr)

	# Initialize the size of the image the player will see, and set the background to the RGB value (0, 0, 0) i.e. black.
	image = Image.new("RGB", (square_size * map_width, square_size * map_height), (0, 0, 0))

	# Update the glbl.SPRITES path to the right biome folder depending on the floor_num
	global FOLDER
	if floor_num < 6: FOLDER = "forest"
	elif floor_num < 11: FOLDER = "swamp"
	else: FOLDER = "mountain"

	# Initialize the various square types and save them into arrays.
	# path, tree, and rock are arrays so that a random image from them can be chosed to add visual variety.
	path = [Image.open(glbl.SPRITES / FOLDER / "path0.png"),
			Image.open(glbl.SPRITES / FOLDER / "path1.png"),
			Image.open(glbl.SPRITES / FOLDER / "path2.png")]
	tree = [Image.open(glbl.SPRITES / FOLDER / "tree0.png"),
			Image.open(glbl.SPRITES / FOLDER / "tree1.png"),
			Image.open(glbl.SPRITES / FOLDER / "tree2.png")]
	water = Image.open(glbl.SPRITES / FOLDER / "water.png")
	rock = [Image.open(glbl.SPRITES / FOLDER / "rock0.png"),
			Image.open(glbl.SPRITES / FOLDER / "rock1.png")]
	harvest = Image.open(glbl.SPRITES / FOLDER / "harvest1.png")
	ledge = [Image.open(glbl.SPRITES / FOLDER / "ledge_up.png"),
			Image.open(glbl.SPRITES / FOLDER / "ledge_down.png"),
			Image.open(glbl.SPRITES / FOLDER / "ledge_left.png"),
			Image.open(glbl.SPRITES / FOLDER / "ledge_right.png")]

	# Loop over all of level_arr[][].
	for i in range(map_height):
		for j in range(map_width):

			# square is the indexed space in level_arr[][] being checked.
			# x and y are the coordinates on image of the upper-left corner where the squares should go.
			square = level_arr[i][j]
			x = (j * square_size)
			y = (i * square_size)

			# If the square is supposed to be part of the walkable path.
			if square == ".":
				image.paste(path[randint(0, 2)], (x, y))

			# If the square is the stair up or down, add in those images.
			elif square == "|":
				image.paste(Image.open(glbl.SPRITES / FOLDER / "stairs_up.png"), (x, y))
			elif square == "/":
				image.paste(Image.open(glbl.SPRITES / FOLDER / "stairs_down.png"), (x, y))
			
			# If square is a wall, place in the correct type of wall.
			if square == "T":
				image.paste(tree[randint(0, 2)], (x, y))
			elif square == "W":
				image.paste(water, (x, y))
			elif square == "R":
				image.paste(rock[randint(0, 1)], (x, y))

			# If the square is a harvestable spot, add in the harvest image.
			elif square == "A":
				image.paste(harvest, (x, y))
			
			# If the square is an up ledge, add in the correct ledge image.
			elif square == "u":
				image.paste(ledge[0], (x, y))

			# If the square is an down ledge, add in the correct ledge image.
			elif square == "d":
				image.paste(ledge[1], (x, y))

			# If the square is an left ledge, add in the correct ledge image.
			elif square == "l":
				image.paste(ledge[2], (x, y))

			# If the square is an right ledge, add in the correct ledge image.
			elif square == "r":
				image.paste(ledge[3], (x, y))

			# If the square is chest key, add in the second chest image.
			elif square == "k":
				image.paste(Image.open(glbl.SPRITES / FOLDER / "chest_key.png"), (x, y))

			# If the square is a chest, add in the first chest image.
			elif square == "K":
				image.paste(Image.open(glbl.SPRITES / FOLDER / "chest_closed.png"), (x, y))

			# If the square is a teleport point, add in the teleport image.
			elif square in glbl.teleport_chars:
				image.paste(Image.open(glbl.SPRITES / FOLDER / "teleport.png"), (x, y))


	# The image is saved.
	image.save((glbl.MAPS / f"floor_{floor_num}.png"))			



if __name__ == "__main__":
	
	# seed(0)

	# for i in range(2, 6):
	# 	fetch_level(i)
	# 	im = Image.open(glbl.MAPS / f"floor_{i}.png")
	# 	im.show()

	file = Path(glbl.MAPS / f"floor_{2}.txt").read_text().split("\n")
	print()
	print('Floor 2:')
	for i in file[50:-1]:
		for j in i:
			if j in ['R', 'T', 'W']: j = 'X'
			if j in ['A', '|', '/', 'r']: j = '.'
			print(' ' + j, end='')
		print()
	
	print()
	