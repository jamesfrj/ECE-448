import math
import time
#important numbers
NUM_TRAINING = 451
NUM_TESTING = 150
NUM_FACE = 2
NUM_PIXEL = 4200		#70*60
IMG_H = 70			#Dimension of images
IMG_W = 60

#initiate a dict with size of 4200
def init_likelihood():
	ret = {}
	for line in range(IMG_H):
		for pixel in range(IMG_W):
			ret[line, pixel] = [0]*NUM_FACE
	return ret

#initiate a matrix with size of 10
def init_posterior():
	ret = []
	for i in range(NUM_FACE):
		temp = [0, 0]
		ret.append(temp)
	return ret

#update likelihood for every digit class for every pixel location
def likelihoods(image, label, freq):
	fore = init_likelihood()
	back = init_likelihood()
	for i in range(NUM_TRAINING):
		curr = IMG_H * i 		#location of first line current image
		for line in range(IMG_H):
			for pixel in range(IMG_W):
				if image[curr+line][pixel] == '#':
					fore[line, pixel][label[i]] += 1
				else:
					back[line, pixel][label[i]] += 1
	#Laplace Smoothing
	k = 1
	v = 2		#feature can only take 1 or 0
	for line in range(IMG_H):
		for pixel in range (IMG_W):
			for i in range(NUM_FACE):
				fore[line,pixel][i] = (fore[line, pixel][i]+k) / float(freq[i]+k*v)
				back[line,pixel][i] = (back[line, pixel][i]+k) / float(freq[i]+k*v)
	return fore, back

#number of occurance
def frequency(label):
	ret = []
	for i in range(NUM_FACE):
		temp = label.count(i)
		ret.append(temp)
	return ret

#Maximum a posterior classification
def MAP(fore, back, prior, image):
	classification = []			#final classification result of each image
	for n in range(NUM_TESTING):	#image loop, 1000
		curr = IMG_H * n
		posterior = []				#list of posteriors of current image
		for i in range(NUM_FACE):	#digit loop, 10
			temp = math.log(prior[i])	#Prior
			for line in range(IMG_H):		#row loop, 28
				for pixel in range(IMG_W):	#column loop, 28
					if image[curr+line][pixel] == '#':
						temp += math.log(fore[line, pixel][i])
					else:
						temp += math.log(back[line, pixel][i])
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

	#P(F | class): likelihood for every pixel location for every digit class
	fore_likelihood, back_likelihood = likelihoods(training, train_label, freq)		
	for i in range(NUM_FACE):
		prior.append(freq[i]/float(NUM_TRAINING))

################	Testing 	#####################

	result = MAP(fore_likelihood, back_likelihood, prior, testing)

################	Evaluation	#####################

	for i in range(NUM_TESTING):
		if result[i] == test_label[i]:
			total_num_correct +=1 

################	Results		#####################
	#Basic Statistics
	print 	"Total Classification Rate: ", total_num_correct/float(NUM_TESTING)*100, \
			"%. Out of 1000 images. "

################	Data		######################
filename = 'facedatatrain'
f = open(filename,'r')
training_images = f.readlines()
f.close()
training = []
for each in training_images:
	array = list(each)
	array.remove('\n')
	training.append(array)
#training is a list contain each line of the trainingimages exec file

filename = 'facedatatrainlabels'
f = open(filename,'r')
training_labels = f.readlines()
f.close()
train_label = []
for each in training_labels:
	num = int(each[0])
	train_label.append(num)
#train_label is a list contain labels of the traininglabels exec file

filename = 'facedatatest'
f = open(filename,'r')
testing_images = f.readlines()
f.close()
testing = []
for each in testing_images:
	array = list(each)
	array.remove('\n')
	testing.append(array)
#testing is a list contain each line of the testingimages exec file

filename = 'facedatatestlabels'
f = open(filename,'r')
testing_labels = f.readlines()
f.close()
test_label = []
for each in testing_labels:
	num = int(each[0])
	test_label.append(num)
#test_label is a list contain labels of the testinglabels exec file

naive_bayes_classifier()	#main function