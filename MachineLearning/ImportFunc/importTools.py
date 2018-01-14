from importHQ import * 

def buffer():
        maxFrames = main()
        results = importAll()
        for result in results:
                if len(result) < maxFrames:
                        difference = maxFrames-len(result)
                        if difference%2 == 0:
                                difference_start = difference_end = int(difference/2)     
                        else:
                                difference_start = int(difference/2)
                                difference_end = difference_start+1
                        for x in range(difference_start):
                                result.insert(0, result[0])
                        for x in range(difference_end):
                                result.append(result[-1])
                        if len(result) != maxFrames:
                                print("what happened")
                else:
                        pass
        print("done")
        return results        


buffer()
