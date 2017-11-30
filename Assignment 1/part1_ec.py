#part1_extra credit
from data_structure import start_loc, find_dots, nearest, nearest_points, Manhattan_distance, maze_to_graph, path_to_solution
from collections import deque
from heapq import heappop, heappush
import sys

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

P = start_loc(maze)				#find the starting location
Dots = find_dots(maze)			#find the locations of '.'
nodes_expanded = 0

#A* search algorithm
def AStar(maze, P, Goal):
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
	#print "A* search #nodes expanded: ", len(path)
	global nodes_expanded
	nodes_expanded += len(path)
	#print path
	return path_to_solution(path, graph)	#call helper function to return solution


def part1_ec(Dots, P, maze):
	totalcost = 0
	while Dots:
		costheap = []
		for each in Dots: heappush(costheap, (len(AStar(maze, P, each))-1, each))
		nextpoint = heappop(costheap)		#find next best point
		totalcost += nextpoint[0]			#update pathcost
		P = nextpoint[1]
		Dots.remove(nextpoint[1])
	return totalcost

print "solution cost:", part1_ec(Dots, P, maze)	
print "nodes_expanded:", nodes_expanded		

