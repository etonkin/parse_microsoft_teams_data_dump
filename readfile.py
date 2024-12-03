import sys;
import csv;
import json
import re
import pytz
from datetime import datetime
import urllib
from pprint import pprint


tz=pytz.timezone('UTC');

with open('messages.json') as f:
    d=json.load(f)
    # Make a list of conversations to choose from
    conversationlist=[]
    for conv in d['conversations']:
        try:
            if 'threadProperties' in conv.keys():
                conversationlist.append(json.dumps(conv['threadProperties']['topic']));
        except:
            next;
        
    conversationlen=len(conversationlist)
    print("Choose from the following list of conversations to print detail:")
    for i in range(0,conversationlen):
        print(str(i)+' '+conversationlist[i])

    targetconv=input("Enter conversation ID: ")
    print("Producing description of conversation "+targetconv+': '+conversationlist[int(targetconv)]);

    durationregex="<duration>(.+?)</duration>";
    durationpattern=re.compile(durationregex);

    for conv in d['conversations']:
        try:
            if 'threadProperties' in conv.keys():
                if(conversationlist[int(targetconv)] in json.dumps(conv['threadProperties']['topic'])):
                    print(conv['threadProperties']['topic']);
                    topic=conversationlist[int(targetconv)]; 
                    participantlist=[];
                    decoder=json.JSONDecoder()
                    participantlist=decoder.decode(conv['threadProperties']['members'])
                    print("Participants in the conversation:");
                    for i in participantlist:
                        print(i);
                    participants=",".join(participantlist).replace('"','')
                    print("Meeting instances and datetimes:");
                    #print(json.dumps(conv['MessageList'],indent=4))
                    callinstances={};
                    for i in conv['MessageList']:
                        print(json.dumps(i,indent=4))
                        contacttype=i['messagetype'];
                        print(contacttype);
                        # create array of type if doesn't exist 
                        if not callinstances.get(contacttype):
                            callinstances[contacttype]=[]
                        originalarrivaltime=i['originalarrivaltime']; 
                        displayName=i['displayName'];
                        properties=i['properties']
                        threadid=i['id']; 
                        content=i['content']; 
                        
                        duration=re.findall(durationpattern, content)
                        duration=duration[0] if len(duration)>0 else ''
                        instance={};
                        instance['displayName']=displayName;
                        instance['threadid']=threadid;
                        instance['originalarrivaltime']=originalarrivaltime;
                        parsedtime=datetime.fromisoformat(originalarrivaltime) 
                        london_tz=pytz.timezone('Europe/London')
                        london_time=parsedtime.astimezone(london_tz);
                        instance['adjustedtime']=london_time.strftime("%Y-%m-%d %H:%M:%S")
                        instance['duration']=duration;
                        instance['participants']=participants;
                        instance['topic']=topic;
                        callinstances[contacttype].append(instance);
                    thekeys=callinstances.keys()
                    print("Dump the comms of each type")
                    with open("outputcsv_"+str(targetconv)+".csv",'w',newline='') as file:
                        writer=csv.writer(file);
                        field=["Contacttype","Topic","datetime (gmt)","datetime (London)","duration (s)","displayName","participants","threadid"]
                        writer.writerow(field);
                        print(thekeys);
                        for k in thekeys:
                            print("Key "+k);
                            print(len(callinstances[k]));
                            #sorted_callinstances=dict(sorted(callinstances[k].threadid(),reverse=False))
                            for j in callinstances[k]:
                                print(k);
                                print(j['originalarrivaltime']);
                                print(j['displayName']);
                                print(j['duration']);
                                threadId=str(j['threadid']);
                                #print([k+' '+j['originalarrivaltime']+' '+j['displayName']+' '+j['threadid']])
                                writer.writerow([k,j['topic'].replace('"',''),j['originalarrivaltime'],j['adjustedtime'],j['duration'],j['displayName'],j['participants'],threadId])


        except:
            print("error follows")
            print(e)
