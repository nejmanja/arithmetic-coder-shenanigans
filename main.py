import matplotlib.pyplot as plt
import random
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
        newLo = lo + (hi - lo)*loSum
        newHi = lo + (hi - lo)*(loSum + probabilities[ind])
        lo = newLo
        hi = newHi

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


# (3, 1) repetition ECC, repeats each bit 3 times
def ECCCoder(bitArray):
    return [b for b in bitArray for _ in range(3)]


# channel with a given probability of bit error p
def channel(bitArray, p):
    bitsFlipped = 0
    for i, e in enumerate(bitArray):
        rand = random.random()
        # flip a bit with given probability p
        if rand < p: 
            bitArray[i] = 1 - e
            # print("Flipped bit {}!".format(i))
            bitsFlipped+=1
    return (bitArray, bitsFlipped)


# ECC decoding, majority decision
def ECCDecoder(bitArray):
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


if __name__ == "__main__":
    symbs = list(SYMBMAP.keys())
    probs = list(SYMBMAP.values())
    message = source(symbs, probs, 10)
    for s in symbs:
        x = [c for c in message if c == s]
        print("P({}): {}".format(s, len(x)/len(message)))


