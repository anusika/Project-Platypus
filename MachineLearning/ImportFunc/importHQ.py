from os import listdir
from os.path import isfile, join
import numpy as numpy

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
	#print(filename)
	inputfile = open(filename)
	for line in inputfile:
		results.append(line.strip(delimiter).split())
		#print(str(results[len(results)-1]))
	return results



def importAll():
	filesList = []
	importFiles('..\etc\DataSet\signHQ',filesList)
	results = []
	for file in range(0,len(filesList)):
		results.append(importFile(filesList[file],"")) #2D array
	return results

def findMaxFrames(signs):
	maxFrames = 0
	for i in range(0,len(signs)):
		if len(signs[i]) > maxFrames:
			maxFrames = len(signs[i])
	return maxFrames

def main():
        signs = importAll()
        maxFrames = findMaxFrames(signs)
        return maxFrames

