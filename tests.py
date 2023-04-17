from main import *

def testSrc():
    print("input:{}".format(SYMBMAP))
    symbs = list(SYMBMAP.keys())
    probs = list(SYMBMAP.values())
    srcStr = source(symbs, probs, 50000)
    print(srcStr)
    for s in symbs:
        x = [c for c in srcStr if c == s]
        print("P({}): {}".format(s, len(x)/len(srcStr)))


def testArithmCDDC():
    bits = arithmeticCoder("HELLO", ['H','E','L','O'], [.2, .2, .4, .2])
    print(arithmeticDecoder(bits, 5, ['H','E','L','O'], [.2, .2, .4, .2]))

def testChannel():
    avgFlipped = 0
    for i in range(10000):
        bits = arithmeticCoder("HELLO", ['H','E','L','O'], [.2, .2, .4, .2])
        bits = ECCCoder(bits)
        (bits, numFlipped) = channel(bits, 0.25)
        bits = ECCDecoder(bits)
        #print(arithmeticDecoder(bits, 5, ['H','E','L','O'], [.2, .2, .4, .2]))
        avgFlipped += numFlipped
    avgFlipped /= 10000
    print("Average flipping probability {}".format(avgFlipped/33))


if __name__ == "__main__":
    testChannel()