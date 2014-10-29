""" Car arriving in 4 different car wash shops.
Car arrives at the car washing machine at random expovariate times, gets washed and leaves for the next car washing shop"""

import simpy
import sys
from math import *
from random import *
from SimPy.Simulation import *

## Model components ------------------------

class Source(Process):
    """ Source generates customers randomly"""
    def generate(self,number,interval,resource, mon):       
        for i in range(number):
            c = Car(name = "Car%02d"%(i,))
            activate(c,c.wash(b=resource, M=mon))
            t = expovariate(1.0/interval)
            yield hold,self,t

class Car(Process):
    """ Car arrives, is washed and leaves """    
    def wash(self,b, M):       
        arrive = now()
        print "%8.5f %s: Arrives     "%(now(),self.name)
        yield request,self,b
        wait = float(now()-arrive)
	wait = float(0.001 if wait == 0 else wait) 
        print "%8.5f %s: Waited for %6.5f"%(now(),self.name,wait)
        M.observe(wait)
        tiw = expovariate(1.0/timeInWasher)
        yield hold,self,tiw                      
        yield release,self,b
        print "%8.5f %s: Finished      "%(now(),self.name)

## Experiment data -------------------------

maxNumber = 6    # maximum of 6 cars
maxTime = 455.0 # minutes                                      
timeInWasher = 5.0  # mean, minutes it takes to clean up a car                         
ARRint = 7       # Create a car every ~7 minutes                         
Nc = 1          # number of counters  
time1 = now()                                       
                                     
## Model  ----------------------------------

def model1(times, runSeed, numbers): 
    ## Car wash shop 1  ----------------------
    print "--------------------------Car wash shop 1 ------------------------"                           
    seed(runSeed)
    k1 = Resource(capacity=Nc,name="Washer", monitored = True)  ## First Monitored Resource
    wM1 = Monitor()                                             ## Monitor
    initialize()
    s = Source('Source')
    activate(s,s.generate(number=numbers,interval=ARRint, resource=k1,mon=wM1),at=times)         
    simulate(until=maxTime)
    value1 = wM1.timeAverage()
    return (wM1.count(),float(0.001 if value1 is None else value1)) 

def model2(times, runSeed, numbers): 
    ## Car wash shop 2  ----------------------
    print "--------------------------Car wash shop 2 ------------------------"                           
    seed(runSeed)
    k2 = Resource(capacity=Nc,name="Washer", monitored = True)  ## Second Monitored Resource
    wM2 = Monitor()                                             ## Monitor
    initialize()
    s = Source('Source')
    activate(s,s.generate(number=numbers,interval=ARRint, resource=k2,mon=wM2),at=times)         
    simulate(until=maxTime)
    value2 = wM2.timeAverage()
    return (wM2.count(),float(0.001 if value2 is None else value2))

def model3(times, runSeed, numbers): 
    ## Car wash shop 3  ----------------------
    print "--------------------------Car wash shop 3 ------------------------"                           
    seed(runSeed)
    k3 = Resource(capacity=Nc,name="Washer", monitored = True)  ## Third Monitored Resource
    wM3 = Monitor()                                             ## Monitor
    initialize()
    s = Source('Source')
    activate(s,s.generate(number=numbers,interval=ARRint, resource=k3,mon=wM3),at=times)         
    simulate(until=maxTime)
    value3 = wM3.timeAverage()
    return (wM3.count(),float(0.001 if value3 is None else value3))

def model4(times, runSeed, numbers): 
    ## Car wash shop 1  ----------------------
    print "--------------------------Car wash shop 4 ------------------------"                           
    seed(runSeed)
    k4 = Resource(capacity=Nc,name="Washer", monitored = True)  ## Fourth Monitored Resource
    wM4 = Monitor()                                             ## Monitor
    initialize()
    s = Source('Source')
    activate(s,s.generate(number=numbers,interval=ARRint, resource=k4,mon=wM4),at=times)         
    simulate(until=maxTime)
    value4 = wM4.timeAverage()
    return (wM4.count(),float(0.001 if value4 is None else value4))
                        

## Experiment/Result  ----------------------------------

theseeds = [393939,31555999,777999555,319999771]
global maxNum
maxNum = maxNumber
orig_time = now()
for Sd in theseeds:
    while maxNum > 0:  
        print "Please enter your probability for the first stage (0 < pr <= 1): "
        pr = input()
        if pr <= 0 or pr > 1:
	    print "System is in hibernation"
	    print "exiting now."
	    sys.exit()
        elif pr == 1:
            time1 = now() 
            number1 = maxNum
	    ## Result 1  ----------------------------------
  	    print "\nIn Car wash shop 1,"
            result = model1(time1, Sd, number1)
	    print "For car wash shop 1, "
            print "Average wait for %3d completions was %6.5f minutes."% result
	    print "-------------------------------------------------------------------------" 
        elif pr > 0 and pr < 1:
            time1 = now() 
	    number1 = int(floor(pr * maxNum))
	    number2 = int(ceil((1 - pr) * maxNum))
	    ## Result 2  ----------------------------------
  	    print "\nIn Car wash shop 1,"
 	    result1 = model1(time1, Sd, number1)
	    time2 = now()
	    print "\nIn Car wash shop 2,"
            result2 = model2(time2, Sd, number2)
	    print "For car wash shop 1, "
	    print "Average wait for %3d completions was %6.5f minutes."% result1
	    print "For car wash shop 2, "
            print "Average wait for %3d completions was %6.5f minutes."% result2
	    print "-------------------------------------------------------------------------"
        else: continue

        print "Please enter your probability for the second stage (0 < prob <= 0.8):"
        prob = input()
        if prob <= 0 or prob > 0.8:
	    print "System is in hibernation"
	    print "exiting now."
	    sys.exit()
        elif prob == 0.8: 
            time1 = now() 
	    n1 = int(prob * maxNum)
            ## Result 3  ----------------------------------
  	    print "\nIn Car wash shop 3,"
            res = model3(time1, Sd, n1)
	    respTime = float(now() - orig_time)
	    print "For car wash shop 3, "
            print "Average wait for %3d completions was %6.5f minutes."% res
	    print "-------------------------------------------------------------------------"
	    remNum = maxNum - n1
	    if remNum == 1:
	        print "Average response time of the last %d car is %6.5f minutes." %(remNum, respTime)
	    elif remNum > 1: 
	        print "Average response time of the last %d cars is %6.5f minutes." %(remNum, respTime)
	    maxNum = n1
        elif prob > 0 and prob < 0.8: 
            time1 = now()
	    n1 = int(floor(prob * maxNum))
	    n2 = int(ceil((0.8 - prob) * maxNum)) 
            ## Result 4  ----------------------------------
  	    print "\nIn Car wash shop 3,"
	    res1 = model3(time1, Sd, n1)
	    time2 = now()
	    print "\nIn Car wash shop 4,"
            res2 = model4(time1, Sd, n2)
	    respTime = float(now() - orig_time)
	    print "For car wash shop 3, "
            print "Average wait for %3d completions was %6.5f minutes."% res1
	    print "For car wash shop 4, "
	    print "Average wait for %3d completions was %6.5f minutes."% res2
	    print "-------------------------------------------------------------------------"
	    remNum = maxNum - (n1 + n2)
	    if remNum == 1:
	        print "Average response time of the last %d car is %6.5f minutes." %(remNum, respTime)
	    elif remNum > 1: 
	        print "Average response time of the last %d cars is %6.5f minutes." %(remNum, respTime)
            maxNum = n1 + n2
        else: continue
