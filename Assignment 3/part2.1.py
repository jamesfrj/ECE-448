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
		# line 26,27, 28 is left blank
		if count == 26 or count == 27: continue
		if count == 28: 
			count = 0
			dataset.append(data)
			data = []
			continue 
		for each in line:
			# regard % as 0, blank as 1
			if each == '%': temp.append(0)
			elif each == ' ': 
				temp.append(1)
				high_ener_count += 1
		data.append(temp)
	file.close()
	
	return dataset

# P(class | document) = P(document | class) * P(class) 
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
			#laplance smooth k = 7.6 v = 15.2
			temp[y] += 7.6
			temp[y] /= (num_of_data + 15.2)
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
	
	#yes no class likelihood
	yes_prob = likelihood(get_data(yes_data_input))
	no_prob = likelihood(get_data(no_data_input))
	#yes no class prior 
	prior_yes = float(131) / float(131+141)
	prior_no = 1 - prior_yes
	
	#yes test
	for index in range(0, yes_number):
		prob_yes = 0
		prob_no = 0
		# calculate the posterior
		# log based add is equal to multiply
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
	#print accuracy
	result = '= ' + str((float)(correct_answer_yes)/yes_number * 100) + '%'
	print "yes_test accuracy:", correct_answer_yes, '/', yes_number, result
	
	#no test y
	for index in range(0, no_number):
		prob_yes = 0
		prob_no = 0
		# calculate posterior
		# log based add is equal to multiply
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
	#print accuracy
	result = '= ' + str((float)(correct_answer_no)/no_number * 100)+ '%'
	print "no_test accuracy:", correct_answer_no, '/', no_number, result  
	
	
	
#input
yes_data_input = "./part2.1_data/yes_train.txt"
yes_test_input = "./part2.1_data/yes_test.txt"
no_data_input = "./part2.1_data/no_train.txt"
no_test_input = "./part2.1_data/no_test.txt"

#classification test
yes_test = get_data(yes_test_input)
no_test = get_data(no_test_input)
naive_bayes_classifier(yes_test, no_test)
	
	
	