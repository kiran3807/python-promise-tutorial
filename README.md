#Why do we need promises ?

Concurrent programming, soon or later every programmer has to do it. 
If you run a server that serves multiple clients, or do heavy scientefic calculations, there are no two ways about it

The most common approach to it is multi-threading.

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
