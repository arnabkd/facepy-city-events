from facepy import GraphAPI
import os, json, sys

new_events = 0

def add_friends_events(events, event_IDs):
    friends_events_fql = """SELECT eid FROM event 
    WHERE eid IN (
           SELECT eid FROM event_member 
           WHERE (uid IN (SELECT uid2 FROM friend WHERE uid1 = me())  OR uid = me())
       )
    """
    results = graph.fql(friends_events_fql)
    print results


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
      #new_events += 1

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
  try:
    a = graph.get('search?fields=location&q=\"'+ city_name + '\"&type=event&since=0')
    event_IDs = [event['id'] for event in a['data']]   
    add_events_to_dict(events, event_IDs, city_name)
  except:
    print "Something went wrong while getting graph data for ", city_name
    print sys.exc_info()[0]

  #Add to file
  fo = open("data/"+ city_name +".json", "w")
  #json.dump(events, fo)
  updated_events = json.dumps(events, sort_keys=True, indent=4, separators=(',', ': '))
  fo.write(updated_events)
  print "saving to", fo.name
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
    try:
      add_city_events(city)
    except:
      print sys.exc_info()[0]
  
  print "No new events to be added" if new_events < 1 else "A total of %s events added"%(new_events)
  
except:
  print sys.exc_info()[0]
  print "No valid access token found"
  print "Usage: python log-city-events.py access_token.txt"


    
  