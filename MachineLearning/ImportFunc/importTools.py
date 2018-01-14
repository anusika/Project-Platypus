import numpy as numpy

def importFile(filename,delimiter):
	results = [];
	print(filename)
	inputfile = open(filename)
	for line in inputfile:
		results.append(line.strip(delimiter).split())
		print(str(results[len(results)-1]))
	return results