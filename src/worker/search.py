import queue
import http.client, urllib.parse, json
import urllib.request
from threading import Thread


host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/images/search"

class SearchWorker(Thread):
    def __init__(self, conf, queue_query, queue_result):
        Thread.__init__(self)
        self.__conf = conf
        self.__query = queue_query
        self.__result = queue_result
        self.__term = None

        if len(self.__conf.subscription_key) != 32:
            print("Invalid Bing Search API subscription key!")
            print("Please paste yours into the source code.")

    def run(self):
        "Performs a Bing image search and returns the results."

        count = 100
        offset = 0
        while True:
            try:
                self.__term = self.__query.get(block=True, timeout=1)
                self.search(self.__term, count, 0)
                offset = count

            except queue.Empty:
                if(self.__term):
                    self.search(self.__term, count, offset)
                    offset = offset+count


    def search(self, term, count, offset):
        print("performe new search term: "+term+ " index: "+str(offset))

        headers = {'Ocp-Apim-Subscription-Key': self.__conf.subscription_key}
        conn = http.client.HTTPSConnection(host)
        query = urllib.parse.quote(self.__term)
        conn.request("GET", path + "?q=" + query + "&count="+str(count) + "&offset="+str(offset), headers=headers)
        response = conn.getresponse()
        response = response.read().decode("utf8")
        result = json.loads(response)
        for img in result["value"]:
            self.__result.put(img)