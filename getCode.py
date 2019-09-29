import urllib.request, sys

url = ""
outputPath = ""
codesInformation = ""
_keyWords = []


JS_INIT = '<script'
JS_FINAL = '</script>'
isJs = False

CSS_INIT = '<style'
CSS_FINAL = '</style>'
isCss = False

SOURCE_INIT = '<link'
isSources = False

for paramIndex in range(0, len(sys.argv)):
    if (paramIndex == 1):
        url = sys.argv[paramIndex]
    elif (paramIndex == 2):
        outputPath = sys.argv[paramIndex]
    elif (paramIndex == 3):
        codesInformation = sys.argv[paramIndex]
    elif (paramIndex == 4):
        if (sys.argv[paramIndex] == "y"):
            isSources = True

if (url == "" or outputPath == "" or codesInformation == ""): sys.exit()

if (codesInformation != ""):
    for symb in codesInformation:
        if (symb == "j"):
            isJs = True
        elif (symb == "c"):
            isCss = True
        else:
            print("I don't know what is " + symb)

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

try:
    _pageContent = urllib.request.urlopen(url).read().decode("utf8")
except urllib.error.HTTPError:
    print("Error 403 - Forbidden. Here is good protection.")
    sys.exit()

if (isJs):
    _keyWords.append((JS_INIT, JS_FINAL))

if (isCss):
    _keyWords.append((CSS_INIT, CSS_FINAL))

initIndex = []
finalIndex = []
resultArr = []
sourceInitIndexes = []
sourceFinalIndexes = []
resultCSSSources = []

for keyWord in _keyWords:
    for i in find_all(_pageContent, keyWord[0]):
        initIndex.append(i)

    for i in find_all(_pageContent, keyWord[1]):
        finalIndex.append(i)

if (isSources):
    for i in find_all(_pageContent, SOURCE_INIT):
        sourceInitIndexes.append(i)

    for i in find_all(_pageContent, ">"):
        sourceFinalIndexes.append(i)

    sources = []

    for sourceInitIndex, sourceFinalIndex in zip(sourceInitIndexes, sourceFinalIndexes):
        sourceInitRange = list(find_all(_pageContent[sourceInitIndex + _pageContent[sourceInitIndex : sourceFinalIndex].find("href") : sourceInitIndex + _pageContent[sourceInitIndex : sourceFinalIndex].find("href") + 120], '"'))

        sources.append(_pageContent[sourceInitIndex + _pageContent[sourceInitIndex : sourceFinalIndex].find("href") + sourceInitRange[0] + 1 : sourceInitIndex + _pageContent[sourceInitIndex : sourceFinalIndex].find("href") + sourceInitRange[1]])

    for source in sources:
        # print(source)
        if ("css" not in source):
            sources.remove(source)
        else:
            print(source)
            if ("http" in source):
                resultCSSSources.append(source)
            else:
                toAddUrl = url[: list(find_all(url, "/"))[2]] + source
                try:
                    _page = urllib.request.urlopen(toAddUrl).read().decode("utf8")
                except:
                    toAddUrl = url + source
                finally:
                    resultCSSSources.append(toAddUrl)
    
    if (len(sources) > 0):
        print("Sources are detected!")

for keyInit, keyFinal in zip(initIndex, finalIndex):
    resultArr.append(_pageContent[keyInit + _pageContent[keyInit : keyFinal].find(">") + 1 : keyFinal])
print("Main page parsed.")

if (isSources and len(resultCSSSources) > 0):
    print(resultCSSSources)
    print("Starting parsing other pages...")

    for source in resultCSSSources:
        try:
        # print(source)
            _page = urllib.request.urlopen(source).read().decode("utf8")
        except:
            print("Unexpected error.")
            sys.exit()
        print(_page)
        resultArr.append(_page)


with open(outputPath, "w") as file:
    for line in resultArr:
        try:
            file.write(line)
        except:
            print("We've got some error.")

if (len(resultArr) > 0): print("Data is written.")