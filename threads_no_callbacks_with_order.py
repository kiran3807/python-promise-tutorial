import urllib2 as u
import json
import time
import threading as t
import random

SIZE = 3

def get_data(post_id, data):
    def __get_data():
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id+1)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        print "data received -- " + str(post_id)
        """ Setting the flag and populating the data at the same time """
        data[post_id] = json.loads(raw_data)['title']
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()
    
def handle_data(_id, data):
    print str(_id) + " has received: " + data[_id][:100]

def boss_thread():
    """ We use data dict as a collection of flag as it is shared among the threads """
    data = {} # this should be READONLY since it's accessible
              # and modifiable in both main and child threads.
    started_count = done_count = 0

    while done_count < SIZE:
        if started_count == done_count:
            get_data(started_count, data)
            started_count += 1

        """ These are the handlers for the data retreived in the worker threads"""
        for _id in range(SIZE):
            if _id in data and _id == done_count:
                handle_data(_id, data)
                done_count += 1

boss_thread()
