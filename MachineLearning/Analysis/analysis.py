import sys
sys.path.append('..')
#import  MachineLearning.Training.training as trained
import MachineLearning.etc.Tools.names as names

def analyzing(sign):
    answer = []
    possible = names.get_words()
    print(possible)
    for word in possible:
        if word == sign:
            answer.append(sign)
    return answer

print(analyzing("hello"))

