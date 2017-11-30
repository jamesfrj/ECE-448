import math, random, time

#global variables
black_nodes = 0
white_nodes = 0
black_moves = 0
white_moves = 0
black_time = 0
white_time = 0

#Define win/lose conditions:
#a worker reaches enemy's home base
#or capture all enemy's workers
#return True if game is over
def win_lose(matrix):
	for each in matrix[0]:
		if each == 2:
			print "White win!!!"
			return True
	for each in matrix[7]:
		if each == 1:
			print "Black win!!!"
			return True
	black = 0
	white = 0
	for row in matrix:
		black += row.count(1)
		white += row.count(2)
	if black == 0:
		print "White win!!!"
		return True
	if white == 0:
		print "Black win!!!"
		return True
	return False

#search tree leaf definition
#return True if matrix was leaf node
def win(turn, matrix):
	if turn == 1:
		for each in matrix[7]:
			if each == 1:
				return True
		num = 0
		for row in matrix:
			num += row.count(2)
		if num == 0:
			return True

	if turn == 2:
		for each in matrix[0]:
			if each == 2:
				return True
		num = 0
		for row in matrix:
			num += row.count(1)
		if num == 0:
			return True
	return False

#count number of workers left
def count_worker(agent, matrix):
	num = 0
	if agent == 1:
		for row in matrix:
			num += row.count(1)
		return num
	else:
		for row in matrix:
			num += row.count(2)
		return num

#print out necessary information of the game match
def statistics(matrix):
	print "Black player/player 1: "
	print "Total nodes: ", black_nodes
	print "Total time: ", black_time
	print "Total moves: ", black_moves
	print "Average expanded nodes: ", black_nodes/black_moves
	print "Average time: ", black_time/black_moves
	print "Enemy worker captured: ", 16 - count_worker(2, matrix)
	print ""
	print "White player/player 2: "
	print "Total nodes: ", white_nodes
	print "Total time: ", white_time
	print "Total moves ", white_moves
	print "Average expanded nodes: ", white_nodes/white_moves
	print "Average time: ", white_time/white_moves
	print "Enemy worker captured: ", 16 - count_worker(1, matrix)


#dumb defensive heuristic
#the more workers left, the higher the h(n)
def Defensive1(agent, matrix):
	num = 0
	if agent == 1:
		for row in matrix:
			num += row.count(1)
		return 2*num + random.random()
	if agent == 2:
		for row in matrix:
			num += row.count(2)
		return 2*num + random.random()

#smart defensive heuristic
#balance the number of workers left and number of enemy workers captured
#add killer strategy to win or avoid lose the game
def Defensive2(agent, matrix):
	if win(agent, matrix):
		return 1000 + random.random()
	if win(nextturn(agent), matrix):
		return -1000 + random.random()

	return 3*Defensive1(agent, matrix) + Offensive1(agent, matrix)

#dumb offensive heuristic
#the more enemy workers captured, the higher the h(n)
def Offensive1(agent, matrix):
	num = 0
	if agent == 1:
		for row in matrix:
			num += row.count(2)
		return 2*(30-num) + random.random()
	if agent == 2:
		for row in matrix:
			num += row.count(1)
		return 2*(30-num) + random.random()

#smart offensive heuristic
#balance the number of workers left and number of enemy workers captured
#add killer strategy to win or avoid lose the game
def Offensive2(agent, matrix):
	if win(agent, matrix):
		return 1000 + random.random()
	if win(nextturn(agent), matrix):
		return -1000 + random.random()

	return Defensive1(agent, matrix) + 2*Offensive1(agent, matrix)
	#return count_worker(agent, matrix) - count_worker(nextturn(agent), matrix) + random.random()

def newmatrix(matrix):
	new_matrix = []
	for each in matrix:
		row = []
		for term in each:
			row.append(term)
		new_matrix.append(row)
	return new_matrix

#return turn of next player
def nextturn(turn):
	if turn == 1:
		return 2
	return 1

def print_board(matrix):
	for row in matrix:
		hold = ''.join(str(e) for e in row)
		print hold

#return all possible moves of the current player of the current node
def moves(turn, matrix):
	ret = []
	if turn == 1:
		for height in range(8):
			for width in range(8):
				if matrix[height][width] == 1:
					if height < 7:
						if matrix[height+1][width] == 0:
							new_matrix = newmatrix(matrix)
							new_matrix[height+1][width] = 1
							new_matrix[height][width] = 0
							ret.append(new_matrix)
						if width > 0:
							if matrix[height+1][width-1] == 0 or matrix[height+1][width-1] == 2:
								new_matrix = newmatrix(matrix)
								new_matrix[height+1][width-1] = 1
								new_matrix[height][width] = 0
								ret.append(new_matrix)
						if width < 7:
							if matrix[height+1][width+1] == 0 or matrix[height+1][width+1] == 2:
								new_matrix = newmatrix(matrix)
								new_matrix[height+1][width+1] = 1
								new_matrix[height][width] = 0
								ret.append(new_matrix)
		return ret
	if turn == 2:
		for height in range(8):
			for width in range(8):
				if matrix[height][width] == 2:
					if height > 0:
						if matrix[height-1][width] == 0:
							new_matrix = newmatrix(matrix)
							new_matrix[height-1][width] = 2
							new_matrix[height][width] = 0
							ret.append(new_matrix)
						if width > 0:
							if matrix[height-1][width-1] == 0 or matrix[height-1][width-1] == 1:
								new_matrix = newmatrix(matrix)
								new_matrix[height-1][width-1] = 2
								new_matrix[height][width] = 0
								ret.append(new_matrix)
						if width < 7:
							if matrix[height-1][width+1] == 0 or matrix[height-1][width+1] == 1:
								new_matrix = newmatrix(matrix)
								new_matrix[height-1][width+1] = 2
								new_matrix[height][width] = 0
								ret.append(new_matrix)
		return ret

#depth of 3 minimax search algorithm
#return heuristic value to recursive functions
#return heuristic value and best move to main function
def minimax1(turn, matrix, depth, type):
	global black_nodes
	black_nodes += 1
	if depth == 0 or win(turn, matrix) or win(nextturn(turn), matrix):
		return Defensive1(1, matrix)
	possible_moves = moves(turn, matrix)
	if depth == 3:
		v = -float("inf")
		move = []
		for each in possible_moves:
			vn = minimax1(nextturn(turn), each, depth-1, 'min')
			if vn > v:
				v = vn
				move = each
		return v, move
	else:
		if type == 'max':
			v = -float("inf")
			for each in possible_moves:
				vn = minimax1(nextturn(turn), each, depth-1, 'min')
				v = max(v, vn)
			return v
		if type == 'min': 
			v = float("inf")
			for each in possible_moves:
				vn = minimax1(nextturn(turn), each, depth-1, 'max')
				v = min(v, vn)
			return v

def minimax2(turn, matrix, depth, type):
	global white_nodes
	white_nodes += 1
	if depth == 0 or win(turn, matrix) or win(nextturn(turn), matrix):
		return Offensive1(2, matrix)
	possible_moves = moves(turn, matrix)
	if depth == 3:
		v = -float("inf")
		move = []
		for each in possible_moves:
			vn = minimax2(nextturn(turn), each, depth-1, 'min')
			if vn > v:
				v = vn
				move = each
		return v, move
	else:
		if type == 'max':
			v = -float("inf")
			for each in possible_moves:
				vn = minimax2(nextturn(turn), each, depth-1, 'min')
				v = max(v, vn)
			return v
		if type == 'min': 
			v = float("inf")
			for each in possible_moves:
				vn = minimax2(nextturn(turn), each, depth-1, 'max')
				v = min(v, vn)
			return v

#depth of 4 minimax search algorithm
#return heuristic value to recursive functions
#return heuristic value and best move to main function
def alpha_beta1(turn, matrix, depth, type, max, min):
	global black_nodes
	black_nodes += 1
	if depth == 0 or win(turn, matrix) or win(nextturn(turn), matrix):
		return Offensive2(1, matrix)
	possible_moves = moves(turn, matrix)
	if depth == 4:
		v = -float("inf")
		move = []
		for each in possible_moves:
			vn = alpha_beta1(nextturn(turn), each, depth-1, 'min',float("inf"), v)
			if vn > v:
				v = vn
				move = each
			if max <= v:
				break
		return v, move
	else:
		if type == 'max':
			v = -float("inf")
			for each in possible_moves:
				vn = alpha_beta1(nextturn(turn), each, depth-1, 'min', max, v)
				if vn > v:
					v = vn
				if max <= v:	#prune; beta cut-off
					break
			return v
		if type == 'min': 
			v = float("inf")
			for each in possible_moves:
				vn = alpha_beta1(nextturn(turn), each, depth-1, 'max', v, min)
				if vn < v:
					v = vn
				if min >= v:	#prune, alpha cut-off
					break
			return v

def alpha_beta2(turn, matrix, depth, type, max, min):
	global white_nodes
	white_nodes += 1
	if depth == 0 or win(turn, matrix) or win(nextturn(turn), matrix):
		return Defensive2(2, matrix)
	possible_moves = moves(turn, matrix)
	if depth == 4:
		v = -float("inf")
		move = []
		for each in possible_moves:
			vn = alpha_beta2(nextturn(turn), each, depth-1, 'min',float("inf"), v)
			if vn > v:
				v = vn
				move = each
			if max <= v:
				break
		return v, move
	else:
		if type == 'max':
			v = -float("inf")
			for each in possible_moves:
				vn = alpha_beta2(nextturn(turn), each, depth-1, 'min', max, v)
				if vn > v:
					v = vn
				if max <= v:
					break
			return v
		if type == 'min': 
			v = float("inf")
			for each in possible_moves:
				vn = alpha_beta2(nextturn(turn), each, depth-1, 'max', v, min)
				if vn < v:
					v = vn
				if min >= v:
					break
			return v

#depth 1 greedy bot
def greedy_bot(turn, matrix):
	possible_moves = moves(turn, matrix)	#find all possible moves
	ret = -float("inf")
	move = []
	for each in possible_moves:				#search the move with largest heuristic value
		global white_nodes
		white_nodes += 1
		temp = Defensive1(turn, matrix)
		if temp > ret:
			ret = temp
			move = each
	return ret, move

def main():
	Game_matrix = [	[1, 1, 1, 1, 1, 1, 1, 1],		# 1 is black worker
					[1, 1, 1, 1, 1, 1, 1, 1],
					[0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0],
					[2, 2, 2, 2, 2, 2, 2, 2],
					[2, 2, 2, 2, 2, 2, 2, 2]]		# 2 is white worker
	while 1:
		#player 1
		turn = 1		# 1 is black turn, 2 is white turn
		s = time.clock()
		#v, Game_matrix = greedy_bot(turn, Game_matrix)												#greedy bot for player1
		#v, Game_matrix = minimax1(turn, Game_matrix, 3,'max')										#minimax bot for player1
		v, Game_matrix = alpha_beta1(turn, Game_matrix, 4, 'max', float("inf"), -float("inf"))		#alpha-beta bot for player1
		global black_time
		black_time += (time.clock() - s)
		print_board(Game_matrix)
		global black_moves
		black_moves += 1
		print ""
		if win_lose(Game_matrix):
			statistics(Game_matrix)
			return
		#player 2
		turn = 2
		t = time.clock()
		w, Game_matrix = alpha_beta2(turn, Game_matrix, 4, 'max', float("inf"), -float("inf"))		#alpha-beta bot for player 2
		#w, Game_matrix = minimax2(turn, Game_matrix, 3,'max')										#minimax bot for player2
		#w, Game_matrix = greedy_bot(turn, Game_matrix)												#greedy bot for player2
		global white_time
		white_time += (time.clock() - t)
		print_board(Game_matrix)
		global white_moves
		white_moves += 1
		print ""
		if win_lose(Game_matrix):
			statistics(Game_matrix)
			return

main()
