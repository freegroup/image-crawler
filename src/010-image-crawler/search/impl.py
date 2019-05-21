import queue
import http.client, urllib.parse, json
import urllib.request
from threading import Thread
from configuration import Configuration

conf = Configuration()


class BingSearchWorker(Thread):
    def __init__(self, queue_input, queue_output):
        Thread.__init__(self)
        self.setDaemon(True)
        self.__terms = queue_input
        self.__queue_output = queue_output
        self.__current_term = None

        if len(conf.search("subscription_key")) != 32:
            print("Invalid Bing Search API subscription key!")
            print("Please paste yours into the source code.")

    def run(self):
        "Performs a Bing image search and returns the results."

        count = 100
        offset = 0
        while True:
            try:
                self.__current_term = self.__terms.get(block=True, timeout=1)
                self.search(self.__current_term, count, 0)
                offset = count

            except queue.Empty:
                if self.__current_term:
                    self.search(self.__current_term, count, offset)
                    offset = offset+count

    def search(self, term, count, offset):
        print("perform new search term: " + term + " index: "+str(offset))

        headers = {'Ocp-Apim-Subscription-Key': conf.search("subscription_key")}
        conn = http.client.HTTPSConnection(conf.search("host"))
        query = urllib.parse.quote(self.__current_term)
        conn.request("GET", conf.search("uri") + "?q=" + query + "&count="+str(count) + "&offset="+str(offset), headers=headers)
        response = conn.getresponse()
        response = response.read().decode("utf8")
        result = json.loads(response)
        for img in result["value"]:
            self.__queue_output.put({
                'url': img["contentUrl"],
                'width': img["width"],
                'height': img["height"]
            })


