from data_structure import start_loc, find_dots, nearest, nearest_points, Manhattan_distance, maze_to_graph, path_to_solution
from collections import deque
from heapq import heappop, heappush
import sys

solution = []
path = []

#main function
#data structure of maze is a 2D array
#each space is one row of the maze
maze = []						#load the maze 
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

P = start_loc(maze)				#find the starting location
Dots = find_dots(maze)			#find the locations of '.'
nodes_expanded = 0				#global variable for storing numbers of nodes expanded
#part 1.2
 	
#A* search algorithm, same as part1.1
def AStar1(maze, P, Goal):
	graph = maze_to_graph(maze)
	heap = []								#priority queue to hold nodes
	heappush(heap, (Manhattan_distance(P, Goal), 0, P))	#(distance+cost, cost, location)
	path = []								#array to record visited nodes
	while heap:								#maze searching loop
		curr = heappop(heap)				#pop the node with smallest (distance+cost) to goal
		if curr[2] == Goal:
			path.append(curr[2])
			break
		if curr[2] in path:					#skip visited nodes
			continue
		path.append(curr[2])
		for neighbour in graph[curr[2][0],curr[2][1]]:		#update neighbours to the priority queue, with (distance+cost) to goal
			heappush(heap, (curr[1]+Manhattan_distance(neighbour, Goal), curr[1]+1, neighbour))
	global nodes_expanded					#
	nodes_expanded += len(path)				#add the nodes expanded in this step
	return path_to_solution(path, graph)	#call helper function to return solution
	
def AStar2(Dots, P, maze):
	if len(Dots) == 0: return 0				#base case
	costheap = []							#priority queue for storing all the costs for the 
	for i in range(0, len(Dots)):
		cost = len(AStar1(maze, P, Dots[i]))-1		
		heappush(costheap, (cost, i))
	mincost = []
	mincost.append(heappop(costheap))
	while len(costheap) != 0:				#pop out the dot(s) with lowest A* search cost
		item = heappop(costheap)
		if item[0] > mincost[0][0]: break
		else: mincost.append(item)
	if len(mincost) == 1:					
		#if theire is a single dot that has lowest cost, recursively to check next dot
		sol = AStar1(maze, P, Dots[mincost[0][1]])	
		global solution
		solution.append(sol)				#update solution
		P = Dots[mincost[0][1]]				#update starting point
		global path
		path.append(Dots[mincost[0][1]])	#save the solution path
		Dots.remove(Dots[mincost[0][1]])
		return AStar2(Dots, P, maze)+mincost[0][0]
	else:
		#when there are several points that have same and minimal cost
		start_location = P
		temp_dots = []
		for each in Dots: temp_dots.append(each)
		P = temp_dots[mincost[0][1]]
		temp_dots.remove(temp_dots[mincost[0][1]])
		leastcost = test(temp_dots, P, maze)+mincost[0][0]		
		index = 0
		for i in range(1, len(mincost)):
			#check each point's final cost
			temp_dots = []
			for each in Dots: temp_dots.append(each)
			P = temp_dots[mincost[i][1]]
 			temp_dots.remove(temp_dots[mincost[i][1]])	
			costtest = test(temp_dots, P, maze)+mincost[i][0]
			if costtest < leastcost:
				leastcost = costtest
				index = i
		sol = AStar1(maze, start_location, Dots[mincost[index][1]])
		solution.append(sol)
		path.append(Dots[mincost[index][1]])
		P = Dots[mincost[index][1]]
		Dots.remove(Dots[mincost[index][1]])	
		return AStar2(Dots, P, maze)+mincost[index][0]	
	
def test(Dots, P, maze):
	#same to AStar2(), excpet that test() doesn't print solution and path
	if len(Dots) == 0: return 0
	costheap = []
	for i in range(0, len(Dots)):
		cost = len(AStar1(maze, P, Dots[i]))-1		
		heappush(costheap, (cost, i))
	mincost = []
	mincost.append(heappop(costheap))
	while len(costheap) != 0:
		item = heappop(costheap)
		if item[0] > mincost[0][0]: break
		else: mincost.append(item)
	if len(mincost) == 1:	
		P = Dots[mincost[0][1]]
		Dots.remove(Dots[mincost[0][1]])
		
		return test(Dots, P, maze)+mincost[0][0]
	else:
		temp_dots = []
		for each in Dots: temp_dots.append(each)
		P = temp_dots[mincost[0][1]]
		temp_dots.remove(temp_dots[mincost[0][1]])
		leastcost = test(temp_dots, P, maze)+mincost[0][0]
		for i in range(1, len(mincost)):
			temp_dots = []
			for each in Dots: temp_dots.append(each)
			P = temp_dots[mincost[i][1]]
 			temp_dots.remove(temp_dots[mincost[i][1]])	
			costtest = test(temp_dots, P, maze)+mincost[i][0]
			if costtest < leastcost:
				leastcost = costtest
		return leastcost				

##main function	
solution_cost = AStar2(Dots, P, maze)
#print solution cost and nodes_expanded
print "solution cost:", solution_cost	
print "nodes_expanded:", nodes_expanded	
Dots = find_dots(maze)
print "solution path:"					
temp = maze
alpha = "abcdefghijklmnopqrstuvwxyz"
#the solution path order for dots is from 0 to 9 then a to z
#print solution path
for sol in solution:
	for each in sol:
 		if each != P and each not in Dots:
			temp[each[0]][each[1]] = '.'
		elif each in Dots:
			for i in range(0, len(path)):
				if each == path[i]: 
					index = i
					break 
			if index < 10: temp[each[0]][each[1]] = index
			else: 
				temp[each[0]][each[1]] = alpha[index-10]
for line in temp:
	hold = ''.join(str(e) for e in line)
 	print hold

