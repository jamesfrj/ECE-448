import math
import numpy

#data loader
def get_data_2(filename):
	dataset = []
	data = []
	file = open(filename, "r")
	count = 0
	for line in file:
		count += 1	
		temp = []
		#line 31, 32, 33 are left blank
		if count == 31 or count == 32: continue
		if count == 33: 
			count = 0
			dataset.append(data)
			data = []
			continue
		#regard % as 0, blank as 1 
		for each in line:
			if each == '%': temp.append(0)
			elif each == ' ': temp.append(1)
		data.append(temp)
		
	file.close()
	return dataset

def get_label_2(filename):
	#get corresponding label list for data
	label = []
	file = open(filename, "r")
	for line in file:
		for each in line:
			#edge case
			if each != '\n' and each != '\r': label.append(each)	
	return label
 
def likelihood_2(data, label, labels):
	total = []
	num_of_data = len(data)
	width = len(data[0])
	length = len(data[0][0])
	for x in range(0, width):
		temp = [0]*13
		for y in range(0, length):
			for index in range(0, num_of_data): 
				if label == int(labels[index]): 
					temp[y] += data[index][x][y]
			#laplace smooth constant k = 0.8 v = 2
			temp[y] += 0.8
			temp[y] /= (12+1.6)
		total.append(temp)		
	return total			

def naive_bayes_classifier_2(test, label):
	#setup the test data
	test_number = len(test)
	width = len(test[0])
	length = len(test[0][0])
	prior = 0.2
	predict_label = []
	training_label = get_label_2(training_label_input)
	
	#likelihood for audio class 1-5
	like_1 = likelihood_2(training_data, 1, training_label)
	like_2 = likelihood_2(training_data, 2, training_label)
	like_3 = likelihood_2(training_data, 3, training_label)
	like_4 = likelihood_2(training_data, 4, training_label)
	like_5 = likelihood_2(training_data, 5, training_label)
	

	correct_answer = 0

	for index in range(0, test_number):
		prob_1 = 0
		prob_2 = 0
		prob_3 = 0
		prob_4 = 0
		prob_5 = 0
		prob_audio = []
		#calculate posterior
		for x in range(0, width):
			for y in range(0, length):
				if test[index][x][y] == 1:		
					prob_1 += math.log10(like_1[x][y])
					prob_2 += math.log10(like_2[x][y])
					prob_3 += math.log10(like_3[x][y])					
					prob_4 += math.log10(like_4[x][y])					
					prob_5 += math.log10(like_5[x][y])			
		
		#add log-based prior		
		prob_1 += math.log10(prior)
		prob_2 += math.log10(prior)
		prob_3 += math.log10(prior)
		prob_4 += math.log10(prior)
		prob_5 += math.log10(prior)	
		
		#get largest posterior
		prob_audio.append(prob_1)
		prob_audio.append(prob_2)
		prob_audio.append(prob_3)
		prob_audio.append(prob_4)
		prob_audio.append(prob_5)
		predict = numpy.argmax(prob_audio)+1
		
		#judge accuracy
		if predict == int(label[index]): correct_answer += 1
		predict_label.append(predict)
	#print result
	result = '= ' + str((float)(correct_answer)/test_number * 100) + '%'
	print "testing accuracy:", correct_answer, '/', test_number, result
	
	#for index in range(0, len(predict_label)):
		#print "corect label", label[index], "predict: ", predict_label[index] 
	
	
#input
training_data_input = "./part2.2_data/training_data.txt"
training_label_input = "./part2.2_data/training_labels.txt"
testing_data_input = "./part2.2_data/testing_data.txt"
testing_labels_input = "./part2.2_data/testing_labels.txt"

#training data
training_data = get_data_2(training_data_input)


#testing data
testing_data = get_data_2(testing_data_input)
testing_label = get_label_2(testing_labels_input)

#testing classification
naive_bayes_classifier_2(testing_data, testing_label)
	
	
