import math
import random
#important numbers
NUM_TRAINING = 5000
NUM_TESTING = 1000
NUM_DIGIT = 10
NUM_FEATURE = 784		#28*28
IMG = 28			#Dimension of images
#Hyper-parameters
ALPHA = 1
BIAS = False			#True for using bias, False for not using bias
BIAS_NUM = 1
INIT_WEIGHT = False		#True for random, False for zeros
WEIGHT_RANGE = 2
TRAIN_ORDER = True		#True for random, False for fixed
EPOCH = 50

#number of occurance
def frequency(label):
	ret = []
	for i in range(NUM_DIGIT):
		temp = label.count(i)
		ret.append(temp)
	return ret

#initiate a dict with isze of 100 = 10^2
def init_matrix():
	ret = {}
	for row in range(NUM_DIGIT):
		for column in range(NUM_DIGIT):
			ret[row, column] = 0
	return ret

#initiate a 3D matrix [digit][line][pixel]
def init_weight():
	ret = []
	if INIT_WEIGHT:	#randomly initial weights
		for i in range(NUM_DIGIT):
			temp = []
			for n in range(IMG):
				temp.append([random.randint(0,WEIGHT_RANGE)]*IMG)
			ret.append(temp)
	else:			#all weights set to zero
		for i in range(NUM_DIGIT):
			temp = []
			for n in range(IMG):
				temp.append([0]*IMG)
			ret.append(temp)
	return ret

#return 1 if foreground, return 0 if background
def identifier(stuff):
	if stuff == '#' or  stuff == '+':
		return 1
	else:
		return 0

#train function, go through training set epoch times to update weights
def train(weight):
	epoch = 0
	bias = [BIAS_NUM]*10
	while epoch < EPOCH:	#iteration epoch number of times
		if not TRAIN_ORDER:	#train the set in fixed order
			for i in range(NUM_TRAINING):
				curr = i*IMG
				y = [0]*NUM_DIGIT
				for n in range(NUM_DIGIT):
					for line in range(IMG):
						for pixel in range(IMG):
							y[n] += weight[n][line][pixel]*identifier(training[curr+line][pixel])
					if BIAS:	#add bias to the y
						y[n] += bias[n]
				result = y.index(max(y))
				if result != train_label[i]:	#test if need update weight and bias
					for line in range(IMG):
						for pixel in range(IMG):
							weight[train_label[i]][line][pixel] += (ALPHA/(ALPHA+float(epoch)))*identifier(training[curr+line][pixel])
							weight[result][line][pixel] -= (ALPHA/(ALPHA+float(epoch)))*identifier(training[curr+line][pixel])
					if BIAS:	#update bias number
						bias[train_label[i]] += (ALPHA/(ALPHA+float(epoch)))
						bias[result] -= (ALPHA/(ALPHA+float(epoch)))
		if TRAIN_ORDER:		#train the set randomly
			index = []
			for num in range(NUM_TRAINING):
				index.append(num)
			random.shuffle(index)
			for i in index:
				curr = i*IMG
				y = [0]*NUM_DIGIT
				for n in range(NUM_DIGIT):
					for line in range(IMG):
						for pixel in range(IMG):
							y[n] += weight[n][line][pixel]*identifier(training[curr+line][pixel])
					if BIAS:
						y[n] += bias[n]
				result = y.index(max(y))
				if result != train_label[i]:
					for line in range(IMG):
						for pixel in range(IMG):
							weight[train_label[i]][line][pixel] += (ALPHA/(ALPHA+float(epoch)))*identifier(training[curr+line][pixel])
							weight[result][line][pixel] -= (ALPHA/(ALPHA+float(epoch)))*identifier(training[curr+line][pixel])
					if BIAS:
						bias[train_label[i]] += (ALPHA/(ALPHA+float(epoch)))
						bias[result] -= (ALPHA/(ALPHA+float(epoch)))
		epoch += 1
	#Evaluate train set accuracy
	num_correct = 0
	for i in range(NUM_TRAINING):
		curr = i*IMG
		y = [0]*NUM_DIGIT
		for n in range(NUM_DIGIT):
			for line in range(IMG):
				for pixel in range(IMG):
					y[n] += weight[n][line][pixel]*identifier(training[curr+line][pixel])
			if BIAS:
				y[n] += bias[n]
		result = y.index(max(y))
		if result == train_label[i]:
			num_correct += 1
	print 	"Traing Classification Rate: ", num_correct/float(NUM_TRAINING)*100, \
			"%. Out of 5000 images. "
	return weight, bias

#test function, go through the testing function to evaluate the overall accuracy
def test(weight, bias):
	ret = []
	for i in range(NUM_TESTING):
		curr = i*IMG
		y = [0]*NUM_DIGIT
		for n in range(NUM_DIGIT):
			for line in range(IMG):
				for pixel in range(IMG):
					y[n] += weight[n][line][pixel]*identifier(testing[curr+line][pixel])
			if BIAS:	#test it use bias
				y[n] += bias[n]
		ret.append(y.index(max(y)))	#append prediction of the algorithm
	return ret

#main classifier function
def main():
	weight = init_weight()
	weight, bias = train(weight)
	result = test(weight, bias)
	num_correct = 0
	confusion_matrix = init_matrix()	#confusion matrix for each class
	test_freq = frequency(test_label)	#frequency of occurance of testing images
	for i in range(NUM_TESTING):
		if result[i] == test_label[i]:
			num_correct +=1 
		else:
			confusion_matrix[test_label[i], result[i]] += 1

	#Basic Statistics
	print 	"Testing Classification Rate: ", num_correct/float(NUM_TESTING)*100, \
			"%. Out of 1000 images. "

	#Confusion Matrix
	print "Confusion Matrix:"
	print "	0	1	2	3	4	5	6	7	8	9"
	for r in range(NUM_DIGIT):
		print r, 	"	", round(confusion_matrix[r,0]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,1]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,2]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,3]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,4]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,5]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,6]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,7]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,8]/float(test_freq[r])*100,1), "%"\
					"	", round(confusion_matrix[r,9]/float(test_freq[r])*100,1), "%"

################	Data		######################
filename = 'trainingimages'
f = open(filename,'r')
training_images = f.readlines()
f.close()
training = []
for each in training_images:
	array = list(each)
	array.remove('\n')
	training.append(array)
#training is a list contain each line of the trainingimages exec file

filename = 'traininglabels'
f = open(filename,'r')
training_labels = f.readlines()
f.close()
train_label = []
for each in training_labels:
	num = int(each[0])
	train_label.append(num)
#train_label is a list contain labels of the traininglabels exec file

filename = 'testimages'
f = open(filename,'r')
testing_images = f.readlines()
f.close()
testing = []
for each in testing_images:
	array = list(each)
	array.remove('\n')
	testing.append(array)
#testing is a list contain each line of the testingimages exec file

filename = 'testlabels'
f = open(filename,'r')
testing_labels = f.readlines()
f.close()
test_label = []
for each in testing_labels:
	num = int(each[0])
	test_label.append(num)
#test_label is a list contain labels of the testinglabels exec file

main()