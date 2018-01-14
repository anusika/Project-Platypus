
from os import walk

names = []
def get_words():
    for (dirpath, dirnames, filenames) in walk('../DataSet/signHQ/tctodd1'):
        for file in filenames:
            file = file.replace('-', ' ').split(' ')
            file = file[0]
            file = file.replace('_', ' ')
            file = file.strip()
            if file not in names:
                names.append(file)
    return names

get_words() 

