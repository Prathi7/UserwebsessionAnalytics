"""
* * * * * * * * * * * * * * * * * * * * * * *
INSIGHT DataEngineering- Solution 
April 5,2018
* * * * * * * * * * * * * * * * * * * * * * *
"""


import datetime
import collections
import argparse


def datetime_str(recorddatetime):
    return recorddatetime.strftime("%Y-%m-%d %H:%M:%S")

class Session:
    doccount=0
    def __init__(self, inputrecord, session_duration):
        self.ip=inputrecord.ip
        self.docs=set()
        self.docs.add(inputrecord.doc)
        self.startdatetime= inputrecord.startdatetime
        self.enddatetime = inputrecord.startdatetime
        self.sessionenddatetime = inputrecord.startdatetime + session_duration

    def update(self, inputrecord, session_duration):#updating key in dictionary
        if(inputrecord.ip == self.ip):
            self.docs.add(inputrecord.doc)
            self.enddatetime = inputrecord.startdatetime
            self.sessionenddatetime = inputrecord.startdatetime + session_duration

    def output(self):#format to o/p file
        duration = self.enddatetime - self.startdatetime
        return "{},{},{},{},{}".format(self.ip, datetime_str(self.startdatetime), datetime_str(self.enddatetime), int(duration.total_seconds()+1), len(self.docs))

class ReadRecord:

    def __init__(self, recordstring):
        self.parse_record(recordstring)

    def parse_record(self,recordstring):#reading i/p record
        splits = recordstring.split(",")
        self.ip =  splits[0]
        startdate = datetime.datetime.strptime(splits[1],"%Y-%m-%d").date()
        starttime = datetime.datetime.strptime(splits[2],"%H:%M:%S").time()
        self.startdatetime = datetime.datetime.combine(startdate,starttime)
        self.doc = (splits[4], splits[5], splits[6])

class Solution(object):
    
    def __init__(self):
        self.records_dic = collections.OrderedDict()

    def record(self,inputrecord, session_duration, outputfile):
        temp=[]
        for key,value in self.records_dic.items():
            if value.sessionenddatetime < inputrecord.startdatetime: # if session has ended, write to o/p file
                outputfile.write(value.output()+"\n")
                #del self.records_dic[key]
                temp.append(key)
        [self.records_dic.pop(k) for k in temp]

        if not inputrecord.ip in self.records_dic: #if not in Dictionary, add key & values
            self.records_dic[inputrecord.ip]= Session(inputrecord, session_duration)
        else: # if present in Dictionary, update values for key
            self.records_dic[inputrecord.ip].update(inputrecord, session_duration)

    def run(self):
        parser = argparse.ArgumentParser()      
        parser.add_argument()
        argv= parser.parse_args()
        
        with open(argv[1],"r") as iptxt:#Read i/p .txt file
            session_duration=datetime.timedelta(seconds=int(iptxt.read()))#Convert to time format
            
        optxt=open(argv[2],"w+")#create o/p .txt file
        
        with open(argv[0], "r") as f:#Read each line of i/p .csv file
            f.readline() #skip header
            for line in f :
                inputrecord = ReadRecord(line)
                self.record(inputrecord, session_duration, optxt)

        for key, value in self.records_dic.items(): #At the end,writing o/p to all open sessions
            optxt.write(value.output()+"\n")

if __name__ == "__main__":
    Solution().run()
