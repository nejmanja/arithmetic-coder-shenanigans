from main import source, SYMBMAP

def testSrc():
    print("input:{}".format(SYMBMAP))
    symbs = list(SYMBMAP.keys())
    probs = list(SYMBMAP.values())
    srcStr = source(symbs, probs, 50000)
    print(srcStr)
    for s in symbs:
        x = [c for c in srcStr if c == s]
        print("P({}): {}".format(s, len(x)/len(srcStr)))


if __name__ == "__main__":
    testSrc()