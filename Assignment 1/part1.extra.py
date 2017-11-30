import sys
from heapq import heappop, heappush

#search down the maze 2D array, look for 'P'
def start_loc(maze):
	for y in range(len(maze)):
		for x in range(len(maze[y])):
			if maze[y][x] == 'P':
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
def next_best(P, Dots, maze):
	heap = []
	for each in Dots:
		heappush(heap, (Manhattan_distance(P, each), each))
	nearest = []
	pop = heappop(heap)
	nearest.append(pop[1])
	while len(heap) != 0:
		temp = heappop(heap)
		if temp[0] != pop[0]:
			break
		nearest.append(temp[1])
	if len(nearest) == 1:
		return nearest[0]
	return dot_density(nearest, Dots)			#smallest_total_Manhattan_distance(nearest, Dots)

#heruistic function, return the absolute distance
#between two locations
def Manhattan_distance(p1, p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])		#Manhattan distance equation

def dot_density(nearest, Dots):
	heapq = []
	for each in nearest:
		count = 0
		if [each[0]-2,each[1]-2] in Dots:
			count += 1
		if [each[0]-2,each[1]-1] in Dots:
			count += 1
		if [each[0]-2,each[1]] in Dots:
			count += 1
		if [each[0]-2,each[1]+1] in Dots:
			count += 1
		if [each[0]-2,each[1]+2] in Dots:
			count += 1

		if [each[0]-1,each[1]-2] in Dots:
			count += 1
		if [each[0]-1,each[1]-1] in Dots:
			count += 1
		if [each[0]-1,each[1]] in Dots:
			count += 1
		if [each[0]-1,each[1]+1] in Dots:
			count += 1
		if [each[0]-1,each[1]+2] in Dots:
			count += 1

		if [each[0],each[1]-2] in Dots:
			count += 1
		if [each[0],each[1]-1] in Dots:
			count += 1
		if [each[0],each[1]] in Dots:
			count += 1
		if [each[0],each[1]+1] in Dots:
			count += 1
		if [each[0],each[1]+2] in Dots:
			count += 1

		if [each[0]+1,each[1]-2] in Dots:
			count += 1
		if [each[0]+1,each[1]-1] in Dots:
			count += 1
		if [each[0]+1,each[1]] in Dots:
			count += 1
		if [each[0]+1,each[1]+1] in Dots:
			count += 1
		if [each[0]+1,each[1]+2] in Dots:
			count += 1

		if [each[0]+2,each[1]-2] in Dots:
			count += 1
		if [each[0]+2,each[1]-1] in Dots:
			count += 1
		if [each[0]+2,each[1]] in Dots:
			count += 1
		if [each[0]+2,each[1]+1] in Dots:
			count += 1
		if [each[0]+2,each[1]+2] in Dots:
			count += 1
		heappush(heapq, (count, each))
	ret = heappop(heapq)
	return ret[1]

def wall_density(nearest, Dots, maze):
	heapq = []
	for each in nearest:
		count = 0
		if maze[each[0]-1][each[1]-1] is "%":
			count += 1
		if maze[each[0]-1][each[1]] is "%":
			count += 1
		if maze[each[0]-1][each[1]+1] is "%":
			count += 1

		if maze[each[0]][each[1]-1] is "%":
			count += 1
		if maze[each[0]][each[1]] is "%":
			count += 1
		if maze[each[0]][each[1]+1] is "%":
			count += 1

		if maze[each[0]+1][each[1]-1] is "%":
			count += 1
		if maze[each[0]+1][each[1]] is "%":
			count += 1
		if maze[each[0]+1][each[1]+1] is "%":
			count += 1

		heappush(heapq, (count, each))
	ret = heappop(heapq)
	return ret[1]

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

#A* search algorithm
def AStar(maze, P, Goal):
	graph = maze_to_graph(maze)
	heap = []								#priority queue to hold nodes
	heappush(heap, (Manhattan_distance(P, Goal), 0, P))	#(distance+cost, cost, location)
	visited = []
	path = []								#array to record visited nodes
	while heap:								#maze searching loop
		curr = heappop(heap)				#pop the node with smallest (distance+cost) to goal
		visited.append(curr)
		if curr[2] == Goal:
			path.append(curr[2])
			break
		if curr[2] in path:					#skip visited nodes
			continue
		path.append(curr[2])
		for neighbour in graph[curr[2][0],curr[2][1]]:		#update neighbours to the priority queue, with (distance+cost) to goal
			heappush(heap, (curr[1]+Manhattan_distance(neighbour, Goal), curr[1]+1, neighbour))
	return (len(visited), path_to_solution(path, graph))	#call helper function to return solution

#main function
#data structure of maze is a 2D array
#each space is one row of the maze
maze = []
mazeinput = sys.argv[1]
file = open(mazeinput, "r")
for line in file:
	temp = []
	for each in line:
		temp.append(each)
	temp.pop()					#pop the newline character
	maze.append(temp)
file.close()
maze[len(maze)-1].append("%")

height = len(maze)
width = len(maze[0])

P = start_loc(maze)				#find the starting location
Dots = find_dots(maze)			#find the locations of '.'

cost = 0
node = 0
while Dots:
	Goal = next_best(P, Dots, maze)			#find next best goal
	node_num, sol = AStar(maze, P, Goal)
	node += (node_num-1)					#update number of nodes expanded
	cost += (len(sol)-1)					#update path cost
	P = Goal
	Dots.remove(Goal)
print "nodes expanded: ", node
print "solution cost: ", cost
