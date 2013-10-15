
import webapp2

import bergcloud.commandsender
import bergcloud.eventreceivergae

import logging

import base64
import datetime

COMMAND_FORM_TEMPLATE = """\
<html>
 <body>
 
    
    <form action="/APIToken" method="post">
        BERG Cloud API token:
      <input value="text" name="api_token">
      <input type="submit">
    </form>
    <form action="/devboardAddress" method="post">
        BERG Cloud address of product:
      <input value="text" name="devboard_address">
      <input type="submit">
    </form>
    
    <form action="/sendCommand" method="post">
        Name: <input type="text" name="command_name">
        Payload: <input type="text" name="command_payload">
        <input type="submit">
    </form>    

"""

#~ Commands Manager----------------------------------------------------------------
bg_cs = bergcloud.commandsender.CommandSender()

#~ Events Manager-------------------------------------------------------------------

#~ create a class that inherit from bergcloud.eventreceivergae.EventReceiver and override its post method for managing
#~ events with methods defined in its parent class

class MyEventReceiver(bergcloud.eventreceivergae.EventReceiver):
    #override parent class method and 
    def post(self): 
        e = bergcloud.eventreceivergae.Event(parent = bergcloud.eventreceivergae.allEventsKey(), 
            name = self.request.get('name'), 
            payload = self.request.get('payload'), 
            address = self.request.get('address'), 
            time = datetime.datetime.now()
        )
        e.put()
        #and uses a method from the parent class
        super(MyEventReceiver, self).deleteOldEntities()
        


class MainPage(webapp2.RequestHandler): #MainPage inherit from webapp2.RequestHandler
    
    def get(self):
        self.response.write("Hi BERGCloud!")
        #~ Set device and api token and send command
        self.response.write('<hr><h1>Events</h1>')
        self.response.write('<pre>Set device and api token and send command</pre>')
        self.response.write(COMMAND_FORM_TEMPLATE) 
        if bg_cs.apiToken is not None: 
            self.response.write('Current API token: ')    
            self.response.write(bg_cs.apiToken+'<br>')    
        if bg_cs.devBoardAddress is not None: 
            self.response.write('Current devboard address: ')        
            self.response.write(bg_cs.devBoardAddress+'<br>') 
        #~ List events received to the current Base URL
        self.response.write('<hr><h1>Events</h1>')
        self.response.write('<pre>List events received to the current Base URL</pre>')
        self.response.write('<h3>time event received - device name - device address - payload</h3>')
        
        
        # PRINT NOT ORDERED EVENT LIST 
        
        bcEvents = bergcloud.eventreceivergae.Event.query(ancestor = bergcloud.eventreceivergae.allEventsKey())
        for bcEvent in bcEvents: 
                self.response.write(
                    unicode(bcEvent.time).encode('ascii', 'xmlcharrefreplace') + ' - ' 
                    + bcEvent.name + ' - ' + bcEvent.address + ' - ' 
                    + bcEvent.payload.encode('ascii', 'ignore')+'<br>'
                )
        
        # PRINT ORDERED EVENT LIST - uses datastore indexes. May take sometime to be updated on the GAE server
        
        #~ try: 
            #~ bcEvents = bergcloud.eventreceivergae.Event.query(ancestor = bergcloud.eventreceivergae.allEventsKey()).order(-bergcloud.eventreceivergae.Event.time).fetch(10)
            #~ for bcEvent in bcEvents: 
                #~ self.response.write(
                    #~ unicode(bcEvent.time).encode('ascii', 'xmlcharrefreplace') + ' - ' 
                    #~ + bcEvent.name + ' - ' + bcEvent.address + ' - ' 
                    #~ + bcEvent.payload.encode('ascii', 'ignore')+'<br>'
                #~ )
        #~ except :
            #~ logging.debug('Index not built yet. Cannot list received events. Wait some time')
                    


class SetAPIToken(webapp2.RequestHandler):
    def post(self): 
        at = self.request.get('api_token')
        global bg_cs
        bg_cs.apiToken = at
        self.redirect('/')
        
class SetDevBoardAddress(webapp2.RequestHandler):
    
    def post(self): 
        da = self.request.get('devboard_address')
        global bg_cs
        bg_cs.devBoardAddress = da
        self.redirect('/')

class SendCommand(webapp2.RequestHandler): 
    def post(self): 
        global bg_cs
        bg_cs.sendCommand(commandName = self.request.get('command_name'), commandPayload = self.request.get('command_payload')) 
        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/APIToken', SetAPIToken),
    ('/devboardAddress', SetDevBoardAddress), 
    ('/sendCommand', SendCommand),
    ('/device-event/.*', MyEventReceiver), #receives every event directed to this Base URL, no matter the name. 
], debug=True)

