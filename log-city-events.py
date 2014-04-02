from facepy import GraphAPI
import os, json

#Access token
access_token = "CAACEdEose0cBAOfZB9Q0cqZAKmB5ZAxIve6ZBuPZCnW5389PN4k6plEtJWrjyI2rkIGClaXkgTdcGRxKQAbIlnWLhhwhM3s5EXvwQjbFpRWJOuxtoqZCQToBQNFhyDNS18xMvUq00NV6FTrlfOQHZCZCVO5bZAZBAzF9Gh496gAex5SyOXicmtcnO15syRQ96nZA2U4KIFzBR3WpwZDZD"
graph = GraphAPI(access_token)


targetdir = "../data/"
if not os.path.exists(targetdir):
  os.mkdir(targetdir)
  
cities = ["Chicago", "London", "Montreal", "New York", "Ottawa", "Toronto", "Washington"]
city_event_logfiles = [targetdir + city + "_events.json" for city in cities]

#print city_event_logfiles



"""
eid = event_IDs[0]

#Get event info
info_fql = "SELECT eid, name, attending_count, unsure_count, declined_count, not_replied_count, location, venue, start_time, end_time from event where eid =  " + eid
event_info = graph.fql(info_fql)


events = {}
events[eid] = event_info['data'][0] 


fo = open("sample-events.json", "w")
json.dump(events, fo)
fo.close()

fo = open("sample-events.json", "r")
events2 = json.loads(fo.read())
fo.close()

print events
print "------------------------"
print events2

print "Are these equal?"
print "yes" if events == events2 else "no"
"""

def add_events_to_dict(event,event_IDs):
  for eid in event_IDs:
    if not events.has_key(eid):
      info_fql = """SELECT eid, name, attending_count, unsure_count, declined_count, not_replied_count, location, venue, start_time, end_time from event where eid =  """ + eid
      event_info = graph.fql(info_fql)
      event = event_info['data'][0]
      
      venue = event['venue']
      if 'dict' in str(type(venue)):
        if (event['venue'].has_key('latitude')):
          event['latitude'] = float(str(event['venue']['latitude']))
        if (event['venue'].has_key('longitude')):
          event['longitude'] = float(str(event['venue']['longitude']))
        del event['venue']
      
      events[eid] = event


#Get all events in a city
a = graph.get('search?fields=location&q=\"'+ cities[6] + 'Washington, DC\"&type=event&since=1388534400')
event_IDs = [event['id'] for event in a['data']]      
events = {}
add_events_to_dict(events, event_IDs)


#Add to file
fo = open("sample-events.json", "w")
json.dump(events, fo)
fo.close()

#Open from file
fo = open("sample-events.json", "r")
events2 = json.loads(fo.read())
fo.close()

print "Are these equal?"
print "yes" if events == events2 else "no"


