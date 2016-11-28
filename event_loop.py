import socket as s
import Queue as q
import time

def get_data(post_id,callback):
    global temp_store, sock_obj
    
    sock = s.socket(s.AF_INET,s.SOCK_STREAM)
    host = 'jsonplaceholder.typicode.com'
    port = 80
    """ Must leave an empty space below the message, its part of the http spec """
    message = """GET /users/{0} HTTP/1.1
Host: jsonplaceholder.typicode.com
Accept: */*

""".format(post_id)
    remote_ip = s.gethostbyname(host)
    sock.connect((remote_ip,port))

    sock.send(message)
    sock.setblocking(0)
    temp_store[callback.__name__] = [sock,callback,'']

""" These are the call backs we will be passing to get_data function """    
def call_back_2(res):
    print "call back 2"
        
def call_back_3(res):
    print "call back 3"
    
def call_back_1(res):
    print "call back 1"
    
""" this checks if the entire json payload has arrived or not """    
def check_end(message):
    that = False
    if message[-1] == '}' and message[-2] != ' ':
        that = True
    return that

""" This is an example of a function we may execute in an async context """    
def main():
    count = 0
    print "processing starts"
    
    get_data(1,call_back_1)
    
    while count < 2 :
        time.sleep(1)
        print "processing"
        count += 1
        
    get_data(2,call_back_2)
    
    count = 0
    while count < 3 :
        time.sleep(1)
        print "processing"
        count += 1
        
    get_data(3,call_back_3)
    
queue = q.Queue(10)
sock_arr = []
temp_store = {}
""" Initialising the queue. """
queue.put((main,None))
def event_loop():
    while True:
        """ Here the non-blocking socket throws an exception if data has not been completely transfered and we try reading from it """
        try:
            for key in temp_store:
                sock = temp_store[key][0]
                temp_store[key][2] += sock.recv(6553)
                if check_end(temp_store[key][2]):
                """ Once the data has been fetched we push the call back into the message queue """
                    queue.put( (temp_store[key][1], temp_store[key][2] ) )
                    del temp_store[key]   
        except :
            pass
        if not queue.empty():
            function,arg= queue.get()
            if arg is None:
                function()
            else :
                function(arg)
                
event_loop()
            
            
