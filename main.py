import matplotlib.pyplot as plt
import random
import numpy as np
from math import log2, ceil

# program-wide constants
SYMBMAP = {'A': 1/2,'B': 1/4,'C': 1/8,'D': 1/32,'E': 1/32,'F': 1/16}
NUM_ITER = 100
NUM_MSG = 100

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


# encode incoming message string using arithmetic coding, returns bit array
def arithmeticCoder(message, symbols, probabilities):
    lo, hi = 0, 1
    for symb in message:
        ind = symbols.index(symb)
        # sum all probabilities up to the current symbol
        loSum = sum(probabilities[:ind])
        # essentially linear interpolation
        newLo = lo + (hi - lo)*loSum
        # the new high bound is the same linear interpolation, but moved by
        # the probability of the current symbol
        newHi = lo + (hi - lo)*(loSum + probabilities[ind])
        lo = newLo
        hi = newHi

    # num bits required to code without data loss
    numBits = ceil(log2(1/(hi-lo))) + 1
    # actual value to be coded
    val = (hi+lo)/2
    bitArray=[]
    # codes floating-point number as a fixed-point number bit-array
    # this approach has limitations, but one of the assumptions is that
    # the result should be fixed-point with numBits of precision
    for _ in range(numBits):
        val *= 2
        if(val > 1):
            bitArray.append(1)
            val-=1
        else:
            bitArray.append(0)
    
    return bitArray


# (3, 1) repetition ECC, repeats each bit 3 times
def ECCCoder(bitArray):
    return [b for b in bitArray for _ in range(3)]


# channel with a given probability of bit error p
def channel(bitArray, p):
    retArr = []
    for e in bitArray:
        rand = random.random()
        # flip a bit with given probability p
        if rand < p: 
            retArr.append(1 - e)
        else:
            retArr.append(e)
    return retArr


# ECC decoding, majority decision
def ECCDecoder(bitArray):
    checkSum = 0
    retArray = []
    for i in range(0, len(bitArray), 3):
        checkSum = bitArray[i]+bitArray[i+1]+bitArray[i+2]
        # if there are 2 or more 1's, it's *probably* a 1 
        if(checkSum >= 2): retArray.append(1)
        else: retArray.append(0)
    
    return retArray


# decode bit-stream created by an arithmetic coder 
def arithmeticDecoder(bitArray, msgLen, symbols, probabilities):
    value = 0
    # reconstruction of value from bit stream
    for i, b in enumerate(bitArray):
        if b == 1: value += 2**(-i-1)

    reconstructedMsg = ""

    # same idea as encoding, find nearest values lower and higher
    # than the received value, and then narrow the search, thus
    # getting the next symbol and so on...
    lo, hi = 0, 1
    for i in range(msgLen):
        hiSum, loSum = 0, 0
        for j, p in enumerate(probabilities):
            hiSum += (hi - lo) * p
            if hiSum + lo >= value:
                loSum = hiSum - (hi - lo) * p
                hi = lo + hiSum; lo = lo + loSum
                reconstructedMsg += symbols[j]
                break
    
    return reconstructedMsg


# helper, returns probabilities of each symbol from symbols appearing in message msg
def getRealMessageProbs(msg, symbols):
    probs = []
    for s in symbols:
        x = [c for c in msg if c == s]
        # append actual probabilities from message
        probs.append(len(x)/len(message))
    return probs


# helper, compares 2 arrays element-wise, returns number of different elements
def compareBitArrays(arr1, arr2):
    numDiff = 0
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]: 
            numDiff+=1

    return numDiff

if __name__ == "__main__":
    symbs = list(SYMBMAP.keys())
    probs = list(SYMBMAP.values())
    
    x = np.linspace(0, 1, 1001)
    Pe = []
    # for each probability...
    for p in x:
        numDiff = 0
        # ...for NUM_MSG messages, do NUM_ITER tests, and get the average bit error rate
        for _ in range(NUM_MSG):
            # generate message
            message = source(symbs, probs, 10)
            probs = getRealMessageProbs(message, symbs)
            inputBits = arithmeticCoder(message, symbs, probs)
            eccBits = ECCCoder(inputBits)

            for _ in range(NUM_ITER):
                outputBits = channel(eccBits, p)
                outputBits = ECCDecoder(outputBits)
                numDiff += compareBitArrays(inputBits, outputBits)

        # average number of different bits
        numDiff /= (NUM_ITER * NUM_MSG)
        # bit error rate for given p
        numDiff /= len(inputBits)
        Pe.append(numDiff)

    # plotting
    fig, ax = plt.subplots()
    # experimental values
    ax.plot(x, Pe, color='red')
    # expected values
    y = x**3 + 3*(1-x)*(x**2)
    ax.plot(x, y, color='blue')

    plt.show()
    

