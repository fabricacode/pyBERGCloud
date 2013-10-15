import webapp2
import datetime

from google.appengine.ext import ndb #use the data modeling API, import the google.appengine.ext.ndb module:

#~ Events Listener----------------------------------------------------------------- 
#~ dependent on google app engine ndb database - write every event received on a database entry
def allEventsKey():
    """Constructs a Datastore key, parent of all events entities."""
    return ndb.Key('AllEvents', 'allEvents')

class Event(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    payload = ndb.StringProperty()
    time = ndb.DateTimeProperty()

class EventReceiver(webapp2.RequestHandler): 
    def post(self): 
        e = Event(parent = allEventsKey(), 
            name = self.request.get('name'), 
            payload = self.request.get('payload'), 
            address = self.request.get('address'), 
            time = datetime.datetime.now()
        )
        e.put()
        #~ self.deleteOverMaxEvents()
        
        self.deleteOldEntities()  
        #~ self.deleteOldEntities(500) #pass the "seconds" parameter here for changing the min time interval for an entity to be considered old
        
    def deleteOldEntities(self, secsFromNow = 100):
        eq = Event.query(ancestor = allEventsKey()) 
        for e in eq: 
            if (datetime.datetime.now() - e.time).total_seconds() > secsFromNow: 
                e.key.delete()
                
    def deleteOverMaxEvents(self, maxEntities = 30):
        eq = Event.query(ancestor = allEventsKey()) 
        nEntities = eq.count()
        if (nEntities > maxEntities): 
            nTrashEntities = nEntities - maxEntities
            #list from the older to the newer one. Pick just the ones 
            eq = Event.query(ancestor = allEventsKey()).order(Event.time).fetch(nTrashEntities)
            for e in eq:
                e.key.delete()
        
 
#~ -------------------------------------------------------------------------- 
