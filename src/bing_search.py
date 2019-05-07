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