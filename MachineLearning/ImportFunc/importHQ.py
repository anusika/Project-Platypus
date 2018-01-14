from os import listdir
from os.path import isfile, join
import numpy as numpy


import sys
sys.path.append('..')
import MachineLearning.etc.Tools.names as names

#recursive function for getting all data filepaths
def importFiles(path,filesList): 
	for subpath in listdir(path):
		absPath = join(path,subpath)
		if isfile(absPath):
			filesList.append(absPath)
		else: 
			importFiles(absPath,filesList)

			
#imports file and splits into array
def importFile(filename,delimiter):
	results = [];
	print(filename)
	inputfile = open(filename)
	for line in inputfile:
		results.append(numpy.array(line.strip(delimiter).split()))
	return results

def buffer(result):
	if len(result) < 136:
		difference = 136-len(result)
		difference_start = int(difference/2)
		difference_end = difference -  difference_start
		for x in range(difference_start):
			result.insert(0, result[0])
		for x in range(difference_end):
			result.append(result[-1])
	return result      

def importAll():
	filesList = []
	importFiles('.\etc\DataSet\signHQ',filesList)
	results = []
	outputValues = []
	for file in range(0,len(filesList)):
		inputMatrix = buffer(importFile(filesList[file],""))
		output = outputs(filesList[file])
		results.append(numpy.hstack(numpy.array(inputMatrix))) #2D array
		outputValues.append(numpy.array(output))
	numpy.savez(".\etc\DataSet\pickledData\savedData.npz",features=results,labels=outputValues)
	return results

def getOutput():
	signNames = names.get_words()
	def placeOutput(filename):
		outputValues = []
		for name in range(0,len(signNames)):
			if signNames[name] in filename:
				outputValues.append(1)
			else:
				outputValues.append(0)
		return numpy.array(outputValues)
	return placeOutput

outputs = getOutput()

def findMaxFrames(signs):
	maxFrames = 0
	for i in range(0,len(signs)):
		if len(signs[i]) > maxFrames:
			maxFrames = len(signs[i])
	return maxFrames

def main():
        signs = importAll()

main()