import numpy as numpy

def importFile(filename,delimiter)
	results = [];
	with open(filename) as inputfile:
    for line in inputfile:
        results.append(line.strip().split())
        str(results[len(results)-1])
    return results
