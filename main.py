import matplotlib.pyplot as plt
import numpy as np

# program-wide constants
SYMBMAP = {'A': 1/2,'B': 1/4,'C': 1/8,'D': 1/32,'E': 1/32,'F': 1/16}

# helper function, returns index of first element in sorted array arr greater than the value val
def findIndFirstGreater(arr, val):
    for i, e in enumerate(arr):
        if e > val: return i


# source that generates amt symbols from a set sized len(probabilities), with their respective probabilities
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

    return (lo, hi)


if __name__ == "__main__":
    symbs = list(SYMBMAP.keys())
    probs = list(SYMBMAP.values())
    message = source(symbs, probs, 10)
    for s in symbs:
        x = [c for c in message if c == s]
        print("P({}): {}".format(s, len(x)/len(message)))

    print(arithmeticCoder(message, symbs, probs))

