import urllib2 as u
import json
import time
import threading as t
import random

def get_data(post_id,data):
    
    def __get_data():
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        time.sleep(random.randint(1,10))
        print "data received -- " + str(post_id)
        """ Setting the flag and populating the data at the same time """
        data[post_id] = json.loads(raw_data)['title']
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()
    
def handle_data_1():
    print "1 has been handled"
    
def handle_data_2():
    print "2 has been handled"
    
def handle_data_3():
    print "3 has been handled"
    

def boss_thread():
    """ We use data dict as a collection of flag as it is shared among the threads """
    data = {}
    current = 0
    while len(data) < 3:
        if len(data) == current:
            get_data(current+1, data)
            current += 1
        time.sleep(2)
        """ These are the handlers for the data retreived in the worker threads"""
        if 1 in data and data[1]:
            handle_data_1()
            data[1] = False
        if 2 in data and data[2]:
            handle_data_2()
            data[2] = False
        if 3 in data and data[3]:
            handle_data_3()
            data[3] = False
            
        print "processing"
    
    
boss_thread()

    







