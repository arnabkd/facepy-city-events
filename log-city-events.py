from facepy import GraphAPI
import os, json, sys

new_events = 0

def add_events_to_dict(events, event_IDs, city_name):
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
      print "Added event:%s for city %s"%(eid, city_name)
      new_events += 1


def add_city_events(city_name):
  events = {}
  
  #Open from file
  if os.path.isfile("data/"+city_name+ ".json"):
    fo = open("data/"+ city_name +".json", "r")
    events = json.loads(fo.read())
    #print "read from", fo.name
    #print len(events), "events read"
    fo.close() 
  
  #Get all events in a city
  a = graph.get('search?fields=location&q=\"'+ city_name + '\"&type=event&since=0')
  event_IDs = [event['id'] for event in a['data']]      
  add_events_to_dict(events, event_IDs, city_name)


  #Add to file
  fo = open("data/"+ city_name +".json", "w")
  json.dump(events, fo)
  #print "saving to", fo.name
  fo.close()

 
#Access token
try:
  oath_file = open(sys.argv[1],'r')
  access_token = oath_file.read()
  oath_file.close()
  
  graph = GraphAPI(access_token)

  #Create a data directory if one does not exist  
  targetdir = "data/"
  if not os.path.exists(targetdir):
    os.mkdir(targetdir)

  #List of cities to query events from
  cities = ["Chicago", "London", "Montreal", "New York", "Ottawa", "Toronto", "Washington", "Oslo"]

  for city in cities:
    add_city_events(city)
  print "No new events to be added" if new_events == 0 else "A total of %s events added"%(new_events)
  
except:
  print "No valid access token found"
  print "Usage: python log-city-events.py access_token.txt"


    
  