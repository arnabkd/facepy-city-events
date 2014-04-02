from facepy import GraphAPI

access_token = "CAACEdEose0cBAKvIVo9zaVZA6qAJsn8TdYEbAQP7peWkL3vXJibMtPIbMdt3FKf19ubiN7IaLAc8f3DK1zmL9cuu7MNKy5PNSI9GrNP4d9XgswUV5UlULaLNrESZAaL82Ccbf2WmB7u8bC2GOheHZBspJSwSRCGj9CoIwWIyB8PdYfHtKcvYn9zzACjqdLTMsiOpdatTAZDZD"

graph = GraphAPI(access_token)

# Get my latest posts 
graph.get('me/posts')

# Post a photo of a parrot 
#graph.post( path = 'me/photos', source = open('parrot.jpg') )

# Make a FQL query 
graph.fql('SELECT name FROM user WHERE uid = me()')

# Make a FQL multiquery 
graph.fql({ 'rsvp_status': 'SELECT uid, rsvp_status FROM event_member WHERE eid=12345678', 'details': 'SELECT name, url, pic FROM profile WHERE id IN (SELECT uid FROM #rsvp_status)' }
