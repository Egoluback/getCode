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

for paramIndex in range(0, len(sys.argv)):
    if (paramIndex == 1):
        url = sys.argv[paramIndex]
    elif (paramIndex == 2):
        outputPath = sys.argv[paramIndex]
    elif (paramIndex == 3):
        codesInformation = sys.argv[paramIndex]

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

for keyWord in _keyWords:
    for i in find_all(_pageContent, keyWord[0]):
        initIndex.append(i)

    for i in find_all(_pageContent, keyWord[1]):
        finalIndex.append(i)

for keyInit, keyFinal in zip(initIndex, finalIndex):
    resultArr.append(_pageContent[keyInit + _pageContent[keyInit : keyFinal].find(">") + 1 : keyFinal])

with open(outputPath, "w") as file:
    for line in resultArr:
        file.write(line)

if (len(resultArr) > 0): print("Data is written.")