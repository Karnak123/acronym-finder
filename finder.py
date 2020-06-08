import re
import sys


def buildLCSmatrix(X, Y):
    m, n = len(X), len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[0] * (n + 1) for i in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 'D'
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 'U'
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 'L'
    return c, b


def buildVector(stack, n):
    list = [0] * n
    for i, j in stack:
        list[j - 1] = i
    return list


def parseLCSmatrix(b, size_i, size_j, m, n, lcs_size, stack, vectorlist):
    for i in range(size_i, m + 1):
        for j in range(size_j, n + 1):
            if b[i][j] == 'D':
                stack.append((i, j))
                if lcs_size == 1:
                    v = buildVector(stack, n)
                    vectorlist.append(v)
                else:
                    parseLCSmatrix(b, i + 1, j + 1, m, n, lcs_size - 1, stack, vectorlist)
                stack.pop()
    return vectorlist


def getFirstAndLastIndex(VectorList):
    try:
        first = next((i for i, x in enumerate(VectorList) if x), None)
    except TypeError:
        first = None
    try:
        reverseV = VectorList[::-1]
    except:
        last = None
        return first, last
    try:
        last = (len(VectorList) - 1) - next((i for i, x in enumerate(reverseV) if x), None)
    except TypeError:
        last = None

    return first, last


def vectorValues(V, types):
    dict = {'size': 0, 'distance': 0, 'stopcount': 0, 'misses': 0}
    try:
        first, last = getFirstAndLastIndex(V)
    except:
        return dict
    dict['size'] = last - first + 1
    dict['distance'] = (len(V) - 1) - last
    dict['stopcount'] = 0
    dict['misses'] = 0
    for i in range(first, last + 1):
        if V[i] > 0 and types[i] == 's':
            dict['stopcount'] = dict['stopcount'] + 1
        elif V[i] == 0 and types[i] != 's' and types[i] != 'h':
            dict['misses'] = dict['misses'] + 1
    return dict


def compareVectors(A, B, types):
    if B == None:
        return A
    if A == None:
        return B

    resultA = vectorValues(A, types)
    resultB = vectorValues(B, types)
    if resultA['misses'] > resultB['misses']:
        return B
    elif resultA['misses'] < resultB['misses']:
        return A
    if resultA['stopcount'] > resultB['stopcount']:
        return B
    elif resultA['stopcount'] < resultB['stopcount']:
        return A
    if resultA['distance'] > resultB['distance']:
        return B
    elif resultA['distance'] < resultB['distance']:
        return A
    if resultA['size'] > resultB['size']:
        return B
    elif resultA['size'] < resultB['size']:
        return A


def findAcronym(words, acronym, stopwords):
    index = [i for i, s in enumerate(words) if acronym in s]
    indexAcronym = index[0]
    # indexAcronym = words.index(acronym)

    preWindowFirstIndex = indexAcronym - 16
    postWindowLastIndex = indexAcronym + 16
    if preWindowFirstIndex < 0:
        preWindow = words[:indexAcronym]
    else:
        preWindow = words[preWindowFirstIndex:indexAcronym]
    if postWindowLastIndex > len(words):
        postWindow = words[indexAcronym + 1:]
    else:
        postWindow = words[indexAcronym + 1:postWindowLastIndex + 1]

    preWindowJoin = ' '.join(preWindow)
    preWindowS = re.findall(r'\w+', preWindowJoin)
    prehyphenatedWords = re.findall(r'\w+-\w+[-\w+]*', preWindowJoin)
    postWindowJoin = ' '.join(postWindow)
    postWindowS = re.findall(r'\w+', postWindowJoin)
    posthyphenatedWords = re.findall(r'\w+-\w+[-\w+]*', postWindowJoin)

    preleaders = [x[0].lower() for x in preWindowS]
    postleaders = [x[0].lower() for x in postWindowS]

    pretypes = []
    for x in preWindowS:
        if x.lower() in stopwords:
            pretypes.append('s')
        else:
            flagHyphen = 0
            for word in prehyphenatedWords:
                listHyphen = ''.join(word).split('-')
                if x in listHyphen:
                    flagHyphen = 1
                    indexHyphen = listHyphen.index(x)
                    if (indexHyphen == 0):
                        pretypes.append('H')
                    else:
                        pretypes.append('h')
            if not flagHyphen:
                pretypes.append('w')

    posttypes = []
    for x in postWindowS:
        if x.lower() in stopwords:
            posttypes.append('s')
        else:
            flagHyphen = 0
            for word in posthyphenatedWords:
                listHyphen = ''.join(word).split('-')
                if x in listHyphen:
                    flagHyphen = 1
                    indexHyphen = listHyphen.index(x)
                    if indexHyphen == 0:
                        posttypes.append('H')
                    else:
                        posttypes.append('h')
            if not flagHyphen:
                posttypes.append('w')

    A, B, C = acronym.lower(), ''.join(preleaders), ''.join(postleaders)

    c1, b1 = buildLCSmatrix(A, B)
    c2, b2 = buildLCSmatrix(A, C)

    m, n, o = len(A), len(B), len(C)
    preVectors = postVectors = []

    try:
        preVectors = parseLCSmatrix(b1, 0, 0, m, n, c1[m][n], [], [])
    except:
        pass
    try:
        postVectors = parseLCSmatrix(b2, 0, 0, m, o, c2[m][n], [], [])
    except:
        pass

    if not preVectors and not postVectors:
        return 'Acronym definition not in text'
    elif not preVectors:
        prechoiceVector, postchoiceVector = [], postVectors[0]
    elif not postVectors:
        prechoiceVector, postchoiceVector = preVectors[0], []
    else:
        prechoiceVector, postchoiceVector = preVectors[0], postVectors[0]
    for i in range(1, len(preVectors)):
        prechoiceVector = compareVectors(prechoiceVector, preVectors[i], pretypes)
    for i in range(1, len(postVectors)):
        postchoiceVector = compareVectors(postchoiceVector, postVectors[i], posttypes)

    finalList = []
    prefirstIndex, prelastIndex = getFirstAndLastIndex(prechoiceVector)
    postfirstIndex, postlastIndex = getFirstAndLastIndex(postchoiceVector)

    countHyphen = 0
    textHyphen = ""
    if prechoiceVector != [] and prechoiceVector is not None:
        for i, x in enumerate(prechoiceVector):
            if prefirstIndex <= i <= prelastIndex:
                if pretypes[i] == 'H' or pretypes[i] == 'h':
                    textHyphen += preWindowS[i]
                    if i + 1 < len(pretypes) and pretypes[i + 1] == 'h':
                        countHyphen += 1
                        textHyphen += '-'
                        continue
                if countHyphen != 0:
                    textJoin = textHyphen
                    textHyphen = ""
                    countHyphen = 0
                else:
                    textJoin = preWindowS[i]
                finalList.append(textJoin)
    elif postchoiceVector != [] and postchoiceVector is not None:
        for i, x in enumerate(postchoiceVector):
            if postfirstIndex <= i <= postlastIndex:
                if posttypes[i] == 'H' or posttypes[i] == 'h':
                    textHyphen += postWindowS[i]
                    if i + 1 < len(posttypes) and posttypes[i + 1] == 'h':
                        countHyphen += 1
                        textHyphen += '-'
                        continue
                if countHyphen != 0:
                    textJoin = textHyphen
                    textHyphen = ""
                    countHyphen = 0
                else:
                    textJoin = postWindowS[i]
                finalList.append(textJoin)

    return ' '.join(finalList)


def main():
    filename = str(sys.argv)[1]
    file = open(filename, 'r')
    text = file.read()
    print(text)

    words = text.replace('(', '').replace(')', '').split()

    fileStopwords = open('stopwords.txt', 'r')
    stopwordsList = fileStopwords.read()
    stopwords = stopwordsList.split()

    acronymList = [x for x in words if x.isupper() and len(x) > 1]
    acronymLists = re.findall(r'\w+', ' '.join(acronymList))

    print("Acronyms and its definitions")
    for acronym in acronymLists:
        definition = findAcronym(words, acronym, stopwords)
        if definition == '':
            definition = 'Acronym definition not in text'
        print(acronym, ":", definition)


main()
