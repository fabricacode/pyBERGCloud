import webapp2
import datetime
import logging

from google.appengine.ext import ndb #use the data modeling API, import the google.appengine.ext.ndb module:

#~ Events Listener----------------------------------------------------------------- 
#~ dependent on google app engine ndb database - write every event received on a database entry
def allEventsKey():
    """Constructs a Datastore key, parent of all events entities."""
    return ndb.Key('AllEvents', 'allEvents')

class Event(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    address = ndb.StringProperty(indexed=False)
    payload = ndb.StringProperty(indexed=False)
    time = ndb.DateTimeProperty(indexed=True)

class EventReceiver(webapp2.RequestHandler): 
    def post(self): 
        e = Event(parent = allEventsKey(), 
            name = self.request.get('name'), 
            payload = self.request.get('payload'), 
            address = self.request.get('address'), 
            time = datetime.datetime.now()
        )
        e.put()        
        self.deleteOldEntities()          
    def deleteOldEntities(self, secsFromNow = 100):
        eq = Event.query(ancestor = allEventsKey()) 
        for e in eq: 
            if (datetime.datetime.now() - e.time).total_seconds() > secsFromNow: 
                e.key.delete()
                
    # function below uses datastore indexes. May take sometime to be updated on the GAE server
    def deleteOverMaxEvents(self, maxEntities = 30):
        eq = Event.query(ancestor = allEventsKey()) 
        #~ nEntities = eq.count()
        nEntities = 60
        logging.debug("n entities: "+str(nEntities))
        logging.debug("n max entities: "+str(maxEntities))
        if (nEntities > maxEntities): 
            nTrashEntities = nEntities - maxEntities
            logging.debug("n trash entities: "+str(nTrashEntities))
            #list from the older to the newer one. Pick just the ones 
            try: 
                eq = Event.query(ancestor = allEventsKey()).order(Event.time).fetch(nTrashEntities)
                logging.debug("n trash entities confirmed: "+str(eq.count()))
                for e in eq:
                    e.key.delete()
            except: 
                logging.debug('Index not built yet. Cannot list received events. Wait some time')
#~ -------------------------------------------------------------------------- 
