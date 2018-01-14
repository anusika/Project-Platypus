
from os import walk

names = []

for (dirpath, dirnames, filenames) in walk('../DataSet/signHQ/tctodd1'):
    if filenames not in names:
        names.append(filenames)
    break

print(names)
