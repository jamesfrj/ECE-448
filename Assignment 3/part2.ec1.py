import math
import os

#data loader
def get_train_data(directory):
	dataset = []
	yes_train = []
	no_train = []
	#read each file in the directory
	for filename in os.listdir(directory):
		file = open(directory + filename, "r")
		order = []
		for index in range(0, len(filename)):
			if filename[index] == '0' or filename[index] =='1':
				order.append(filename[index])

		data = []
		high_ener = 0
		#regard % as 0, blank as 1
		for line in file:	
			temp = [] 
			count = 0
			for each in line: 
				if each == '%': temp.append(0)
				elif each == ' ': 
					temp.append(1)
					high_ener += 1
			data.append(temp)
			
		file.close()
		
		avl_high_ener = float(high_ener) / 8
		#split the garbage out
		train_data = throw_garbage_away(data, avl_high_ener)
		
		#if 8 spectrogram generated, the data is truly useful
		if len(train_data) == 8:
			#divide the useful data into corresponding class(yes or no)
			for index in range(0, len(order)):
				if order[index] == '1': yes_train.append(train_data[index])
				else: no_train.append(train_data[index])
		
	
	return yes_train, no_train

def get_test_data(directory):
	dataset = []
	#read each file in directory
	for filename in os.listdir(directory):
		file = open(directory + filename, "r")
		data = []
		#regard % as 0, blank as 1
		for line in file:	
			temp = [] 
			count = 0
			for each in line: 
				if each == '%': temp.append(0)
				elif each == ' ': temp.append(1)
			data.append(temp)
		file.close()
		dataset.append(data)
		
	return dataset

		

def throw_garbage_away(raw_dataset, high_ener):
	
	row = len(raw_dataset)
	col = len(raw_dataset[0])
	dataset = []
	x = 0
	flag = False
	while x < col:
		high_ener_count = 0
		for y in range(0, row):
			if raw_dataset[y][x] == 1: high_ener_count += 1
			
		#a useful spectrofram might start at this column
		if high_ener_count != 0:
			data = []
			high_ener_count = 0
			for record_y in range(0, row):
				temp = []
				# edge case
				if x + 10 >= col: continue
				#store the data
				for record_x in range(x, x + 10):
					temp.append(raw_dataset[record_y][record_x])
					if raw_dataset[record_y][record_x] == 1: high_ener_count += 1
				data.append(temp)	
						
			#23 is the offset to increase the accuracy of throwing garbage
			if high_ener_count >= high_ener - 23: 
				x += 10
				flag = True
				dataset.append(data)
		
		if flag == False: x += 1
		else: flag = False
	
	return dataset		

## P(class | document) = P(document | class) * P(class) 
def likelihood(data):
	total = []
	num_of_data = len(data)
	width = len(data[0])
	length = len(data[0][0])
	for x in range(0, width):
		temp = [0]*10
		for y in range(0, length):
			for item in data: temp[y] += item[x][y]
			temp[y] = (float)(temp[y])
			#laplace smooth constant k = 0.4, v = 2
			temp[y] += 0.4 
			temp[y] /= (num_of_data+0.8)
		total.append(temp)			
	return total			

def naive_bayes_classifier(yes_test, no_test):
	#setup the test data
	width = len(yes_test[0])
	length = len(yes_test[0][0])
	correct_answer_yes = 0
	correct_answer_no = 0
	yes_number = len(yes_test)
	no_number = len(no_test)
	
	#likelihood and prior
	yes_prob = likelihood(get_train_data("./part2.ec_data/training/")[0])
	no_prob = likelihood(get_train_data("./part2.ec_data/training/")[1])
	prior_yes = float(192) / float(192+160)
	prior_no = 1 - prior_yes
	
	#yes test
	for index in range(0, yes_number):
		prob_yes = 0
		prob_no = 0
		for x in range(0, width):
			for y in range(0, length):
				if yes_test[index][x][y] == 1:
					if yes_prob[x][y] != 0:
						prob_yes += math.log10(yes_prob[x][y])
					if no_prob[x][y] != 0:
						prob_no += math.log10(no_prob[x][y])
							
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
		for x in range(0, width):
			for y in range(0, length):
				if no_test[index][x][y] == 1:
					if yes_prob[x][y] != 0:
						prob_yes += math.log10(yes_prob[x][y])
					if no_prob[x][y] != 0:
						prob_no += math.log10(no_prob[x][y])
							
		prob_yes += math.log10(prior_yes)
		prob_no += math.log10(prior_no)		
		#judge accuracy		
		if prob_no > prob_yes: correct_answer_no += 1
	#print result 	
	result = '= ' + str((float)(correct_answer_no)/no_number * 100)+ '%'
	print "no_test accuracy:", correct_answer_no, '/', no_number, result  
	
	
	
#input
get_train_data("./part2.ec_data/training/")
yes_test = get_test_data("./part2.ec_data/yes_test/")
no_test = get_test_data("./part2.ec_data/no_test/")

#testing classification
naive_bayes_classifier(yes_test, no_test)