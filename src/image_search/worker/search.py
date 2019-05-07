from random import randint
from threading import Thread
import time

class SearchThread(Thread):
    def __init__(self, val):
        ''' Constructor. '''

        Thread.__init__(self)
        self.val = val


    def run(self):
        for i in range(1, self.val):
            print('Value %d in worker %s' % (i, self.getName()))

            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = randint(1, 5)
            print('%s sleeping fo %d seconds...' % (self.getName(), secondsToSleep))
            time.sleep(secondsToSleep)
