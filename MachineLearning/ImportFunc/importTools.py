import numpy as numpy
import importHQ as HQ
#imports file and splits into array
def importFile(filename,delimiter):
	results = [];
	#print(filename)
	inputfile = open(filename)
	for line in inputfile:
		results.append(line.strip(delimiter).split())
		#print(str(results[len(results)-1]))
	return results

def buffer():
        signs = HQ.importAll(signs)
        maxFrames = HQ.main(signs)
        return maxFrames

print(buffer())
