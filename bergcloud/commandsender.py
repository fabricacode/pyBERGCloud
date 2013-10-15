#~ - devBoardAddress is here http://remote.bergcloud.com/developers/devkit_devices under the name of BERG Cloud address
#~ - at the correspondent product link there's the API token, under the name of BERG Cloud API token


import webapp2
import base64
import urllib 
import urllib2
import datetime

import logging


#~ Command-------------------------------------------------------------------------- 
class Command: 
    def __init__(self, name = None, payload = None): 
        self.name = name
        self.payload = payload

class CommandSender: 
    def __init__(self, apiToken = None, devBoardAddress = None): 
        self.apiToken = apiToken 
        self.devBoardAddress = devBoardAddress

    def sendCommand(self, command = None, commandName = None, commandPayload = None): 
        if commandName is not None and commandPayload is not None: 
            self.payload = commandPayload
            self.name = commandName
        elif command is not None:  
            self.payload = command.payload
            self.name = command.name
        else: 
            logging.debug("Command data not provided") 
            return
            
        self.form_fields = {
            "address": self.devBoardAddress,
            "payload": base64.urlsafe_b64encode(self.payload)#encode string as Base64
        }
        self.form_data = urllib.urlencode(self.form_fields)
        self.commandUrl = 'http://api.bergcloud.com/v1/products/'+self.apiToken+'/'+self.name
        # - send POST to bergcloud
        self.req = urllib2.Request(self.commandUrl, self.form_data)
        try: 
            self.resp = urllib2.urlopen(self.req)
        except:
            logging.debug("Destination URL for posting Event not found. Check if there's any event set on BERGCloud with the name: "+str(self.name))
            
            
      

