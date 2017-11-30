from heapq import heappush, heappop
#data structure and some basic helper functions used in mp1


#search down the maze 2D array, look for 'P'
def start_loc(maze):
	for y in range(len(maze)):
		for x in range(len(maze[y])):
			if maze[y][x] == 'P':
				return [y,x]

#get and refresh maze
def get_maze(name):
	maze = []
	file = open(name, "r")
	for line in file:
		temp = []
		for each in line:
			temp.append(each)
		temp.pop()					#pop the newline character
		maze.append(temp)
	file.close()
	maze[len(maze)-1].append("%")
	return maze

#search down the maze 2D array, look for 'P'
def find_dot(maze):
	for y in range(len(maze)):
		for x in range(len(maze[y])):
			if maze[y][x] == '.':
				return [y,x]

#search down the maze 2D array, look for 'P'
def find_dots(maze):
	ret = []
	for y in range(len(maze)):
		for x in range(len(maze[y])):
			if maze[y][x] == '.':
				ret.append([y,x])
	return ret

#find the nearest goal to the start point
def nearest(P, Dots):
	heap = []
	for each in Dots:
		heappush(heap, (Manhattan_distance(P, each), each))
	goal = heappop(heap)
	
	return goal[1]

def nearest_points(P, Dots):
	heap = []
	for each in Dots:
		heappush(heap, (Manhattan_distance(P, each), each))
	goal = []
	goal.append(heappop(heap))
	while len(heap) != 0:
		p2 = heappop(heap) 
		if p2[0] != goal[0][0]:
			break
		else:
			goal.append(p2)
	points = []
	for each in goal:
		points.append(each[1])
	#print points
	return points
	
#heruistic function, return the absolute distance
#between two locations
def Manhattan_distance(p1, p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])		#Manhattan distance equation

		
#turn the 2D array into dictionary structure
#each key is a location, and the key's items are 
#accesible locations of the key
def maze_to_graph(maze):
	height = len(maze)						#height of maze
	width = len(maze[0])					#width of maze
	graph = {}
	for h in range(height-1):				#looking for all locations that are not wall
		for w in range(width-1):
			if maze[h][w] is not "%":
				graph[h,w] = []				#set the location as a key of the dictionary
	for y, x in graph.keys():				#check if neighbor locations are accssible
		if maze[y-1][x] is not "%":			#check up
			graph[y,x].append([y-1,x])
		if maze[y+1][x] is not "%":			#check down
			graph[y,x].append([y+1,x])
		if maze[y][x-1] is not "%":			#check left 
			graph[y,x].append([y,x-1])
		if maze[y][x+1] is not "%":			#check right
			graph[y,x].append([y,x+1])
	return graph

#find actual solution from path that contains mistakes 
def path_to_solution(path, graph):
	solution = path							#solution
	solution.reverse()						#reverse to trace from back
	size = len(solution)
	delete = []								#array to record item need to be deleted
	for i in range(size-1):
		curr = solution[i]
		if i in delete:						#skip nodes that should be deleted
			continue
		p = 1
		while 1:
			if solution[i+p] in graph[curr[0],curr[1]]:
				break						#trace back the path to find adjacent node of current node
			delete.append(i+p)
			p+= 1
	for each in reversed(delete):			#delete nodes from back, avoid index out range
		del solution[each]
	solution.reverse()						#reverse solution back
	return	solution
