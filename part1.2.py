import math
import time
from scipy.spatial.distance import cosine
#important numbers
NUM_TRAINING = 5000
NUM_TESTING = 1000
NUM_DIGIT = 10
NUM_FEATURE = 784		#28*28
IMG = 28			#Dimension of images
K = 7

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

#convert the images into 1 or 0
def modify_image(data):
	ret = []
	for i in range(len(data)/IMG):
		curr = i*IMG
		temp = []
		for line in range(IMG):
			for pixel in range(IMG):
				if data[curr+line][pixel] == ' ':
					temp.append(0)
				else:
					temp.append(1)
		ret.append(temp)	
	return ret

def Manhattan_distance(setA, setB):
	ret = 0
	for temp in range(len(setA)):
		ret += abs(setA[temp] - setB[temp])
	return ret

def Euclid_distance(setA, setB):
	ret = 0
	for temp in range(len(setA)):
		ret += pow(setA[temp] - setB[temp],2)
	return math.sqrt(ret)

def SupremamDist(A, B):
	temp = []
	for i in range (len(A)):
		temp.append(abs(A[i]-B[i]))
	return max(temp)

def Cosine_distance(A, B):
	return cosine(A, B)
	temp = []
	for i in range (len(A)):
		temp.append(A[i]*B[i])
	dotProduct = sum(temp)
	lengthA = 0
	lengthB = 0
	for j in range (len(A)):
		lengthA += A[j]**2
		lengthB += B[j]**2
	lengthA = math.sqrt(lengthA)
	lengthB = math.sqrt(lengthB)
	return dotProduct/(lengthA*lengthB)

#main classifier function, calculate k nearest distances to each training image of 
#each testing image. 
#then select the most frequent label as prediction result
def classifier(train, test):
	ret = []
	for n in range(NUM_TESTING):	#testing image loop
		distance = [0]*NUM_TRAINING
		for i in range(NUM_TRAINING):	#training image loop
			distance[i] = Cosine_distance(train[i], test[n])	#calculate distane b/t training and testing image
		nearest = []
		for count in range(K):		#get k nearest neighbors
			temp = distance.index(min(distance))
			distance[temp] = float("inf")
			nearest.append(temp)
		nearest_labels = []
		for each in nearest:		#get label of the k nearest neighbors
			nearest_labels.append(train_label[each])
		freq = {}
		for each in nearest_labels:	#calculate frequence of occurance of each label
			if each in freq:
				freq[each] += 1
			else:
				freq[each] = 1
		values = list(freq.values())
		keys = list(freq.keys())
		ret.append(keys[values.index(max(values))])	#get the most frequent label as prediction result
	return ret

def main():
	train_image = modify_image(training)	#modify the image data type
	test_image = modify_image(testing)
	start = time.clock()
	result = classifier(train_image, test_image)	#prediction result
	print "Running time: ", time.clock()-start
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