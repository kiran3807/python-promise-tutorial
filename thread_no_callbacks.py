import urllib2 as u
import json
import time
import threading as t

def get_data(post_id,data):
    
    def __get_data():
        site= "http://jsonplaceholder.typicode.com/posts/" + str(post_id)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = u.Request(site,headers=hdr)
        raw_data = u.urlopen(req).read()
        time.sleep(4)
        print "data received -- " + str(len(data) )
        data.append(json.loads(raw_data)['title'] )
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()
    
def boss_thread():
    data = []
    current = 0
    while len(data) < 3:
        if len(data) == current:
            get_data(current+1, data)
            current += 1
        time.sleep(2)
        print "processing"
    
    
boss_thread()

    







