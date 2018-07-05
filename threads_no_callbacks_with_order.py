import urllib2 as u
import json
import time
import threading as t
import random

SIZE = 3

def get_data(post_id, data):
    def __get_data():
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        print "data received -- " + str(post_id)
        """ Setting the flag and populating the data at the same time """
        data[post_id] = json.loads(raw_data)['title']
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()
    
def handle_data(_id):
    print str(_id) + " has been handled"

def boss_thread():
    """ We use data dict as a collection of flag as it is shared among the threads """
    data = {}
    current = 0
    while len(data) < SIZE:
        if len(data) == current:
            get_data(current+1, data)
            current += 1

        """ These are the handlers for the data retreived in the worker threads"""
        for _id in range(1, SIZE+1):
            if _id in data and data[_id]:
                handle_data(_id)
                data[_id] = False
    
boss_thread()
