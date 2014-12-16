## FCFS queues
import simpy
import sys
from math import *
from SimPy.Simulation import *
from random import expovariate, seed

## Model components ------------------------
class QN():   
    def model(self, nrRuns, num, arrInt, endTime):
        averageRespTimeSum = 0
        probMetDeadline = 0
        for runNr in range(nrRuns):
            self.wm1 = Monitor(name='ResponseTime')
            self.numberMeetDeadline = 0
            
            initialize()
            source = Source(self)
            activate(source,source.generate(num, arrInt, processors), at=0.0)
            simulate(until=endTime)
            
            result1 = self.wm1.count(), self.wm1.mean(), self.wm1.total()
            averageRespTimeSum = averageRespTimeSum + self.wm1.mean()
            print("Average response time for %3d completions was %5.3f seconds. Total response time = %3d." % result1)
            probMetDeadline = probMetDeadline + (self.numberMeetDeadline/self.wm1.count())
            print("%d out of %d Jobs met the response time requirement of %5.3f" % (self.numberMeetDeadline, self.wm1.count(), responseTimeReq))
            print ("%s run(s) completed" %(runNr + 1))

        print("****************************************************************************")    
        print("Average response time over %d runs is %5.3f seconds." % (nrRuns, averageRespTimeSum/nrRuns))
        print("Probability of Jobs that met the response time requirement of %5.3f over %d runs is %f" % (responseTimeReq, nrRuns, probMetDeadline/nrRuns))
        print("****************************************************************************")
                
class Source(Process):
    ## Source generates jobs randomly
    def __init__(self,sys):
        Process.__init__(self)
        self.sys = sys

    def generate(self, number, interval, processors):
        for i in range(number):
            c = Job("Job%02d" % (i), i, self.sys)
            activate(c, c.visit(processors))
            t = expovariate(1.0/interval)
            yield hold, self, t

class Job(Process):
    ## Job arrives, chooses the shortest queue is served and leaves
    def __init__(self,name,i,sys):
        Process.__init__(self)
        self.name=name
        self.i=i
        self.sys = sys
        
    def visit(self, processors):
        arrive = now()
        print ("%8.5f %s: Arrives     "%(now(),self.name))
        if self.i%2 == 0:
            yield request,self,processors[0]
            wait = float(now()-arrive)
            print ("%8.5f %s: Waited for %6.5f for processor %i"%(now(),self.name,wait, 0))
            tiw = expovariate(1.0/serviceTime)
            yield hold,self,tiw                      
            yield release,self,processors[0]
            
        j = random.randint(1, 10)
        wait = now()
        while j < 4:
            if j <= 2:
                yield request,self,processors[1]
                wait = float(now()-wait)
                print ("%8.5f %s: Waited for %6.5f for processor %i"%(now(),self.name,wait, 1))
                tiw = expovariate(1.0/serviceTime)
                yield hold,self,tiw                      
                yield release,self,processors[1]
            elif j > 2 and j <= 4:
                yield request,self,processors[2]
                wait = float(now()-wait)
                print ("%8.5f %s: Waited for %6.5f for processor %i"%(now(),self.name,wait, 2))
                tiw = expovariate(1.0/serviceTime)
                yield hold,self,tiw                      
                yield release,self,processors[2]
            i = random.randint(1, 10)
            wait = now()
        
        print ("%8.5f %s: Finished      "%(now(),self.name))
        responseTime = now() - arrive
        print("%8.5f %s Response time: %2f" % (now(), self.name, responseTime))
        if responseTime <= responseTimeReq:
            self.sys.numberMeetDeadline = self.sys.numberMeetDeadline + 1
        self.sys.wm1.observe(responseTime)
        
## Parameters -------------------------
maxNumber = 80
endTime = 20000.0    ## second
serviceTime = 30
arrInt = 300     ## mean, seconds
nrRuns = 3
theseed = 787878
responseTimeReq = 100
Nc = 3             ## number of counters
processors = [Resource(name="VM1"), Resource(name="VM2"), Resource(name="VM3")]

## Model ------------------------------
seed(theseed)
plt=QN()
plt.model(nrRuns, maxNumber, arrInt, endTime)
