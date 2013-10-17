#~ pyBERGCloud - a python library for interfacing with the BERGCloud platform
#~ 
#~ Copyright (c) 2013 Amico Leonardo - leonardo.amico@gmail.com
#~ 
#~ 
#~ Permission is hereby granted, free of charge, to any person obtaining a copy
#~ of this software and associated documentation files (the "Software"), to deal
#~ in the Software without restriction, including without limitation the rights
#~ to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#~ copies of the Software, and to permit persons to whom the Software is
#~ furnished to do so, subject to the following conditions:
#~ 
#~ The above copyright notice and this permission notice shall be included in
#~ all copies or substantial portions of the Software.
#~ 
#~ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#~ IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#~ FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#~ AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#~ LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#~ OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#~ THE SOFTWARE.


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
        nEntities = eq.count()
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
