import math
import time
#important numbers
NUM_TRAINING = 5000
NUM_TESTING = 1000
NUM_DIGIT = 10
NUM_PIXEL = 784		#28*28
IMG = 28			#Dimension of images

#initiate a dict with size of 784 = 28^2
def init_likelihood():
	ret = {}
	for line in range(IMG):
		for pixel in range(IMG):
			ret[line, pixel] = [0]*NUM_DIGIT
	return ret

#initiate a dict with isze of 100 = 10^2
def init_matrix():
	ret = {}
	for row in range(NUM_DIGIT):
		for column in range(NUM_DIGIT):
			ret[row, column] = 0
	return ret

#initiate a matrix with size of 10
def init_posterior():
	ret = []
	for i in range(NUM_DIGIT):
		temp = [0, 0]
		ret.append(temp)
	return ret

#update likelihood for every digit class for every pixel location
def likelihoods(image, label, freq):
	fore = init_likelihood()
	back = init_likelihood()
	for i in range(NUM_TRAINING):
		curr = IMG * i 		#location of first line current image
		for line in range(IMG):
			for pixel in range(IMG):
				if image[curr+line][pixel] == '#' or image[curr+line][pixel] == '+':
					fore[line, pixel][label[i]] += 1
				else:
					back[line, pixel][label[i]] += 1
	#Laplace Smoothing
	k = 0.1
	v = 2		#feature can only take 1 or 0
	for line in range(IMG):
		for pixel in range (IMG):
			for i in range(NUM_DIGIT):
				fore[line,pixel][i] = (fore[line, pixel][i]+k) / float(freq[i]+k*v)
				back[line,pixel][i] = (back[line, pixel][i]+k) / float(freq[i]+k*v)
	return fore, back

#number of occurance
def frequency(label):
	ret = []
	for i in range(NUM_DIGIT):
		temp = label.count(i)
		ret.append(temp)
	return ret

#Maximum a posterior classification
def MAP(fore, back, prior, image):
	classification = []			#final classification result of each image
	posterior_table = []		#posteriors of each digit class of each image
	for n in range(NUM_TESTING):	#image loop, 1000
		curr = IMG * n
		posterior = []				#list of posteriors of current image
		for i in range(NUM_DIGIT):	#digit loop, 10
			temp = math.log(prior[i])	#Prior
			for line in range(IMG):		#row loop, 28
				for pixel in range(IMG):	#column loop, 28
					if image[curr+line][pixel] == '#' or image[curr+line][pixel] == '+':
						temp += math.log(fore[line, pixel][i])
					else:
						temp += math.log(back[line, pixel][i])
			posterior.append(temp)
		posterior_table.append(posterior)
		classification.append(posterior.index(max(posterior)))
	return	classification, posterior_table

#find highest and lowest posterior for each digit class
def min_max_posterior(p_table, test_label):
	ret = init_posterior()	#record images with highest and lowest posteriors for each class
	minimum = [-1]*10		#list of minimum posteriors of each class
	maximum = [-1]*10		#list of maximum posteriors of each class
	for n in range(NUM_TESTING):
		for i in range(NUM_DIGIT):
			if test_label[n] == i:
				if maximum[i] == -1 and minimum[i] == -1:	#assign initial value
					maximum[i] = p_table[n][i]
					minimum[i] = p_table[n][i]
				if p_table[n][i] > maximum[i]:				#min()
					ret[i][0] = n
					maximum[i] = p_table[n][i]
				if p_table[n][i] < minimum[i]:				#max()
					ret[i][1] = n
					minimum[i] = p_table[n][i]
	return ret

#print a 28*28 image
def print_image(index):
	location = index*IMG
	for i in range(location, location+IMG):
		temp = ''.join(str(e) for e in testing[i])
		print temp

#print ASCII log likelihood map for a digit class
def print_likelihood_map(likelihood, digit):
	for i in range(IMG):
		for j in range(IMG):
			temp = math.log(likelihood[i, j][digit])
			if temp > -1:
				print '+',
			if temp < -1 and temp > -3:
				print '-',
			if temp < -3:
				print ' ',
		print"	"

def print_odd_ratio_map(likelihood, digit1, digit2):
	for i in range(IMG):
		for j in range(IMG):
			temp = math.log(likelihood[i, j][digit1]/likelihood[i, j][digit2])
			if temp > 0:
				print '+',
			if temp < 0 and temp > -2:
				print '-',
			if temp < -2:
				print ' ',
		print"	"

#NAC
def naive_bayes_classifier():
	freq = frequency(train_label)		#frequency of occurance of training images
	prior = []							#P(class): emprical frequency of each class
	test_freq = frequency(test_label)	#frequency of occurance of testing images
	classification_rate = [0]*10		#table to count correctness of each class
	confusion_matrix = init_matrix()	#confusion matrix for each class
	total_num_correct = 0				#count total correctness rate

################	Training 	#####################
	t = time.clock()
	#P(F | class): likelihood for every pixel location for every digit class
	fore_likelihood, back_likelihood = likelihoods(training, train_label, freq)		
	for i in range(NUM_DIGIT):
		prior.append(freq[i]/float(NUM_TRAINING))
	print time.clock() - t
################	Testing 	#####################
	t = time.clock()
	result, posterior_table = MAP(fore_likelihood, back_likelihood, prior, testing)
	print time.clock() - t
################	Evaluation	#####################

	for i in range(NUM_TESTING):
		if result[i] == test_label[i]:
			total_num_correct +=1 
			classification_rate[test_label[i]] += 1
		else:
			confusion_matrix[test_label[i], result[i]] += 1
	#highest and lowest posteriors for each class
	posterior_record = min_max_posterior(posterior_table, test_label)

################	Results		#####################
	#Basic Statistics
	# print 	"Total Classification Rate: ", total_num_correct/float(NUM_TESTING)*100, \
	# 		"%. Out of 1000 images. "
	# for i in range(NUM_DIGIT):
	# 	print 	"Classification Rate for ", i, ": ", round(classification_rate[i]/float(test_freq[i])*100, 1), \
	# 			"%. Out of ", test_freq[i], "images. "	#rate ronuded to 1 decimal places

	#Confusion Matrix
	# print "Confusion Matrix:"
	# print "	0	1	2	3	4	5	6	7	8	9"
	# for r in range(NUM_DIGIT):
	# 	print r, 	"	", round(confusion_matrix[r,0]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,1]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,2]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,3]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,4]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,5]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,6]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,7]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,8]/float(test_freq[r])*100,1), "%"\
	# 				"	", round(confusion_matrix[r,9]/float(test_freq[r])*100,1), "%"

	#Test Examples with Highest and Lowest Posterior Probabilities for each Class
	# for i in range(NUM_DIGIT):
	# 	print "Digit Class ", i
	# 	print "Most Prototypical Index:	", posterior_record[i][0]
	# 	print_image(posterior_record[i][0])
	# 	print "Least Prototypical Index:	", posterior_record[i][1]
	# 	print_image(posterior_record[i][1])

	#Odd Ratios
	#Four pairs with highest confusion rate:	(4,9), (8,3), (7,9), (5,3)
	# print_likelihood_map(fore_likelihood, 4)
	# print "	"
	# print_likelihood_map(fore_likelihood, 9)
	# print "	"
	# print_odd_ratio_map(fore_likelihood, 4, 9)


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

naive_bayes_classifier()	#main function