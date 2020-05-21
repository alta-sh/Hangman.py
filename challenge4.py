from functools import reduce
def sum_dig_prod(*args):
    newNum = sum(args) if len(args) > 1 else args[0]
    if(newNum > 9):    
        return sum_dig_prod(reduce((lambda x, y: x * y), map(int, list(str(sum_dig_prod(newNum))))))
    else:
        return newNum

print(sum_dig_prod(16, 28, 42, 13))