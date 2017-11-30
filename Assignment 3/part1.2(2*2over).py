import math
import time
#important numbers
NUM_TRAINING = 5000
NUM_TESTING = 1000
NUM_DIGIT = 10
NUM_PIXEL = 784		#28*28
IMG = 28			#Dimension of images

#initiate a dict with size of 729 = 27^2
def init_likelihood():
	ret = {}
	for line in range(27):
		for pixel in range(27):
			ret[line, pixel] = [0]*NUM_DIGIT
	return ret

#update likelihood for every digit class for every pixel location
def likelihoods(image, label, freq):
	ret = []
	for i in range(16):
		temp = init_likelihood()
		ret.append(temp)
	for i in range(NUM_TRAINING):
		curr = IMG * i 		#location of first line current image
		for line in range(27):
			for pixel in range(27):
				index = get_type(image, curr, line, pixel)
				ret[index][line,pixel][label[i]] += 1

	#Laplace Smoothing
	k = 0.1
	v = 16		#feature can take 16 values
	for line in range(27):
		for pixel in range (27):
			for i in range(NUM_DIGIT):
				for index in range(16):
					ret[index][line, pixel][i] = (ret[index][line, pixel][i]+k) / float(freq[i]+k*v)
	return ret

def get_type(image, curr, line, pixel):
	if 	image[curr+line][pixel] == ' ' and image[curr+line][pixel+1] == ' ' \
		and image[curr+line+1][pixel] == ' ' and image[curr+line+1][pixel+1] == ' ':
		return 0	#0000

	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and image[curr+line][pixel+1] == ' ' \
		and image[curr+line+1][pixel] == ' ' and image[curr+line+1][pixel+1] == ' ':
		return 1	#1000
	if 	image[curr+line][pixel] == ' ' and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#')\
		and image[curr+line+1][pixel] == ' ' and image[curr+line+1][pixel+1] == ' ':
		return 2	#0100
	if 	image[curr+line][pixel] == ' ' and image[curr+line][pixel+1] == ' ' \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and image[curr+line+1][pixel+1] == ' ':
		return 3	#0010
	if 	image[curr+line][pixel] == ' ' and image[curr+line][pixel+1] == ' ' \
		and image[curr+line+1][pixel] == ' ' and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 4	#0001

	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#') \
		and image[curr+line+1][pixel] == ' ' and image[curr+line+1][pixel+1] == ' ':
		return 5	#1100
	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and image[curr+line][pixel+1] == ' ' \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and image[curr+line+1][pixel+1] == ' ':
		return 6	#1010
	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and image[curr+line][pixel+1] == ' ' \
		and image[curr+line+1][pixel] == ' ' and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 7	#1001
	if 	image[curr+line][pixel] == ' ' and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#')\
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and image[curr+line+1][pixel+1] == ' ':
		return 8	#0110
	if 	image[curr+line][pixel] == ' ' and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#')\
		and image[curr+line+1][pixel] == ' ' and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 9	#0101
	if 	image[curr+line][pixel] == ' ' and image[curr+line][pixel+1] == ' ' \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 10	#0011

	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#') \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and image[curr+line+1][pixel+1] == ' ':
		return 11	#1110
	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#') \
		and image[curr+line+1][pixel] == ' ' and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 12	#1101
	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and image[curr+line][pixel+1] == ' ' \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 13	#1011
	if 	image[curr+line][pixel] == ' ' and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#') \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 14	#0111

	if 	(image[curr+line][pixel] == '+' or image[curr+line][pixel] == '#') and (image[curr+line][pixel+1] == '+' or image[curr+line][pixel+1] == '#') \
		and (image[curr+line+1][pixel] == '+' or image[curr+line+1][pixel] == '#') and (image[curr+line+1][pixel+1] == '+' or image[curr+line+1][pixel+1] == '#'):
		return 15

#number of occurance
def frequency(label):
	ret = []
	for i in range(NUM_DIGIT):
		temp = label.count(i)
		ret.append(temp)
	return ret

#Maximum a posterior classification
def MAP(likelihood, prior, image):
	classification = []			#final classification result of each image
	for n in range(NUM_TESTING):	#image loop, 1000
		curr = IMG * n
		posterior = []				#list of posteriors of current image
		for i in range(NUM_DIGIT):	#digit loop, 10
			temp = math.log(prior[i])	#Prior
			for line in range(27):		#row loop, 28
				for pixel in range(27):	#column loop, 28
					index = get_type(image, curr, line, pixel)
					temp += math.log(likelihood[index][line, pixel][i])
			posterior.append(temp)
		classification.append(posterior.index(max(posterior)))
	return	classification

#NAC
def naive_bayes_classifier():
	freq = frequency(train_label)		#frequency of occurance of training images
	prior = []							#P(class): emprical frequency of each class
	test_freq = frequency(test_label)	#frequency of occurance of testing images
	total_num_correct = 0				#count total correctness rate

################	Training 	#####################
	t = time.clock()
	#P(F | class): likelihood for every pixel location for every digit class
	likelihood = likelihoods(training, train_label, freq)		
	for i in range(NUM_DIGIT):
		prior.append(freq[i]/float(NUM_TRAINING))
	print time.clock() - t
################	Testing 	#####################
	t = time.clock()
	result= MAP(likelihood, prior, testing)
	print time.clock() - t
################	Evaluation	#####################

	for i in range(NUM_TESTING):
		if result[i] == test_label[i]:
			total_num_correct +=1 

################	Results		#####################
	#Basic Statistics
	print 	"Total Classification Rate: ", total_num_correct/float(NUM_TESTING)*100, \
			"%. Out of 1000 images. "

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