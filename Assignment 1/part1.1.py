from data_structure import start_loc, find_dot, nearest, nearest_points, Manhattan_distance, maze_to_graph, path_to_solution, get_maze
from collections import deque
from heapq import heappop, heappush
import sys

#Depth-first search algorithm
def DFS(maze, P, Goal):
	graph = maze_to_graph(maze)
	queue = deque([P])						#queue to hold nodes
	path = []								#array to record visited nodes
	visited = []
	while deque:							#maze searching loop
		curr = queue.pop()					#pop from right, depth first search
		visited.append(curr)
		if curr == Goal:
			path.append(curr)
			break
		if curr in path:					#skip visited nodes
			continue
		path.append(curr)
		for neighbour in graph[curr[0],curr[1]]:
			queue.append(neighbour)			#update the search queue from the key's items in the graph
	print "Depth-first search #nodes expanded: ", len(visited)
	# print visited
	return path_to_solution(path, graph)	#call helper function to return solution

#helper function to test DFS and print solution path
def test_DFS(maze, P, Goal):
	DFS_solution = DFS(maze, P, Goal)
	print "DSF path cost: ", len(DFS_solution)-1
	print DFS_solution
	temp = []
	for item in maze:
		temp.append(item)
	for each in DFS_solution:
		if each != P and each != Goal:
			temp[each[0]][each[1]] = "."
	for line in temp:
		hold = ''.join(str(e) for e in line)
		print hold


#Breadth-first search algorithm
def BFS(maze, P, Goal):
	graph = maze_to_graph(maze)
	queue = deque([P])						#queue to hold nodes
	path = []								#array to record visited nodes
	visited = []
	while deque:							#maze searching loop
		curr = queue.popleft()				#pop from left, breadth first search
		visited.append(curr)
		if curr == Goal:
			path.append(curr)
			break
		if curr in path:					#skip visited nodes
			continue
		path.append(curr)
		for neighbour in graph[curr[0],curr[1]]:
			queue.append(neighbour)			#update the search queue from the key's items in the graph
	print "Breadth-first search #nodes expanded: ", len(visited)
	# print visited
	return	path_to_solution(path, graph)	#call helper function to return solution

#helper function to test BFS and print solution path
def test_BFS(maze, P, Goal):
	BFS_solution = BFS(maze, P, Goal)
	print "BSF path cost: ", len(BFS_solution)-1
	print BFS_solution
	temp = []
	for item in maze:
		temp.append(item)
	for each in BFS_solution:
		if each != P and each != Goal:
			temp[each[0]][each[1]] = "."
	for line in temp:
		hold = ''.join(str(e) for e in line)
		print hold

#Greedy best-first search algorithm
def GBFS(maze, P, Goal):
	graph = maze_to_graph(maze)
	heap = []								#priority queue to hold nodes
	heappush(heap, (Manhattan_distance(P, Goal), P))		#(distance, location)
	path = []								#array to record visited nodes
	visited = []
	while heap:								#maze searching loop
		curr = heappop(heap)				#pop the node with smallest distance to goal
		visited.append(curr)
		if curr[1] == Goal:
			path.append(curr[1])
			break
		if curr[1] in path:					#skip visited nodes
			continue
		path.append(curr[1])
		for neighbour in graph[curr[1][0],curr[1][1]]:		#update neighbours to the priority queue, with distance to goal
			heappush(heap, (Manhattan_distance(neighbour, Goal), neighbour))
	print "Greedy best-first search #nodes expanded: ", len(visited)
	# print visited
	return path_to_solution(path, graph)	#call helper function to return solution

#helper function to test Greedy Best-first search and print solution path
def test_GBFS(maze, P, Goal):
	GBFS_solution = GBFS(maze, P, Goal)
	print "GBSF path cost: ", len(GBFS_solution)-1
	print GBFS_solution
	temp = []
	for item in maze:
		temp.append(item)
	for each in GBFS_solution:
		if each != P and each != Goal:
			temp[each[0]][each[1]] = "."
	for line in temp:
		hold = ''.join(str(e) for e in line)
		print hold

#A* search algorithm
def AStar(maze, P, Goal):
	graph = maze_to_graph(maze)
	heap = []								#priority queue to hold nodes
	heappush(heap, (Manhattan_distance(P, Goal), 0, P))	#(distance+cost, cost, location)
	path = []								#array to record visited nodes
	visited = []
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
	print "A* search #nodes expanded: ", len(visited)
	# print visited
	return path_to_solution(path, graph)	#call helper function to return solution

#helper function to test A* Search and print solution path
def test_AStar(maze, P, Goal):
	AStar_solution = AStar(maze, P, Goal)
	print "AStar path cost: ", len(AStar_solution)-1
	print AStar_solution
	temp = maze
	for each in AStar_solution:
		if each != P and each != Goal:
			temp[each[0]][each[1]] = "."
	for line in temp:
		hold = ''.join(str(e) for e in line)
		print hold

#main function
#data structure of maze is a 2D array
#each space is one row of the maze
mazeinput = sys.argv[1]
maze = get_maze(mazeinput)

P = start_loc(maze)				#find the starting location
Goal = find_dot(maze)			#find the location of '.'

test_DFS(maze, P, Goal)
print "-----------------------------------------------------------------------------------------------------------------------------------------------"
maze = get_maze(mazeinput)
test_BFS(maze, P, Goal)
print "-----------------------------------------------------------------------------------------------------------------------------------------------"
maze = get_maze(mazeinput)
test_GBFS(maze, P, Goal)
print "-----------------------------------------------------------------------------------------------------------------------------------------------"
maze = get_maze(mazeinput)
test_AStar(maze, P, Goal)
