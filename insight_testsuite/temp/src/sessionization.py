#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/

from datetime import datetime, date, time, timedelta
import sys

ipSessions = dict()

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def sessionInactive(session, inactivePeriod, dateTime):
    if session and not session.isActive(inactivePeriod, dateTime):
        return True
    
def reportAndDeleteSessions(outFile, conditional = None):
    global ipSessions

    if conditional:
       inactivePeriod = conditional[0]
       requestDateTime = conditional[1]
       pred = conditional[2]

    if len(ipSessions) > 0:
        for ip,session in ipSessions.items():
            if session and (conditional and pred(session, inactivePeriod, requestDateTime) or not conditional):
                outString = ip+','+session.toString()
                print(outString.rstrip(), file = outFile)
                print(outString)
                ipSessions=removekey(ipSessions,ip)
                
def openFile(fileName, mode):
    try:
        return open (fileName, mode)
    except IOError as e:
        sys.exit("program failed: Input/Output error: %s" % ( str(e) ) )

    
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
    in_edgarLog = openFile(in_edgarLog_path, 'rt')
    
    in_inatctPeriod_path = '../insight_testsuite/tests/test_1/input/inactivity_period.txt' if len(sys.argv) < 4 else sys.argv[2]
    in_inactPeriod = openFile(in_inatctPeriod_path, 'rt')

    out_sessionization_path = '../insight_testsuite/tests/test_1/output/sessionization2.txt' if len(sys.argv) < 4  else sys.argv[3]
    out_sessionization = openFile(out_sessionization_path, "wt")

    inactivityPeriod = int(in_inactPeriod.read())
    
    head = True
    for line in in_edgarLog:
        if head:
            fields = line.rstrip().split(',')
            head = False
        else:
            values = line.rstrip().split(',')
            #Process record if it references a valid document?
            if (values[fields.index('cik')] and values[fields.index('accession')] and values[fields.index('extention')]):
                try:
                    ip = values[fields.index('ip')]
                    date = values[fields.index('date')]
                    time =  values[fields.index('time')]
                    dateTime = date+'-'+time
                    datetime_object = datetime.strptime(dateTime, '%Y-%m-%d-%H:%M:%S')
                    reportAndDeleteSessions(out_sessionization, (inactivityPeriod,datetime_object, sessionInactive))
                    if ip in ipSessions.keys():
                        currentSession = ipSessions.get(ip)
                        if currentSession and currentSession.isActive(inactivityPeriod, datetime_object):
                            currentSession.addDocumentRequest(datetime_object)
                        else:           #overwrite IP session record
                            ipSessions[ip] = Session (datetime_object)
                    else: #create an IP session record
                        ipSessions[ip] = Session (datetime_object)
                except Exception:
                    print('Invalid EDGAR weblog record: Record Skiped')
                    
    reportAndDeleteSessions(out_sessionization)

    in_edgarLog.close()
    in_inactPeriod.close()
    out_sessionization.close()
    

         
if __name__ == '__main__': main()
