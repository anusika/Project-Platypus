from os import listdir
from os.path import isfile, join
import importTools as iT
#recursive function for getting all data filepaths
def importFiles(path,filesList): 
	for subpath in listdir(path):
		absPath = join(path,subpath)
		if isfile(absPath):
			filesList.append(absPath)
		else: 
			importFiles(absPath,filesList)

filesList = []
importFiles('..\etc\DataSet\signHQ',filesList)
for file in range(0,len(filesList)):
	iT.importFile(filesList[file],"")
