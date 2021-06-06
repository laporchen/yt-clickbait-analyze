
import json
import nltk
import os
import time

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def openJson(path):
    with open(path)as f:
        data = json.load(f, strict=False)
        return data


def writeJson(path, data):
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
    if(token == False) or isEnglish(str) != True:
        print("Input failed.")
        return "A"
    lowerStr = str.lower()
    # clickbait:common words
    bait = ["99.9","0.00","100%","0.01","99%","only", "impossible", "won't believe", "not believe", "you can't", "you cannot", "just to", "only to", "truth about",
            "reason why", "reasons way", "things you", "this is why", "this is how", "you can now", "ever need", "why you should", "the truth", "telling the truth", "i'm done", "I'm sorry", "response to", "responses to", "this is the"]
    baitCount = 0
    for s in bait:
        if lowerStr.find(s) != -1:
            baitCount += 1
    # clickbait:write a word with all upper cases, LIKE this ,but filer out some words,like NTNU
    cap = 0
    for s in token:
        if s.isupper() and len(s) > 1:
            if s.lower() in nltk.corpus.words.words() or s in nltk.corpus.words.words():
                cap += 1
    # clickbait:putting brackets in the title, example: UFO evidence! (truth)
    bracket = 0
    if token[-1].find("(") != -1 and token[-1].find(")") != -1:
        bracket = 1
    else:
        bracket = 0
    if(bracket + cap + baitCount > 0):
        return True
    else:
        return False

start_time = time.time()
if __name__ == "__main__":
    path = "youtube.json"
    keywordsPath = "keywords.json"
    keywords = openJson(keywordsPath)
    data = openJson(path)
    output = "result/result"
    totalcViews = 0
    totalnocViews = 0
    totalcVids = 0
    totalnocVids = 0
    totalRESULT = []
    totalVIEW = []
    totalTITLE = []
    for kw in keywords["keywords"]:
        cViews = 0
        nocViews = 0
        cVids = 0
        nocVids = 0
        keywordjson = {}
        finalResult = {}
        viewLIST = []
        titleLIST = []
        resultLIST = []
        keywordjson = {}
        print("Now on the word", kw)
        i = 0
        for video in data[kw]:
            try:
                result = analyzeBait(video["title"].replace(",", " "))
                if(result != "A"):
                    if(result == True):
                        cViews = cViews + int(video["view"])
                        cVids = cVids + 1
                        totalcViews = totalcViews + int(video["view"])
                        totalcVids = totalcVids + 1
                    else:
                        nocViews = nocViews + int(video["view"])
                        nocVids = nocVids + 1
                        totalnocViews = totalnocViews + int(video["view"])
                        totalnocVids = totalnocVids + 1
                    resultData = {}
                    titleLIST.append(video["title"])
                    viewLIST.append(video["view"])
                    resultLIST.append(result)
                    totalTITLE.append(video["title"])
                    totalVIEW.append(video["view"])
                    totalRESULT.append(result)
            except:
                continue
        if(cVids == 0):
            finalResult["clickbait_avg_views"] = -1
        else:
            finalResult["clickbait_avg_views"] = cViews/cVids
        if(nocVids == 0):
            finalResult["noclickbait_avg_views"] = -1
        else:
            finalResult["noclickbait_avg_views"] = nocViews/nocVids
        if(nocVids + cVids == 0):
            finalResult["clickbait_per_video"] = -1
        else:
            finalResult["clickbait_per_video"] = cVids/(cVids + nocVids)

        finalResult["video_counts"] = cVids + nocVids
        finalResult["clickbait_video_count"] = cVids
        finalResult["noclclickbait_video_count"] = nocVids
        finalResult["total_views"] = cViews + nocViews
        finalResult["clickbait_views"] = cViews
        finalResult["noclclickbait_views"] = nocViews

        finalResult["result"] = resultLIST
        finalResult["view"] = viewLIST
        finalResult["title"] = titleLIST
        keywordjson[kw] = finalResult
        writeJson(output+"_"+kw+".json", keywordjson)
    cavg = 0
    if(totalcVids == 0):
        cavg = -1
    else:
        cavg = totalcViews/totalcVids
    nocavg = 0
    if(totalnocVids == 0):
        nocavg = -1
    else:
        nocavg = totalnocViews/totalnocVids
    cpv = 0
    if((totalcVids + totalnocVids) == 0):
        cpv = -1
    else:
        cpv = totalcVids/(totalcVids + totalnocVids)
    total = {"clickbait_per_video": cpv, "clickbait_avg_views": cavg,
             "noclickbait_avg_views": nocavg, "video_count": totalcVids + totalnocVids,
             "clickbait_video_count": totalcVids, "noclclickbait_video_count": totalnocVids,
             "total_views": totalcViews + totalnocViews,
             "clickbait_views": cViews,
             "noclclickbait_views":  totalnocViews,"result":totalRESULT,"views":totalVIEW,"title":totalTITLE
             }
    writeJson(output+"_total.json", total)
print("--- %s seconds ---" % (time.time() - start_time))