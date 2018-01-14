from os import listdir
from os.path import isfile, join

#recursive function for getting all data filepaths
def importFiles(path,filesList) 
	for subpath in listdir(path):
		absPath = join(path,subpath)
		if isfile(absPath):
			filesList.append(absPath)
		else: 
			importFiles(absPath,filesList)

filesList = []
importFiles('../etc/signHQ')
for file in range(0,len(filesList)):
	return 0
