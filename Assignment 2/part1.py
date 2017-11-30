from heapq import heappush, heappop
from random import shuffle

#read the input file and return a 2-D array 
#to represent the game board
def get_game(name):
	game = []
	file = open(name, "r")
	for line in file:
		temp = []
		for each in line: temp.append(each)
		if temp[len(temp)-1] == '\n' or temp[len(temp)-1] == '\r': temp.pop()
		if temp[len(temp)-1] == '\n' or temp[len(temp)-1] == '\r': temp.pop()
		game.append(temp)
	file.close
	return game

#print the game result 
def print_game(game):	
	temp = []
	for item in game:
		temp.append(item)
	for line in temp:
		hold = ''.join(str(e) for e in line)
		print hold
	print '\n'

#find all the legal domain, for specific 
#variable this domain found will be constrained
def get_domain(game):
	domain = []
	for line in game:
		for each in line:
			if each != '_' and each not in domain:
				domain.append(each)
	return domain

#find all the source cell's position
def get_source(game):
	source = []
	for y in range(0, len(game)):
		for x in range(0, len(game[0])):
			if game[y][x] != '_':
				source.append([y, x])
	return source
	
#find all the remaining variable
def get_variable(game):
	variable = []
	for y in range(0, len(game)):
		for x in range(0, len(game[0])):
			if game[y][x] == '_': variable.append([y, x])
	return variable	

#minimum remaining value heuristics
def mrv(var, game, source, domain):
	heap = []
	for each in var:
		count = 0
		avail_color = []
		for color in domain:
			if constraints_withfc(game, color, each, source) == True:
				avail_color.append(color)
				count += 1 
		heappush(heap, (count, each, avail_color))
	item = []
	item.append(heappop(heap))
	if len(heap) > 0: last = heappop(heap)
	else: return item[0]
	
	while item[0] == last:
		item.append(last) 
		if len(heap) > 0: lest = heappop(heap)
	
	return mcv(game, item)

#most constraining variable heuristic
def mcv(game, item):
	heap = []
	for each in item:
		count = 0
		y = each[1][0]
		x = each[1][1]
		up = y - 1
		down = y +1
		left = x -1 
		right = x+1
		if up in range(0, len(game)): 
			if game[up][x] == '_': count += 1
			
		if down in range(0, len(game)):
			if game[down][x] == '_': count += 1
		
		if left in range(0, len(game[0])):
			if game[y][left] == '_': count += 1
		
		if right in range(0, len(game[0])):
			if game[y][right] == '_': count += 1
		heappush(heap, (count, [y, x], each[2]))
	var = []
	while len(heap) > 0: var.append(heappop(heap))
	
	return var[len(var)-1]
	
#Least constraining assignment heuristics
def lca(game, cur_var, domain, colors, source):
	heap = []
	sorted_colors = []
	y = cur_var[0]
	x = cur_var[1]
	up = cur_var[0] - 1
	down = cur_var[0] + 1
	left = cur_var[1] - 1
	right = cur_var[1] + 1
	for each in colors:
		game[y][x] = each
		count = 0
		for color in domain:
			if up in range(0, len(game)) and game[up][x] == '_':
				if constraints_withfc(game, color, [up, x], source) == True:
					count += 1 
			if down in range(0, len(game)) and game[down][x] == '_':
				if constraints_withfc(game, color, [down, x], source) == True:
					count += 1 
			if left in range(0, len(game[0])) and game[y][left] == '_':
				if constraints_withfc(game, color, [y, left], source) == True:
					count += 1
			if right in range(0, len(game[0])) and game[y][right] == '_': 
				if constraints_withfc(game, color, [y, right], source) == True:
					count += 1 
		heappush(heap, (count, color, each))
		game[y][x] = '_'
	while len(heap) != 0:
		sorted_colors.append(heappop(heap)[2])
	sorted_colors.reverse()
	return sorted_colors	
		
#dumb backtracking search
def dumb_solver(game, var, domain, source):
	if len(var) == 0:
		if goaltest(game, source) == True:
			print_game(game)	
			return True
		else: return False
	shuffle(var)
	cur_val = var[0]
	for color in domain:
		if constraints(game, color, cur_val, source) == True:
			game[cur_val[0]][cur_val[1]] = color
			temp_v = get_variable(game)
			result = dumb_solver(game, temp_v, domain, source)
			if result == True: return True
			game[cur_val[0]][cur_val[1]] = '_'
	return False

#smart backtracking search
def smart_solver(game, var, domain, source):
	if len(var) == 0:
		if goaltest(game, source) == True:
			print_game(game)	
			return True
		else: return False
	item = mrv(var, game, source, domain)
	cur_val = item[1]
	sorted_color = lca(game, cur_val, domain, item[2], source)
	for color in sorted_color:
		game[cur_val[0]][cur_val[1]] = color
		temp_v = get_variable(game)
		result = smart_solver(game, temp_v, domain, source)
		if result == True: return True
	game[cur_val[0]][cur_val[1]] = '_'
	return False
#constraints with forward checking
def constraints_withfc(game, color, val, source):
	count = 0
	y = val[0]
	x = val[1]
	up = y-1
	down = y+1
	left = x-1
	right = x+1
	
	#check isolated cell
	if up in range(0, len(game)):
		if game[up][x] == '_' or color == game[up][x]: count += 1
	if left in range(0, len(game[0])): 
		if game[y][left] == '_' or color == game[y][left]: count += 1
	if down in range(0, len(game)): 
		if game[down][x] == '_' or color == game[down][x]: count += 1
	if right in range(0, len(game[0])): 
		if game[y][right] == '_' or color == game[y][right]: count += 1
	if count < 2: return False
		
	#forward checking
	if up in range(0, len(game)):
		if game[up][x] != '_':
			count = 0
			if up-1 in range(0, len(game)):
				if game[up-1][x] == game[up][x] or game[up-1][x] == '_': count += 1
				if game[up][x] == color: count += 1
			if up+1 in range(0, len(game)):
				if game[up+1][x] == game[up][x] or game[up+1][x] == '_': count += 1
				if game[up][x] == color: count += 1
			if left in range(0, len(game[0])):
				if game[up][left] == game[up][x] or game[up][left] == '_': count += 1
				if game[up][x] == color: count += 1
			if right in range(0, len(game[0])):
				if game[up][right] == game[up][x] or game[up][right] == '_': count += 1
				if game[up][x] == color: count += 1
			if [up, x] in source: 
				if count <= 1: return False
			else: 
				if count <= 2: return False
		
	if down in range(0, len(game)):
		if game[down][x] != '_':
			count = 0
			if down-1 in range(0, len(game)):
				if game[down-1][x] == game[down][x] or game[down-1][x] == '_': count += 1
				if game[down][x] == color: count += 1
			if down+1 in range(0, len(game)):
				if game[down+1][x] == game[down][x] or game[down+1][x] == '_': count += 1
				if game[down][x] == color: count += 1
			if left in range(0, len(game[0])):
				if game[down][left] == game[down][x] or game[down][left] == '_': count += 1
				if game[down][x] == color: count += 1
			if right in range(0, len(game[0])):
				if game[down][right] == game[down][x] or game[down][right] == '_': count += 1
				if game[down][x] == color: count += 1
			if [down, x] in source: 
				if count <= 1: return False
			else: 
				if count <= 2: return False
	
	if left in range(0, len(game[0])):
		if game[y][left] != '_':
			count = 0
			if up in range(0, len(game)):
				if game[up][left] == game[y][left] or game[up][left] == '_': count += 1
				if game[y][left] == color: count += 1
			if down in range(0, len(game)):
				if game[down][left] == game[y][left] or game[down][left] == '_': count += 1
				if game[y][left] == color: count += 1
			if left-1 in range(0, len(game[0])):
				if game[y][left-1] == game[y][left] or game[y][left-1] == '_': count += 1
				if game[y][left] == color: count += 1
			if left+1 in range(0, len(game[0])):
				if game[y][left+1] == game[y][left] or game[y][left+1] == '_': count += 1
				if game[y][left] == color: count += 1
			if [y, left] in source: 
				if count <= 1: return False
			else: 
				if count <= 2: return False

	if right in range(0, len(game[0])):
		if game[y][right] != '_':
			count = 0
			if up in range(0, len(game)):
				if game[up][right] == game[y][right] or game[up][right] == '_': count += 1
				if game[y][right] == color: count += 1
			if down in range(0, len(game)):
				if game[down][right] == game[y][right] or game[down][right] == '_': count += 1
				if game[y][right] == color: count += 1
			if right-1 in range(0, len(game[0])):
				if game[y][right-1] == game[y][right] or game[y][right-1] == '_': count += 1
				if game[y][right] == color: count += 1
			if right+1 in range(0, len(game[0])):
				if game[y][right+1] == game[y][right] or game[y][right+1] == '_': count += 1
				if game[y][right] == color: count += 1
			if [y, right] in source: 
				if count <= 1: return False
			else: 
				if count <= 2: return False
				
	#zigzag check
	count = 0
	if up in range(0, len(game)):
		if game[up][x] == color: count += 1
	if left in range(0, len(game[0])): 
		if game[y][left] == color: count += 1
	if down in range(0, len(game)): 
		if game[down][x] == color: count += 1
	if right in range(0, len(game[0])): 
		if game[y][right] == color: count += 1	
	if count > 2: return False

	return True	
#constraints without forward checking
def constraints(game, color, val, source):
	count = 0
	y = val[0]
	x = val[1]
	up = y-1
	down = y+1
	left = x-1
	right = x+1
	#check isolated cell
	if up in range(0, len(game)):
		if game[up][x] == '_' or color == game[up][x]: count += 1
	if left in range(0, len(game[0])): 
		if game[y][left] == '_' or color == game[y][left]: count += 1
	if down in range(0, len(game)): 
		if game[down][x] == '_' or color == game[down][x]: count += 1
	if right in range(0, len(game[0])): 
		if game[y][right] == '_' or color == game[y][right]: count += 1
	if count < 2: return False
				
	#zigzag check
	count = 0
	if up in range(0, len(game)):
		if game[up][x] == color: count += 1
	if left in range(0, len(game[0])): 
		if game[y][left] == color: count += 1
	if down in range(0, len(game)): 
		if game[down][x] == color: count += 1
	if right in range(0, len(game[0])): 
		if game[y][right] == color: count += 1	
	if count > 2: return False

	return True	


#test whether all assignments are valid
def goaltest(game, source):
	for y in range(0, len(game)):
		for x in range(0, len(game[0])):
			up = y-1
			down = y+1
			left = x-1
			right = x+1
			color = game[y][x]
			count = 0
			if up in range(0, len(game)):
				if game[up][x] == color: count += 1
			if left in range(0, len(game[0])): 
				if game[y][left] == color: count += 1
			if down in range(0, len(game)): 
				if game[down][x] == color: count += 1
			if right in range(0, len(game[0])): 
				if game[y][right] == color: count += 1	
			if [y, x] in source and count > 1: return False
			if [y, x] not in source and count > 2: return False
			
	return True
	
################################
#run the free flow solver				
game = get_game("input1214.txt")
domain = get_domain(game) 
source = get_source(game)
variable = get_variable(game)
#smart_solver(game, variable, domain, source)
#dumb_solver(game, variable, domain, source)