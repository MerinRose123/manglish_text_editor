# -*- coding: utf-8 -*-

import sqlite3
import itertools
import time

schemefile = sqlite3.connect("ml.scheme")
cursor = schemefile.cursor()

# CACHE FOR WORDS
cacheRegistry = []
cacheData = {}

# CACHE FOR TOKENS
savedTokens = {}

# CONSTANTS
maxCacheSize = 100
maxTokenSize = 8

_ER_ = 'ERROR'
_WRN_ = 'WARNING'
_LOG_ = 'LOG'


def addLog(logType, msg):
    logFile = open('log.txt', 'a', encoding='utf-8')
    logFile.write(logType + ' : ' + msg + ' @ ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n')
    logFile.close()


def cache(pattern, data):
    global cacheRegistry
    global cacheData

    if pattern in cacheRegistry:
        cacheRegistry.remove(pattern)
        cacheRegistry.append(pattern)
        return True

    if len(cacheRegistry) >= maxCacheSize:
        keyToRemove = cacheRegistry[0]
        cacheRegistry = cacheRegistry[1:]
        del cacheData[keyToRemove]

    cacheRegistry.append(pattern)
    cacheData[pattern] = data
    return True


def getFromCache(pattern):
    if pattern in cacheRegistry:
        return cacheData[pattern]
    return False


def setupScheme():
    cursor.execute('''
    create table if not exists symbols(
      id integer not null primary key autoincrement,
      pattern varchar(32),
      value1  varchar(32),
      value2  varchar(32),
      value3 varchar(32),
      type integer,
      matchType integer,
      frequency integer default 0
    )
  ''')

    cursor.execute('''
    create table if not exists words(
      id integer not null primary key autoincrement,
      pattern varchar(120),
      wordID integer
      frequency integer default 0
    )
  ''')
    cursor.execute('''
    create table if not exists wordList(
      wordId integer not null primary key autoincrement,
      word varchar(120),
      frequency integer default 0
    )
  ''')

    # INDEXES TO SPEED UP QUERY
    cursor.execute('create index pattern_SYMBOLS on symbols (pattern asc)')
    cursor.execute('create index pattern_WORDS on words (pattern asc)')
    cursor.execute('create index wordId_WORDLIST on wordList(wordId asc)')
    cursor.execute('create index value1_SYMBOLS on symbols (value1 asc)')

    schemefile.commit()
    return True


def extractKeysAndValues(keys, values, Tokentype, matchType=1):
    if str(type(keys)) == "<class 'tuple'>":
        for key in keys:
            if str(type(key)) == "<class 'tuple'>":
                extractKeysAndValues(key, values, Tokentype, 2)
            else:
                saveKeyValue(key, values, Tokentype, matchType)
    else:
        saveKeyValue(keys, values, Tokentype, matchType)


def saveKeyValue(key, values, Tokentype, matchType):
    # print(key,values)
    if str(type(values)) == "<class 'list'>":
        if len(values) > 2:
            value1 = values[0]
            value2 = values[1]
            value3 = values[2]
        elif len(values) > 1:
            value1 = values[0]
            value2 = values[1]
            value3 = ''
    else:
        value1 = values
        value2 = ''
        value3 = ''

    sql = '''insert into symbols 
      (pattern,value1,value2,value3,type,matchType) 
      values('%s','%s','%s','%s',%d,%d)''' % (key, value1, value2, value3, Tokentype, matchType)
    return cursor.execute(sql)  # ,[])


def vowel(hash):
    for hashKey in hash:
        extractKeysAndValues(hashKey, hash[hashKey], 1, 1)
        schemefile.commit()


def consonants(hash):
    for hashKey in hash:
        extractKeysAndValues(hashKey, hash[hashKey], 2, 1)
        schemefile.commit()


def generateCV():
    tokensv = []
    tokensc = []
    sqlv = "select pattern,value2 from symbols where type = 1"
    sqlc = "select pattern,value1,value2 from symbols where type=2"
    res = cursor.execute(sqlv)
    for i in res:
        tokensv.append(i)
    res = cursor.execute(sqlc)
    for i in res:
        tokensc.append(i)
    for consonant in tokensc:
        consonant_has_inherent_a_sound = (
                    consonant[0][len(consonant[0]) - 1] == 'a' and consonant[0][len(consonant[0]) - 2] != 'a')
        if consonant_has_inherent_a_sound:
            pattern = consonant[0][:len(consonant[0]) - 1]
            value = consonant[1] + '???'
            saveKeyValue(pattern, value, 3, 1)
        for v in tokensv:
            if v[1] != '':
                if consonant_has_inherent_a_sound:
                    pattern = consonant[0][:len(consonant[0]) - 1] + v[0]
                else:
                    pattern = consonant[0] + v[0]
                values = consonant[1] + v[1]
                saveKeyValue(pattern, values, 3, 1)


def createSchemeFile():
    setupScheme()

    vowel({"~": "???"})
    vowel({"a": "???"})
    vowel({"a": ["???", "??????"]})
    vowel({"ah": ["???", "??????"]})
    vowel({(("a"), "aa", "A"): ["???", "???"]})
    vowel({"i": ["???", "???"]})
    vowel({("ee", "I", "ii", ("i")): ["???", "???"]})
    vowel({"u": ["???", "???"]})
    vowel({(("u"), "uu", "oo", "U"): ["???", "???"]})
    vowel({(("ri", "ru"), "R"): ["???", "???", "???"]})
    vowel({"e": ["???", "???"]})
    vowel({("E", ("e")): ["???", "???"]})
    vowel({("ai", "ei"): ["???", "???"]})
    vowel({"o": ["???", "???"]})
    vowel({("O", ("o")): ["???", "???"]})
    vowel({("ou", "au", "ow"): ["???", "???"]})
    vowel({("OU", "AU", "OW"): ["???", "???"]})

    consonants({("ka"): "???"})
    consonants({("kha", ("gha")): "???"})
    consonants({"ga": "???"})
    consonants({("gha", ("kha")): "???"})
    consonants({("NGa", ("nga")): "?????????"})
    consonants({"cha": "???"})
    consonants({("CHa", ("cha", "jha")): "???"})
    consonants({(("cha")): "?????????"})
    consonants({"ja": "???"})
    consonants({("jha", "JHa"): "???"})
    consonants({(("nja"), "NJa"): "?????????"})
    consonants({("ta", ("tta")): "?????????"})
    consonants({(("da", "ta"), "Ta"): "???"})
    consonants({(("da", "ta"), "TTa"): "???"})
    consonants({("Da", ("da")): "???"})
    consonants({(("da"), "DDa"): "???"})
    consonants({("tha", ("ta")): "???"})
    consonants({(("tha", "dha"), "thha"): "???"})
    consonants({(("tha", "dha"), "tathha"): "?????????"})
    consonants({"da": "???"})
    consonants({(("dha"), "ddha"): "?????????"})
    consonants({"dha": "???"})
    consonants({"pa": "???"})
    consonants({("pha", "fa", "Fa"): "???"})
    consonants({"ba": "???"})
    consonants({"bha": "???"})
    consonants({("va", "wa"): "???"})
    consonants({("Sa", ("sha", "sa")): "???"})
    consonants({("sa", "za"): "???"})
    consonants({"ha": "???"})

    consonants({"nja": ["???", "?????????"]})
    consonants({"nga": ["???", "?????????"]})

    consonants({("kra"): "?????????"})
    consonants({"gra": "?????????"})
    consonants({("ghra", ("khra")): "?????????"})
    consonants({("CHra", ("chra", "jhra")): "?????????"})
    consonants({"jra": "?????????"})
    consonants({(("dra", "tra"), "Tra"): "?????????"})
    consonants({("Dra", ("dra")): "?????????"})
    consonants({"Dhra": "?????????"})
    consonants({("thra", ("tra")): "?????????"})
    consonants({"dra": "?????????"})
    consonants({("ddhra", ("dhra")): "???????????????"})
    consonants({"dhra": "?????????"})
    consonants({"pra": "?????????"})
    consonants({("phra", "fra", "Fra"): "?????????"})
    consonants({"bra": "?????????"})
    consonants({"bhra": "?????????"})
    consonants({("vra", "wra"): "?????????"})
    consonants({("Sra", ("shra", "sra")): "?????????"})
    consonants({"shra": "?????????"})
    consonants({("sra", "zra"): "?????????"})
    consonants({"hra": "?????????"})
    consonants({"nthra": "???????????????"})
    consonants({(("ndra", "ntra"), "nDra", "Ntra", "nTra"): "???????????????"})
    consonants({"ndra": "???????????????"})
    consonants({(("thra"), "THra", "tthra"): "???????????????"})
    consonants({"nnra": "???????????????"})
    consonants({("kkra", "Kra", "Cra"): "???????????????"})
    consonants({("mpra", "mbra"): "???????????????"})
    consonants({("skra", "schra"): "???????????????"})
    consonants({"ndhra": "???????????????"})
    consonants({"nmra": "???????????????"})
    consonants({("NDra", ("ndra")): "???????????????"})

    consonants({("cra"): "?????????"})

    consonants({"ya": "???"})
    consonants({"sha": "???"})
    consonants({"zha": "???"})
    consonants({("xa", ("Xa")): "?????????"})
    consonants({"ksha": "?????????"})
    consonants({"nka": "?????????"})
    consonants({("ncha", ("nja")): "?????????"})
    consonants({"ntha": "?????????"})
    consonants({"nta": "?????????"})
    consonants({(("nda"), "nDa", "Nta"): "?????????"})
    consonants({"nda": "?????????"})
    consonants({"tta": "?????????"})
    consonants({(("tha"), "THa", "ttha"): "?????????"})
    consonants({"lla": "?????????"})
    consonants({("LLa", ("lla")): "?????????"})
    consonants({"nna": "?????????"})
    consonants({("NNa", ("nna")): "?????????"})
    consonants({("bba", "Ba"): "?????????"})
    consonants({("kka", "Ka"): "?????????"})
    consonants({("gga", "Ga"): "?????????"})
    consonants({("jja", "Ja"): "?????????"})
    consonants({("mma", "Ma"): "?????????"})
    consonants({("ppa", "Pa"): "?????????"})
    consonants({("vva", "Va", "wwa", "Wa"): "?????????"})
    consonants({("yya", "Ya"): "?????????"})
    consonants({("mpa", "mba"): "?????????"})
    consonants({("ska", "scha"): "?????????"})
    consonants({(("cha"), "chcha", "ccha", "Cha"): "?????????"})
    consonants({"ndha": "?????????"})
    consonants({"jnja": "?????????"})
    consonants({"nma": "?????????"})
    consonants({("Nma", ("nma")): "?????????"})
    consonants({("nJa", ("nja")): "?????????"})
    consonants({("NDa", ("nda")): "?????????"})

    consonants({("ra"): "???"})
    consonants({(("ra"), "Ra"): "???"})
    consonants({("na"): "???"})
    consonants({(("na"), "Na"): "???"})
    consonants({("la"): "???"})
    consonants({(("la"), "La"): "???"})
    consonants({("ma"): "???"})

    consonants({("rva", "rwa"): "?????????"})
    consonants({"rya": "?????????"})
    consonants({("Rva", "Rwa", ("rva")): "????????????"})
    consonants({("Rya", ("rya")): "????????????"})
    consonants({("nva", "nwa"): "?????????"})
    consonants({"nya": "?????????"})
    consonants({("Nva", "Nwa", ("nva", "nwa")): "?????????"})
    consonants({("Nya", ("nya")): "?????????"})
    consonants({("lva", "lwa"): "?????????"})
    consonants({"lya": "?????????"})
    consonants({("Lva", "Lwa", ("lva", "lwa")): "?????????"})
    consonants({("Lya", ("lya")): "?????????"})
    consonants({("mva", "mwa"): "?????????"})
    consonants({"mya": "?????????"})
    consonants({'c': "??????"})

    generateCV()

    consonants({
        (("ru")): "??????",
        (("r~", "ru")): "??????",
        (("nu")): "??????",
        (("n~", "nu")): "??????",
        (("lu")): "??????",
        (("l~", "lu")): "??????",
        (("mu")): "??????",
        ("r~"): "??????",
        ("R~"): "??????",
        ("n~"): "??????",
        ("N~"): "??????",
        ("l~"): "??????",
        ("L~"): "??????",
        ("m~"): "??????",
        "m": ["???", "???", "???"],
        "n": ["???", "?????????", "???"],
        ("N", ("n")): ["???", "?????????", "???"],
        "l": ["???", "?????????", "???"],
        ("L", ("l")): ["???", "?????????", "???"],
        ("r"): ["???", "?????????", "???"]
    })


def tokenizeWord(word):
    tokenList = []
    while len(word) > 0:

        strbuff = word[:min(len(word), maxTokenSize)]

        while len(strbuff) > 0:
            if strbuff in savedTokens:
                res = savedTokens[strbuff]
                break
            else:
                sql = "select pattern,value1,value2,value3,id,frequency from symbols where pattern = '%s' order by frequency desc" % (
                    strbuff)
                cursor.execute(sql)
                res = cursor.fetchall()
                if len(res) == 0:
                    strbuff = strbuff[:len(strbuff) - 1]
                else:
                    savedTokens[strbuff] = res
                    break
        else:
            tokenList.append(word[0])
            word = word[1:]
            strbuff = ''

        word = word[len(strbuff):]
        tokenList.append(res)

    return tokenList


def reTokenizeWord(mlword):
    tokenList = []

    while len(mlword) > 0:
        strbuff = mlword[:min(7, len(mlword))]  # 6 digits max
        while len(strbuff) > 0:
            # sql = "select pattern from symbols where value1 = '%s' or value2 = '%s' or value3 = '%s'"%(strbuff,strbuff,strbuff)
            if strbuff in savedTokens:
                res = savedTokens[strbuff]
                break
            else:
                sql = "select lower(pattern) as pattern from symbols where value1 = '%s' or value2 = '%s' or value3 = '%s' group by lower(pattern) order by frequency" % (
                strbuff, strbuff, strbuff)
                cursor.execute(sql)
                res = cursor.fetchall()
                if len(res) == 0:
                    strbuff = strbuff[:len(strbuff) - 1]
                    if len(strbuff) == 0:
                        return -1
                else:
                    savedTokens[strbuff] = res
                    break
        mlword = mlword[len(strbuff):]
        tokenList.append(res)

    return tokenList


def getMaxTokenCount(tokenMatrix):
    count = 1
    for i in tokenMatrix:
        count *= len(i)
    return count


def getLargestMatrixIndex(matrix):
    index = 0
    for i in range(1, len(matrix)):
        if len(matrix[i]) > len(matrix[index]):
            index = i
    return index


def isLearnedWord(word):
    sql = "select * from wordList where word ='%s'" % (word)
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res) == 0:
        return False
    return True


def sanitizeWordForLearning(word):
    word = word.replace('\u200d', '')
    word = word.replace('\u200c', '')
    word = word.strip()

    return word


def flattenToken(matrix):
    if len(matrix) < 2:
        return matrix

    wordsCount = getMaxTokenCount(matrix)

    if wordsCount > 50:
        addLog(_WRN_, '%d possiilites with matrix' % (wordsCount) + ' ' + str(matrix))
        print("{} possibilities for ".format(str(wordsCount)))

    matrixA = list(itertools.product(*matrix))
    return matrixA


def reverseTranslate(word):
    tokenList = reTokenizeWord(word)
    if tokenList == -1:
        return -1
    wordsList = flattenToken(tokenList)
    possilePatterns = []
    for i in wordsList:
        q = ''
        for j in i:
            q = q + j[0]
        possilePatterns.append(q)
    return possilePatterns


def learnPatternsFor(word):
    patternList = reverseTranslate(word)
    failedFileList = open('failed.txt', 'a', encoding='utf-8')
    if (patternList == -1):
        print("failed to learn word %s" % (word))
        failedFileList.write(word + '\n')
        return -1
    # print(word,'=>',patternList)
    print('learning %s' % (word))

    cursor.execute("insert into wordList (word) values('%s')" % (word))
    schemefile.commit()

    cursor.execute("select wordId from wordList where word = '%s'" % (word))
    d = cursor.fetchall()
    wordId = d[0][0]
    for i in patternList:
        cursor.execute("insert into words (pattern,wordId) values('%s','%d')" % (i, wordId))
    schemefile.commit()


def learnFromFiles(fileList):
    for i in fileList:
        learningFile = open("dataset/" + str(i) + '.txt', encoding='utf-8')

        addLog(_LOG_, 'learning from file %d.txt Started ' % (i))

        for word in learningFile:
            word = word.split(' ')[0]
            word = sanitizeWordForLearning(word)
            if isLearnedWord(word):
                print("already learned word %s" % (word))
            else:
                learnPatternsFor(word)
        addLog(_LOG_, 'learning from file %d.txt Finished ' % (i))
        learningFile.close()


def breakPattern(word):
    wordList = []
    while len(word) > 0:
        strbuff = word
        while len(strbuff) > 0:
            cacheEntry = getFromCache(strbuff)
            if cacheEntry != False:
                wordList.append(cacheEntry)
                break
            else:
                cursor.execute(
                    "select pattern,wordID from words where pattern='%s' order by frequency desc" % (strbuff))
                re = cursor.fetchall()
                if len(re) == 0:
                    strbuff = strbuff[:len(strbuff) - 1]
                else:
                    w = []
                    for ll in re:
                        w.append(fetchWord(ll[1])[0][0])
                    cache(strbuff, tuple(w))
                    wordList.append(tuple(w))
                    break
        else:
            break
        word = word[len(strbuff):]
    if len(word) == 0:
        return wordList

    else:
        # wordList should have the closest matches
        # word has remaing part to tokenize
        remList = tokenizeWord(word)  # APPLY REDUCE NOISE FUNCTION HERE
        return wordList + remList

    return wordList


def generate_word_list(word):
    re = []
    sql = "select * from words where pattern = '%s' order by frequency desc" % (word)
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res) == 0:
        wordList = flatten(breakPattern(word))
        return (wordList)
    else:
        for i in res:
            cursor.execute("select word from wordList where wordID = %d" % (i[2]))
            re += cursor.fetchall()
        return list(re)


def fetchWord(wordID):
    cursor.execute("select word from wordList where wordid=%d" % (wordID))
    return cursor.fetchall()


def flatten(tokenList):
    stack = []
    virama = '???'

    for tok in tokenList:
        if str(type(tok)) == "<class 'tuple'>":
            if len(stack) == 0:
                stack = list(tok)
            else:
                ns = []

                # delete virama
                for el in range(0, len(stack)):
                    li = len(stack[el]) - 1
                    if stack[el][li] == virama:
                        stack.append(stack[el][:li])  # stack[el] = stack[el][:li]

                for elmt in tok:
                    for elms in stack:
                        ns.append(elms + elmt)
                stack = ns
        else:
            if len(stack) == 0:
                for elm in tok:
                    stack.append(elm[1])
                    if elm[2] != '':
                        stack.append(elm[2])
                    if elm[3] != '':
                        stack.append(elm[3])
            else:
                ns = []

                # delete virama end of elms from stack
                for el in range(0, len(stack)):
                    li = len(stack[el]) - 1
                    if stack[el][li] == virama:
                        stack[el] = stack[el][:li]

                for elmt in tok:
                    for elms in stack:
                        ns.append(elms + elmt[1])
                        if elmt[2] != '':
                            ns.append(elms + elmt[2])
                        if elmt[3] != '':
                            ns.append(elms + elmt[3])
                stack = ns
    return list(stack)


def reduceNoise(matrix):
    for m in matrix:
        for i in range(0, len(m)):
            if '~' in m[i][0] and len(m[i]) > 0:
                m.remove(m[i])

    while getMaxTokenCount(matrix) > 100:
        index = getLargestMatrixIndex(matrix)
        if len(matrix[index]) > 1:
            matrix[index] = matrix[index][:len(matrix[index]) - 1]

    return matrix


def updateTokenFrequency(pattern, word):
    tokenList = tokenizeWord(pattern)
    link = []

    for tokenNode in tokenList:

        strbuff = word
        flag = False

        while len(strbuff) > 0:

            for token in tokenNode:
                if strbuff in token[1:4]:
                    link.append(token[4])
                    flag = True
                    break

            if flag:
                break
            strbuff = strbuff[:len(strbuff) - 1]
        word = word[len(strbuff):]

    for tokenId in link:
        sql = "update symbols set frequency = frequency+1 where id = %d" % (tokenId)
        cursor.execute(sql)
    schemefile.commit()
    return True


def ui(opts=[]):
    print('TRANSLITERATOR')

    while True:

        word = input("Enter word to transliterate : ")
        wordList = generate_word_list(word)

        print('Possible outputs are')

        for i in range(0, len(wordList)):

            if str(type(wordList[i])) == "<class 'tuple'>":
                print("%d %s" % (i, wordList[i][0]))
            else:
                print("%d %s" % (i, wordList[i]))

        if 'train' in opts:

            index = int(input("Enter the index of exact match : "))
            if index != -1:
                if str(type(wordList[index])) == "<class 'tuple'>":
                    wordl = wordList[index][0]
                else:
                    wordl = wordList[index]

                if isLearnedWord(wordl) == False:
                    learnPatternsFor(wordl)
                else:
                    wordId = \
                    cursor.execute("select wordId from wordList where word = '%s' " % (wordl)).fetchall()[0][0]
                    cursor.execute(
                        "update words set frequency = frequency+1 where pattern = '%s' and wordId = %d" % (
                        word, wordId))
                    schemefile.commit()

                updateTokenFrequency(word, wordl)

        elif len(wordList) == 1:
            if str(type(wordList[0])) == "<class 'tuple'>":
                wordl = wordList[0][0]
            else:
                wordl = wordList[0]
            updateTokenFrequency(word, wordl)  # IS A CONFIDENT MATCH SHOULD TRAIN ON IT TO IMPROOVE QUALITY

        if input("Convert another Word (n/y) ?") == 'n':
            break


if __name__ == "__main__":
    # Only run the code for schema creation and learning if the sqllite database is not already existing
    # as learning process may take hours to complete.
    # createSchemeFile()
    # learnFromFiles(range(0, 6))
    ui(['train'])
