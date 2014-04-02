#Import Graph API
from facepy import GraphAPI
access_token = ""

graph = GraphAPI(access_token)

# Get my latest posts 
latest_posts = graph.get('me/posts')
#print latest_posts

events_fql = """select 
    eid, 
    name, 
    description, 
    location, 
    all_members_count, 
    attending_count, 
    unsure_count, 
    not_replied_count, 
    declined_count, 
    start_time, 
    end_time,
    venue 
from 
    event 
where     
    eid in 
    (
        select 
            eid, 
            start_time 
        from 
            event_member 
        where 
            uid in 
            (
                select 
                    page_id 
                from 
                    place 
                where 
                    distance(latitude, longitude, "59.9500", "10.7500") < 50000
            ) and 
            start_time > "2012-01-01"
    ) and 
    end_time < "2013-01-01" and 
    end_time <> 'null' """
    
events =  graph.fql(events_fql)
print len(events)
print type(events)

event_search = """search?fields=location&q="Oslo, Norway"&type=event&since=1356994800"""
sample_event = graph.get(event_search)['data'][150]

sample_event_fql = """SELECT eid, name, attending_count, unsure_count, declined_count, not_replied_count, location, start_time, end_time from event where eid =  """ + sample_event['id']
sample_event_info = graph.fql(sample_event_fql)
print sample_event_info

#Setup access tokens

#Get graph results

#Process results

#Output
