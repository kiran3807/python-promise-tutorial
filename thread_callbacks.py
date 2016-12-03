import urllib2 as u
import json
import time
import threading as t
import random

""" The oberver here works like an event dispatcher, executing the callbacks in the order they were registered """
class Observer(object):

    def __init__(self):
        self.callback_list = []
        
    def register(self,callback,post_id):
            
        self.callback_list.append( (callback, post_id) )
        
    def trigger(self, current_id, result):
        for callback, associated_id in self.callback_list:
            if current_id == associated_id:
                callback(result) 
            
        
def get_data(post_id):
    
    global observer
    def __get_data():
        time.sleep(random.randint(1,10))
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        data = json.loads(raw_data)
        print "data received -- " + str(post_id)
        observer.trigger(post_id, data['title'])
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()

  
def async_function_1(callback):
    global observer
    get_data(1)
    if callback is not None:
        observer.register(callback,1)
        
def async_function_2(callback):
    global observer
    get_data(2)
    if callback is not None:
        observer.register(callback,2)
              
def driver():

    def call_back_1(res):
        print "processed data - 1, Here is the data retreived : {0}".format(res)
        
        def call_back_2(res):
            print "processed data - 2, Here is the data retreived : {0}".format(res)
            
        async_function_2(call_back_2)
        
    async_function_1(call_back_1)
      
def boss_thread():
  
    print "processing"
    driver()
    while True :
        time.sleep(2)
        print "processing"
    
    

observer = Observer()
boss_thread()

