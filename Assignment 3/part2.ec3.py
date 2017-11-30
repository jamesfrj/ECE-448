#!/usr/bin/python

import math

#data loader

def get_data(filename):
	dataset = []
	data = []
	file = open(filename, "r")
	count = 0
	high_ener_count = 0
	for line in file:
		count += 1	
		temp = []
		#line 26, 27, 28 are left blank
		if count == 26 or count == 27: continue
		if count == 28: 
			count = 0
			dataset.append(data)
			data = []
			continue 
		#regard % as 0, blank as 1
		for each in line:
			if each == '%': temp.append(0)
			elif each == ' ': 
				temp.append(1)
				high_ener_count += 1
		data.append(temp)
	file.close()
	return dataset

## P(class | document) = P(document | class) * P(class) 
def likelihood_3(data):
	#the 2-D array
	total = []
	num_of_data = len(data)
	row = 25
	col = 10
	for x in range(0, row):
		array = [0]*11
		for item in data: #131 item
			index = item[x].count(1) 
			array[index] += 1
		
		for i in range(0, len(array)):
			#laplace constant k = 4.5 v = 11
			array[i] = float(array[index]+4.5) / float(num_of_data+4.5*11)	
			
		#insert 25 1-D array sized 11
		total.append(array)			
	return total			

def naive_bayes_classifier_3(yes_test, no_test):
	#setup the test data
	width = len(yes_test[0])
	length = len(yes_test[0][0])
	correct_answer_yes = 0
	correct_answer_no = 0
	yes_number = len(yes_test)
	no_number = len(no_test)
	
	#likelihood and prior
	yes_prob = likelihood_3(get_data(yes_data_input))
	no_prob = likelihood_3(get_data(no_data_input))
	prior_yes = float(131) / float(131+141)
	prior_no = 1 - prior_yes
	
	#yes test
	for index in range(0, yes_number):
		prob_yes = 0
		prob_no = 0
		#calculate posterior
		for x in range(0, width):
			order = yes_test[index][x].count(1)
			if yes_prob[x][order] != 0:
				prob_yes += math.log10(yes_prob[x][order])
			if no_prob[x][order] != 0:
				prob_no += math.log10(no_prob[x][order])
		
		#add log-based prior					
		prob_yes += math.log10(prior_yes)
		prob_no += math.log10(prior_no)
		
		#judge accuracy
		if prob_yes > prob_no: correct_answer_yes += 1
	#print result
	result = '= ' + str((float)(correct_answer_yes)/yes_number * 100) + '%'
	print "yes_test accuracy:", correct_answer_yes, '/', yes_number, result
	
	#no test y
	for index in range(0, no_number):
		prob_yes = 0
		prob_no = 0
		#calculate posterior
		for x in range(0, width):
			order = no_test[index][x].count(1)
			if yes_prob[x][order] != 0:
				prob_yes += math.log10(yes_prob[x][order])
			if no_prob[x][order] != 0:
				prob_no += math.log10(no_prob[x][order])
				
		#add log-based prior					
		prob_yes += math.log10(prior_yes)
		prob_no += math.log10(prior_no)		
				
		#judge accuracy		
		if prob_no > prob_yes: correct_answer_no += 1
	#print result
	result = '= ' + str((float)(correct_answer_no)/no_number * 100)+ '%'
	print "no_test accuracy:", correct_answer_no, '/', no_number, result  
	
	
	
#input
yes_data_input = "./part2.1_data/yes_train.txt"
yes_test_input = "./part2.1_data/yes_test.txt"
no_data_input = "./part2.1_data/no_train.txt"
no_test_input = "./part2.1_data/no_test.txt"

#testing classification
yes_test = get_data(yes_test_input)
no_test = get_data(no_test_input)
naive_bayes_classifier_3(yes_test, no_test)
	
	
	