import matplotlib.pyplot as plt
import numpy as np
from math import log2, ceil

# program-wide constants
SYMBMAP = {'A': 1/2,'B': 1/4,'C': 1/8,'D': 1/32,'E': 1/32,'F': 1/16}

# helper function, returns index of first element in sorted array arr greater than the value val
def findIndFirstGreater(arr, val):
    for i, e in enumerate(arr):
        if e > val: return i


# source that generates amt symbols from a set sized len(probabilities), with their respective desired probabilities
def source(symbols, probabilities, amt):
    # reformat probabilities in a way where each element is the sum of all previous elements from the original array
    # this allows for easier indexing later
    probabilities = [sum(probabilities[:i]) for i in range(len(probabilities))]
    probabilities.append(1)
    # generate list of rand numbers
    symbs = np.random.rand(1, amt)[0]
    symStr=''
    # for each randomly generated number, get the corresponding symbol
    for s in symbs:
        symStr += symbols[findIndFirstGreater(probabilities, s) - 1]

    return symStr


# encode incoming message string using 
def arithmeticCoder(message, symbols, probabilities):

    lo, hi = 0, 1
    for symb in message:
        ind = symbols.index(symb)
        loSum = sum(probabilities[:ind])
        print(symb + " loSum:{}".format(loSum))
        newLo = lo + (hi - lo)*loSum
        newHi = lo + (hi - lo)*(loSum + probabilities[ind])
        lo = newLo
        hi = newHi
        print(lo, hi)

    # num bits required to code without data loss
    numBits = ceil(log2(1/(hi-lo))) + 1
    val = (hi+lo)/2
    bitArray=[]
    for i in range(numBits):
        val *= 2
        if(val > 1):
            bitArray.append(1)
            val-=1
        else:
            bitArray.append(0)
    
    return bitArray


# decode bit-stream created by an arithmetic coder 
def arithmeticDecoder(bitArray, symbols, probabilities):
    value = 0
    # reconstruction of value from bit stream
    for i, b in enumerate(bitArray):
        if b == 1: value += 2**(-i-1)

    return value


if __name__ == "__main__":
    symbs = list(SYMBMAP.keys())
    probs = list(SYMBMAP.values())
    message = source(symbs, probs, 10)
    for s in symbs:
        x = [c for c in message if c == s]
        print("P({}): {}".format(s, len(x)/len(message)))


