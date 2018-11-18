import numpy as np
import math
import random
import csv

reader = csv.reader(open("pima-indians-diabetes.csv", "rb"), delimiter=",")
raw_list = list(reader)
# make a list of list of floats with all attributes

float_list = map(lambda x: map(lambda y: float(y),x),raw_list[9:])

#shuffle the float_list to randomly split
total_list = []
k_list = [1,5,11]
k_accuracy = [[],[],[]]
for j in range(3):
  for g in range(20):
    correct = 0
    incorrect = 0
    random.shuffle(float_list)


      #split data
    training_data_float = float_list[:len(float_list)//2  ]
    test_data_float = float_list[len(float_list)//2:]

    #rescale training data
    min_list = [ float("inf"), float("inf"), float("inf")]
    max_list = [float("-inf"),float("-inf"),float("-inf")]
    for i in range(len(training_data_float)):

      if(training_data_float[i][1]<min_list[0]):
        min_list[0] = training_data_float[i][1]

      if(training_data_float[i][1]>max_list[0]):  
        max_list[0] = training_data_float[i][1]

      
      if(training_data_float[i][2]<min_list[1]):
        min_list[1] = training_data_float[i][2]

      if(training_data_float[i][2]>max_list[1]):
        max_list[1] = training_data_float[i][2]

      if(training_data_float[i][3]<min_list[2]):
        min_list[2] = training_data_float[i][3]

      if(training_data_float[i][3]>max_list[2]):
        max_list[2] = training_data_float[i][3]
    # min_list = [0.0,0.0,0.0]
    # max_list = [1.0,1.0,1.0]
    distance = []
    for i in range(len(training_data_float)):
      training_data_float[i][1] = (training_data_float[i][1]-min_list[0])/(max_list[0]-min_list[0])
      training_data_float[i][2] = (training_data_float[i][2]-min_list[1])/(max_list[1]-min_list[1])
      training_data_float[i][3] = (training_data_float[i][3]-min_list[2])/(max_list[2]-min_list[2])
    #testing
     
    # min_list = [0.0,0.0,0.0]
    # max_list = [1.0,1.0,1.0]

    def count_k(distance,k):
      distance = distance[0:k]
      # print(distance)
      return {'class0':len(filter(lambda x: x[1]==0,distance)),
              'class1':len(filter(lambda x: x[1]==1,distance)) }

    for i in  range(len(test_data_float)): 
      test_data_float[i][1] = (test_data_float[i][1]-min_list[0])/(max_list[0]-min_list[0])
      test_data_float[i][2] = (test_data_float[i][2]-min_list[1])/(max_list[1]-min_list[1])
      test_data_float[i][3] = (test_data_float[i][3]-min_list[2])/(max_list[2]-min_list[2])
      distance = map(lambda x: [(math.sqrt(math.pow(test_data_float[i][1]-x[1],2.0)+math.pow(test_data_float[i][2]-x[2],2.0)+math.pow(test_data_float[i][3]-x[3],2.0))),x[8]],training_data_float)

      distance=sorted(distance,key = lambda ele : ele[0])
      # print(distance)
      cc = count_k(distance,k_list[j])
      # print(cc)
      if(cc['class0']>cc['class1'] and test_data_float[i][8]==0.0):
        correct = correct+1
      elif (cc['class0']<cc['class1'] and test_data_float[i][8]==1.0):
        correct = correct+1
      else:
        incorrect = incorrect+1
    total_list.append(float(correct)/float(correct+incorrect))
    k_accuracy[j].append(float(correct)/float(correct+incorrect))

t_mat  = np.array(total_list)
k_one = np.array(k_accuracy[0])
k_five = np.array(k_accuracy[1])
k_eleven = np.array(k_accuracy[2])

print("Mean accuracy for K = 1: "+str(k_one.mean(0)))
print("STD accuracy for K = 1: "+str(k_one.std()))
print("Mean accuracy for K = 5: "+str(k_five.mean(0)))
print("STD accuracy for K = 5: "+str(k_five.std()))
print("Mean accuracy for K = 11: "+str(k_eleven.mean(0)))
print("STD accuracy for K = 11: "+str(k_eleven.std()))
print("total mean accuracy: "+str(t_mat.mean(0)))
print("total std accuracy: "+str(t_mat.std()))
