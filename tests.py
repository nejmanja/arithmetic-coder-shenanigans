from main import source, arithmeticCoder, arithmeticDecoder, SYMBMAP

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
    print(arithmeticDecoder(bits, ['H','E','L','O'], [.2, .2, .4, .2]))


if __name__ == "__main__":
    testArithmCDDC()