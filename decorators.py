def decorator(funkcja):
    
    def wew(*args):
        print("start decorator")
        result = funkcja(*args)
        print("end decorator")

        return result
    return wew


@decorator
def func(*args):
    # print ("start func")
    
    # print("end func")
    return args

retu = func(1,2,5,6,7)
print(retu)
