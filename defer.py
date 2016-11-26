from twisted.internet import defer
from twisted.python import failure
import time

def callback_1(r):
    time.sleep(2)
    print "call-back 1 done"
    
def callback_1_err(r):
    print "call-back 1 err done"
    
def callback_2(r):
    time.sleep(1)
    print "call-back 2 done"
    
def callback_2_err(r):
    print "call-back 2 err done"
    
    
def callback_3(r):
    time.sleep(3)
    print "call-back 3 done"
    
def callback_3_err(r):
    print "call-back 3 err done"
    
    
def returns_promise():
    print "program starts"
    promise = defer.Deferred()
    return promise
    
def main():
    print "processing"
    promise = returns_promise().addCallbacks(callback_1,callback_1_err).addCallbacks(callback_2,callback_2_err).addCallbacks(callback_3,callback_3_err)
    promise.callback('success')
    
main()
    

    
