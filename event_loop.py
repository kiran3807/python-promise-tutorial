import urllib2 as u
import Queue as q
import json
import time

def get_data(index):
    global dataArr
    time.sleep(2)
    site= "http://jsonplaceholder.typicode.com/posts/" + str(index+1)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = u.Request(site,headers=hdr)
    raw_data = u.urlopen(req).read()
    dataArr[index] = json.loads(raw_data)['title']
    print "data received -- " + str(index)

def call_back_2(callback):
    def __internal():
        get_data(1)
        callback(None)
        
    global queue
    queue.put(__internal)
        
def call_back_3(callback):
    def __internal():
        get_data(2)
        
    global queue
    queue.put(__internal)
    
def call_back_1(callback):
    def __internal():
        get_data(0)
        callback(call_back_3)
        
    global queue
    queue.put(__internal)

def should_stop(dataArr):
    value = False
    for v in dataArr:
        if(v is None):
            value = True
            break
    return value
    
""" Here we use static memory location dataArr in liue of event emmiting systems found in real life systems like twisted """
queue = q.Queue(10)
dataArr = [None,None,None]

def event_loop():
    global dataArr
    print "processing"
    call_back_1(call_back_2)
    while should_stop(dataArr) :
        #print dataArr 
        print "processing"
        inner = queue.get()
        inner()
                
event_loop()
            
            
