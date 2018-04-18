#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/

from datetime import datetime, date, time, timedelta
import operator  # this is for sorting
import sys

ipSessions = dict()
#ipSessions = []

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def sessionInactive(session, dateTime):
    if session and not session.isActive(2, dateTime):
        return True
    
def flushSessions(inactivePeriod = None, requestDateTime = None, pred = None):
    global ipSessions
    if len(ipSessions) > 0:
        for ip,session in ipSessions.items():
            if session and (pred and pred(session, requestDateTime) or not pred):
                outString = ip+','+session.toString()
                print(outString)
                ipSessions[ip] = None
    
class Session:
    def __init__(self, requestDateTime):
        self._requestCount = 1 
        self._firstRequestDateTime= requestDateTime
        self._lastRequestDateTime = requestDateTime

    def docRequests(self):
        return self._requestCount
            
    def isActive(self, inactivePeriod, requestTime):
        if (self._lastRequestDateTime + timedelta(seconds = inactivePeriod) >= requestTime):
                return True
        else:
                return False
            
    #should only be called if is active
    def addDocumentRequest (self, requestDateTime):
        self._requestCount = self._requestCount + 1
        self._lastRequestDateTime=requestDateTime
        
    def toString(self):
        return(self.__str__())
            
    def __str__ (self):
        duration = self._lastRequestDateTime - self._firstRequestDateTime 
        return (self._firstRequestDateTime.strftime('%Y-%m-%d %H:%M:%S') + ',' + self._lastRequestDateTime.strftime('%Y-%m-%d %H:%M:%S') + ','
           +  str (int(duration.total_seconds()) + 1)+ ',' +  str(self.docRequests()) )    
                
def main():
    
    in_edgarLog_path =  '../insight_testsuite/tests/test_1/input/log.csv' if len(sys.argv) < 4 else sys.argv[1]
    in_edgarLog = open(in_edgarLog_path, 'rt')
    
    in_inatctPeriod_path = '../insight_testsuite/tests/test_1/input/inactivity_period.txt' if len(sys.argv) < 4 else sys.argv[2]
    in_inatctPeriod = open(in_inatctPeriod_path, 'rt')


    out_sessionization_path = '../insight_testsuite/tests/test_1/output/sessionization2.txt' if len(sys.argv) < 4  else sys.argv[3]
    out_sessionization = open(out_sessionization_path, "wt")

    head = True
    for line in in_edgarLog:
        if head:
            fields = line.rstrip().split(',')
            head = False
        else:
            values = line.rstrip().split(',')
            if (values[fields.index('cik')] and values[fields.index('accession')] and values[fields.index('extention')]):
                ip = values[fields.index('ip')]
                date = values[fields.index('date')]
                time =  values[fields.index('time')]
                dateTime = date+'-'+time
                datetime_object = datetime.strptime(dateTime, '%Y-%m-%d-%H:%M:%S')
                flushSessions(2,datetime_object, sessionInactive)
                if ip in ipSessions.keys():
                    currentSession = ipSessions.get(ip)
                    if currentSession and currentSession.isActive(2, datetime_object):
                    #if currentSession:
                        currentSession.addDocumentRequest(datetime_object)
                    else:           #overwrite the IP Session
                        ipSessions[ip] = Session (datetime_object)
                else:
                    ipSessions[ip] = Session (datetime_object)
    flushSessions()
        
def print_dict(o):
    #for x in o: print(f'{x}: {o[x]}')
    for x in o: print(x, {o[x]})
         
if __name__ == '__main__': main()
