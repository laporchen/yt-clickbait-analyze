
import json
import nltk

def openJson(path):
    with open(path)as f:
        data = json.load(f, strict=False)
        return data
def writeJson(path,data):
    with open(path, 'w', encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def getToken(str):
    try:
        tokens = nltk.word_tokenize(str)
        return tokens
    except:
        print("Failed to tokenize the string")
        return False

def analyzeBait(str):
    token = getToken(str)
    if(token == False):
        print("Input failed.")
        return "A"
    lowerStr = str.lower()
    #clickbait:common words
    bait = ["only", "impossible", "won't believe", "not believe", "you can't", "you cannot", "just to", "only to", "truth about",
            "reason why", "reasons way", "things you", "this is why", "this is how", "you can now", "ever need", "why you should", "the truth","telling the truth","i'm done","I'm sorry","response to","responses to","this is the"]
    baitCount = 0
    for s in bait:
        if lowerStr.find(s) != -1:
            baitCount += 1
    #clickbait:write a word with all upper cases, LIKE this ,but filer out some words,like NTNU
    cap = 0
    for s in token:
        if s.isupper() and len(s) > 1:
            if s.lower() in nltk.corpus.words.words():
                cap += 1
    #clickbait:some extreme number ,like 99.9999,0.001
    percentCheck = 0
    percentSTR = str
    if percentSTR.find("99.9") != -1 or percentSTR.find("0.00") != -1 or percentSTR.find("0.01") != -1 or percentSTR.find("99%") != -1:
        percentCheck = 1
    #clickbait:putting brackets in the title, example: UFO evidence! (truth)
    bracket = 0
    if token[-1].find("(") != -1 and token[-1].find(")") != -1:
        bracket = 1
    else:
        bracket = 0
   # print(str)
   # print("bait:",baitCount)
   # print("cap : ",cap)
   # print("percent : ", percentCheck)
   # print("bracket : " ,bracket)
   # print("\n")
    if(bracket + percentCheck + cap +baitCount > 0):
        return True
    else:
        return False

if __name__ == "__main__":
    path = "ytTesting.json"
    data = openJson(path)
    output = "result.json"
    importLIST = data["screach_key_word"]
    finalResult = {}
    viewLIST = []
    titleLIST = []
    resultLIST = []
    for video in importLIST:
        try:
            result = analyzeBait(video["title"].replace(","," "))
            if(result != "A"):
                resultData = {}
                titleLIST.append( video["title"])
                viewLIST.append(video["view"])  
                resultLIST.append(result)
        except:
            continue
    finalResult["result"] = resultLIST
    finalResult["view"] = viewLIST
    finalResult["title"] = titleLIST
    writeJson(output, finalResult)
    