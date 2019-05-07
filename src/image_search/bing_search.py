# -*- coding: utf-8 -*-

import http.client, urllib.parse, json
import urllib.request

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "sub-key-of-bing-image-search"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/images/search"

term = "cat garden"

def BingImageSearch(search, count, offset):
    "Performs a Bing image search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query + "&count="+str(count) + "&offset="+str(offset), headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
               if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

if len(subscriptionKey) == 32:

    print('Searching images for: ', term)

    headers, result = BingImageSearch(term, 2,0)
    result = json.loads(result)
    for img in result["value"]:
        contentUrl = img["contentUrl"]
        imageId = img["imageId"]
        encodingFormat = img["encodingFormat"]
        urllib.request.urlretrieve(contentUrl, imageId+"."+encodingFormat)
else:
    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")