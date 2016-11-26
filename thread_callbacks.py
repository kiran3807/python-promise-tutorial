import urllib2 as u
import json
import time
import threading as t
            
def get_data(post_id):
    
    def __get_data():
        time.sleep(2)
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        print "data received -- " + str(post_id)
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()

def call_back_3(callback):
    get_data(3)
    if callback is not None:
        callback(None)
        
def call_back_1(callback):
    get_data(1)
    if callback is not None:
        callback(call_back_3)
    
def call_back_2(callback):
    get_data(2)
    if callback is not None:
        callback(None)
    
def boss_thread():
    count = 0
    print "processing"
    call_back_1(call_back_2)
    while True :
        time.sleep(2)
        print "processing"
    
    
    
boss_thread()

    







