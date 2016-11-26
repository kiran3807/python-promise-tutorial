import urllib2 as u
import json
import time
import threading as t

from twisted.internet import defer
from twisted.python import failure
            
def get_data(post_id,promise):
    
    def __get_data():
        time.sleep(2)
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        print "data received -- " + str(post_id)
        promise.callback('success')
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()

def call_back_3(result):
    promise = defer.Deferred()
    get_data(3,promise)
    return promise
        
def call_back_1():
    promise = defer.Deferred()
    get_data(1,promise)
    return promise
    
    
def call_back_2(result):
    promise = defer.Deferred()
    get_data(2,promise)
    return promise
    
def boss_thread():
    count = 0
    print "processing"
    call_back_1().addCallback(call_back_2).addCallback(call_back_3)
    while True :
        time.sleep(2)
        print "processing"
    
    
    
boss_thread()

    







