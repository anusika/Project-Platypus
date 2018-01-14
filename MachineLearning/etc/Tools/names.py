
from os import walk

names = []
def get_words():
    for (dirpath, dirnames, filenames) in walk('./etc/DataSet/signHQ/tctodd1'):
        for file in filenames:
            file = file.replace('-', ' ').split(' ')
            file = file[0]
            if file not in names:
                names.append(file)
    return names

#get_words() 
