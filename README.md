#Why do we need promises in python ?

Concurrent programming, soon or later every programmer has to do it. 
If you run a server that serves multiple clients, or do heavy scientefic calculations, there are no two ways about it
There are two ways to go about concurrent programming : Synchronous and Asynchronous 

##Synchronous programming :

Synchronous programming is where functions are blocking. In other words, if you call a function `foo` it will not relinquish control till it has completed its execution. 

###How do we acheive concurrency ?

Lets take a concrete example. Say we need to retreive a names, highest upvoted questions and answers of all users whose names start with k in stackoverflow

This translates into 3 calls. Let the functions doing those calls be `getNames`, `getQuestions`, `getAnswers`. We can spawn three threads corresponding to the functions. Mind you the functions also have the logic to handle the data after retreival. Here the functions are still blocking, but since they are being executed in parallel threads, we acheive concurrence here 

##Asynchronous programming:

Here the function calls are non-blocking. That is the function does not wait to relinquish control untill its execution is complete.

###How do we acheive concurrency ?

Lets take the previous example. We can have a parent thread which handles the main execution. We simply spawn a worker thread for the 3 calls that we wish to make. However once the data is retreived we signal the parent thread, which then takes over the processing of the retreived data.

The signalling can be done via events or setting a flag in the shared memory.

Consider this :
```python

import threading as t

def get_data(id):
    
    def __get_data(id):
        """ Logic to retreive data from server based on the id above """
        """ Here we set the shared memory to let the parent thread know that the task is complete"""
        global flags
        flags[id] = True
        
    my_thread = t.Thread(target=__get_data)
    my_thread.start()
    
def handle_data_1():
    """ Logic to handle the data from the first call """
    
def handle_data_2():
    """ Logic to handle the data from the second call """
    
def handle_data_3():
    """ Logic to handle the data from the third call """
    
""" Here signalling is done via flag setting in the shared memory """
flags = [False,False,False,False]
def boss_thread():
    id = 0
    while id < 3:
         get_data(id)
         id += 1
        """ These are the handlers for the data retreived in the worker threads"""
        if flags[0]:
            handle_data_1()
            flags[0] = False
        if flags[1]:
            handle_data_2()
            flags[1] = False
        if flags[2]:
            handle_data_3()
            flags[2] = False
            
        """ Do some processing here in the parent thread """
    
    
boss_thread()
```
Here the thread on which the async function was executed will continue running without blocking as for the potential blocking network/IO operations are offloaded to back ground threads which will carryout the operations and signal completion of their tasks by event dispatching or by setting a flag in shared memory.

The result is then collected and processed in the thread running the async function

###Event loops :
Multi-threading is not the only way to do asynchronous programming though, We can also do it in a single threaded context.
Here enter event loops. Event loops consist of two parts. An infinite loop called the reactor which listens for events and a queue caled the messaging queue, which has a list of functions that have to be executed in the current context.

An async function here almost always accepts a call-back, that is a function as an argument. That function will be executed later when the async operation is done

Whenever we wish to execute a async function, the function returns immediatly and the execution context dispatches the blocking code and simply waits for the result to appear. For example after sending the call to a remote url the context will wait for response to appear. Mind you since the data is on external network, in the process of arriving, the waiting here doesnt have to block execution. Meanwhile since the async function has returned further processing can continue

Once the response appears an event is dispatched for the same. That causes the call-back passed to the async function to be enqueued.

The messaging queue checks wether a function is executing in the current stack. If not a function is removed in the queue and executed.

Here is a pseudo-sample of how the event loop might work.
```python
import Queue

message_queue = q.Queue(10)
def get_data(post_id,callback):
    """ Make a call to get data from remote, we set the event dispatcher to broadcast an event when data arrives """
    event_dispatcher.markForBroadcast(callback)

def event_loop():
    while True:
       if event_dispatcher.event is not None :
          message_queue.put(event_dispatcher.event.callback)
          
       if not message_queue.empty() :
          callback = message_queue.get()
          callback()
                
event_loop()
```

Whenever we execute any async function, that function will be put in the queue by the execution context
##Multi-threading :

Multi-threading allows you to have parallel flow of execution either by time-slicing or by executing on multiple cores
Operation that we perform are usually either processor bound or IO bound.

IO bound operation spend relatively large time waiting for response, doing nothing.

##The Global interpretor lock :

python, although spawns kernel threads, but at the level of the language interpretor can only run a single python thread at a time
the implication being even in a multi-core system true parallel execution is not possible in python systems. Unless we spawn sub-processes that is

##Where are python threads usefull ?

They are generally usefull for threads which are IO bound as python can schedule and switch to other threads when the IO thread is waiting

##Enter Asynchronous programming :

This is another paradigm for concurrent programming, it is generally described as being event-driven. that is we have an event loop
on a single thread, which listens to events and executes the functions accordingly. Most famous example here would be node.js

asynchrnous programming is a good fit for IO bound operations as we are essentially run a single loop without the over head of thread creation and context switching. Not to mention the synchronisation efforts that go along with threads, like semaphores and mutexes

Also asynchrnous programming is used in GUI environment

asynchronous programming being event driven , heavily depends on call-backs

##Callbacks ?? :

A type of inversion of control, callbacks are basically higher-order functions, fancy term for functions that can be passed to other functions as arguments

programming using callbacks for event handlers requires a change of perspective but is pretty cool once you get used to it

However callbacks present us with a problem, say we want to execute blocks of code synchronously , one after another.

For example , say we want to retreive the id of an employee first and then make a call using that id to get his details

things can are never this simple and real life and the situations leads to a phenomenon called call-back-hell. Here enter promises

##Promises :

They are a design pattern
That allow you to write asynchronous code in a synchronous manner. instead passing functions inside functions you can simply chain the calls
thus greatly simplyfying the logic flow of the code

The implementation of promises we will be using is defer from twisted. on ubuntu do apt-get install python-twisted
on RHEL/Centos yum install python-twisted

A promise basically is a representation of unfinished work, a token that the information will be arriving in future.
Twisted calls the object deffered object.

The most important method we will be needing : addCallbacks

addCallBacks basically takes two arguments success callback and failure call back.
the function also returns a deffered object itself, so you can chain the calls and write code that feels synchronous despite its nature

both success and error cal backs recieve success and failure objects as arguments, the failure object is a wrapper over the exception object in python which has deffered specicfic menthods

failure is induced by throwing an exception in one of the call-backs

promises basically help separate out the concerns, that is instead of writing the logic inside the callbacks at the same place, you can split the logic between different parts of the program, with the deffered object acting as the common currency 
