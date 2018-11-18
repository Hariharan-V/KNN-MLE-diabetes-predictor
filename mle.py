import csv
import numpy as np
import sys
import random
import math

##get csv to read the file into a list
reader = csv.reader(open("pima-indians-diabetes.csv", "rb"), delimiter=",")
raw_list = list(reader)
# make a list of list of floats with all attributes
float_list = map(lambda x: map(lambda y: float(y),x),raw_list[9:])
#shuffle the float_list to randomly split
accuracy = []

for j in range(20):
	correct = 0
	incorrect = 0
	random.shuffle(float_list)


	#split data
	training_data_float = float_list[:len(float_list)//2	]
	test_data_float = float_list[len(float_list)//2:]

	## training the model
	train_class_zero = np.array(map(lambda x: [x[1],x[2],x[3]]  , filter(lambda x: x[8]==0,training_data_float)))
	train_class_one = np.array(map(lambda x: [x[1],x[2],x[3]]  , filter(lambda x: x[8]==1,training_data_float)))
	class_zero_mean= train_class_zero.mean(0)
	class_one_mean = train_class_one.mean(0)
	class_zero_cov = np.cov(train_class_zero.T)
	class_one_cov = np.cov(train_class_one.T)
	prior_class_zero = float(len(train_class_zero))/(float(len(train_class_zero))+float(len(train_class_one)))
	prior_class_one = float(len(train_class_one))/(float(len(train_class_zero))+float(len(train_class_one)))

	def distribution_class_zero(vect):
		# print(np.dot(np.dot(np.subtract(vect,class_zero_mean),np.linalg.inv(class_zero_cov)),np.subtract(vect,class_zero_mean).T))
		return (1.0/math.pow((2*math.pi),1.5))*math.pow(np.linalg.det(class_zero_cov),-0.5)*math.exp(-0.5*np.dot(np.dot(np.subtract(vect,class_zero_mean),np.linalg.inv(class_zero_cov)),np.subtract(vect,class_zero_mean).T))

	def distribution_class_one(vect):
		# print(np.dot(np.dot(np.subtract(vect,class_zero_mean),np.linalg.inv(class_zero_cov)),np.subtract(vect,class_zero_mean).T))
		return (1.0/math.pow((2*math.pi),1.5))*math.pow(np.linalg.det(class_one_cov),-0.5)*math.exp(-0.5*np.dot(np.dot(np.subtract(vect,class_one_mean),np.linalg.inv(class_one_cov)),np.subtract(vect,class_one_mean).T))




	#testing the model

	for i in range(len(test_data_float)):
		test_vect = np.array([test_data_float[i][1],test_data_float[i][2],test_data_float[i][3]])
		d0 = distribution_class_zero(test_vect)*prior_class_zero
		d1 = distribution_class_one(test_vect)*prior_class_one
		if(d0>d1 and test_data_float[i][8]==0):
			correct = correct+1
		elif(d0<d1 and test_data_float[i][8]==1):
			correct = correct+1
		else:
			incorrect = incorrect+1

	accuracy.append(float(correct)/float(correct+incorrect))

accuracy_mat = np.array(accuracy)


print(("Mean Accuracy: ") + str(accuracy_mat.mean(0)))

print(("Standard deviation of Accuracy: ")+ str(accuracy_mat.std()))

		



