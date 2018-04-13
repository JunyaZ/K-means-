
import random
import math
##________________________Processing the data_________________________________#
def DataProcessing(filename):
    file = open(filename, 'r')              
    infile = file.readlines()  # read the every line of the data
    file.close()# close the file
    Originaldata = [] # declare a new empty list to put all the data into the list
    for line in infile: # for each line in this file
        a = line.strip('\n')       #delete the \n in each line
        b= a.replace(' ',',')  # repalce space with comma
        c= b.split(',')     #split each line by delimter ','
        Originaldata.append(c) #put everthing in the list
    #print(Originaldata)
    floatValue=[]
    for i in range(len(Originaldata)):
        A =Originaldata[i]
        for j in range(len(A)):
            B= A[j]
            for x in B.split(','):
                C= float(x)
                #print(C)
                floatValue.append(C)
    #print(floatValue)
    temp=[]
    InputData=[]
    for i in range(0,int(len(floatValue)),3):
        for j in range(i,i+3):
            temp.append(floatValue[j])
        InputData.append(temp)
        temp= []
    #print(InputData)
    #print(len(InputData))
    return InputData
#__________________________normalizated the data_____________________________#
"""
def normalization(data):
    normlized =[]
    for j in range(len(data[0])):
        col=[]
        for i in range(len(data)):
            col.append(data[i][j])
        norm = [(i-min(col))/(max(col)-min(col) )for i in col]
        normlized.append(norm)
    map(list, zip(*normlized))    
    return list(map(list, zip(*normlized)))
"""
#____________________get the data only not include its label _________________#
def getData(Ogrinaldata):
    data=[]
    for i in range(len(Ogrinaldata)):
        data.append(Ogrinaldata[i][:2])
    return data
#_________________________get the label only___________________________#
def getLabel(Ogrinaldata):    
    label=[]
    for i in range(len(Ogrinaldata)):
        label.append(Ogrinaldata[i][-1])
    return label
#________________________distrance calulation_______________________#
def Distance(data, centroid):
    distance= 0
    for i in range(len(data)):
        distance += math.pow(data[i] - centroid[i],2)
    return math.sqrt(distance)
#_________________________________________________________________#
def countNumInCluster(Input,k):
    #print(Input)
    label = getLabel(Input)
    NewCentroids =[]
    for x in range(k):
        #print("Cluster ", x, "has " ,label.count(x), "samples" )
        list_= []
        for i in range(len(Input)):
            if Input[i][-1]== x:
                list_.append(Input[i][0:k-1])
        #print(list_)
        result=[]
        for i in range(len(list_[0])):
            MeanValue= []
            for j in range(len(list_)):
                MeanValue.append(list_[j][i])
                means= sum(MeanValue)/len(list_)
            #print(means)
            result.append(means)
        result.insert(len(Input),x)
        NewCentroids.append(result)
        #print(NewCentroids)
    return NewCentroids
#_________________________stopping criterion______________________#
def stopCriterion(Centroids, NewCentroids,counter,MaxValue):
    if counter > MaxValue:
        return True
    else:
        for old in Centroids:
            for new in NewCentroids:
                return Distance(old,new) <0.001
#___________________________________________________________________#
def countNum(OutputData,OrginalLabel,k):
    label= getLabel(OutputData)
    #print(label)
    start=0
    end=0
    Overallnum=0
    for x in range(k):
        majority = 0
        mylist=[]
        print("Cluster",x)
        print("Size of Cluster ", x, "is",label.count(x))
        end += OrginalLabel.count(x)
        start += OrginalLabel.count(x-1)
        #print(start,end)       
        misclassified =[]       
        for i in range(start,end):
            mylist.append(label[i])
            majority = max(mylist,key=mylist.count)
            if label[i]!=majority:
                misclassified.append(OutputData[i])
        print("Cluster lable is",majority)
        print("The number of objects misclassified in this cluster is",len(misclassified))
        Overallnum += len(misclassified)
        print(misclassified)
        print("The Overall misclassfied num is ",Overallnum)
        print("========================")
    print("Accuracy rate is ",((len(label)-Overallnum)/len(label))*100,"%")
#__________________________________________________________________________                      
def DistanceClustering(dataset,Centroids):
    Output= []# declare an empty list
    for sample in dataset:
        distance = list()
        for center in Centroids:
            distance.append(Distance(sample,center))
        #print(distance)
        sample.insert(len(sample),distance.index(min(distance)))
        Output.append(sample)
    return Output    
###_____________________the main kmeans algorithm______________________###
def K_means(dataset, k):
    counter = 0
    Dataset =getData(dataset)
    random.seed(0)
    #Dataset = normalization(Data)
    #print(Dataset)
    Centroids = random.sample(Dataset,k)
    #print(Centroids)
    print("Initial k-means are:")
    for i in range(len(Centroids)):
        print("Means[",i,"] is", [Centroids[i][:len(Centroids)-1],i])
    newCentroids = [[0,0,0],[0,0,0],[0,0,0]]           
    while not stopCriterion(Centroids,newCentroids,counter,20):
        OutputData= DistanceClustering(Dataset,Centroids)
        NewCentroids = countNumInCluster(OutputData,k)
        newcentroids= getData(NewCentroids)
        #print(newcentroids)
        Dataset=getData(OutputData)
        Centroids = newcentroids
        counter= counter+1
        #print(counter)
    return OutputData
#____________________________________________####
InputData = DataProcessing('synthetic_2D.txt')
InputLabel = getLabel(InputData)
OrginalLabel= []
for data in InputLabel:
    OrginalLabel.append(int(data))
#print(OrginalLabel)
result = K_means(InputData,3)
num = countNum(result,OrginalLabel,3)
print(num)

