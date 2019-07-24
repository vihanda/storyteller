import json
import pprint
import http.client, urllib.request, urllib.parse, urllib.error, base64

def extractSentences(rawText):
    """
    This gives list of sentences from raw text
    """
    return rawText.split('.')

def extractPhrasesFromSentence(sentence):
    """
    gives key phrases from sentence
    """
    #Call API
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': '1487ee9f904042c0bb72c50d8bb4ad3b',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'showStats': 'false',
    })
    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.1/keyPhrases?%s" % params, buildBody(sentence), headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data)
        docArr = jsondata['documents']
        conn.close()
        return docArr[0]['keyPhrases']
    except Exception as e:
        print("[Errno {0}]".format(e))
    ####################################
    return ""


def getImageForPhrase(phrase):
    """
    Calls bing api to get image corresponding to phrase
    """
    # call API
    ########### Python 3.2 #############

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'a4dc6e50a5904c27b8e9be9a03fbc27f',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'q': phrase + "+site:unsplash.com",
        'count': '1',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
        'imageType': 'Clipart',
        'size': 'medium',
        'width': 400,
        'height': 400
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v7.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data)
        valArr = jsondata['value']
        conn.close()
        return valArr[0]['contentUrl']
    except Exception as e:
        print("[Errno {0}]".format(e))
    return ""
    ####################################

def getSentimentForSentence(sentence):
    """
    Gets overall sentiment for the sentence. Return double value between 0 to 1
    """
    #Call API
    ########### Python 3.2 #############
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '1487ee9f904042c0bb72c50d8bb4ad3b',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'showStats': 'false',
    })
    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.1/sentiment?%s" % params, buildBody(sentence), headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data)
        docArr = jsondata['documents']
        conn.close()
        return docArr[0]['score']
    except Exception as e:
        print("[Errno {0}]".format(e))
    ####################################
    return 0

def buildBody(sentence):
    body = {}
    docArr = []
    document = {}
    document["language"] = "en"
    document["id"] = 1
    document["text"] = sentence
    docArr.append(document)
    body["documents"] = docArr
    return json.dumps(body)

def downloadImg(url):
    '''
    This downloads image url to local directory with name same as the file name
    '''

    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    local=url.split('/')[-1]
    urllib.request.urlretrieve(url,local)

def constructFrameData(rawText):
    """
    Returns framelist in format 
    
    frameList = [{
            "sentence": "{sentence1}"
            "images": ["", ""],
            "phrases": ["", ""],
            "sentiment": 0.8
        },
        {
            "sentence": "{sentence2}"
            "images": ["", ""],
            "phrases": ["", ""],
            "sentiment": 0.2
        }
    ]
    

    """
    frameList = []
    sentences = extractSentences(rawText)
    for sentence in sentences:
        phrases = extractPhrasesFromSentence(sentence)
        frame = {}
        frame['sentence'] = sentence
        imagesArr = []
        for phrase in phrases:
            image = getImageForPhrase(phrase)
            imagesArr.append(image)
            downloadImg(image)
        frame["images"] = imagesArr
        frame["phrases"] = phrases

        sentiment = getSentimentForSentence(phrase)
        frame["sentiment"] = sentiment
        frameList.append(frame)

    return frameList



text = "We know that running your own business is rewarding.But sometimes the paperwork can be a drag! Meet Mathew.Matthew is very busy running his own business. Tax time always overwhelms him with paperwork.Paperwork from vendors, the IRS and customers to name a few.So Matthew searches online for a solution and discovers Acme Tax.Acme Tax offers solutions for managing payroll, monthly financial statements and IRS statement reviews.Now Matthew can focus less on paperwork and more on growing his business!"
frameList = constructFrameData(text)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(frameList)
