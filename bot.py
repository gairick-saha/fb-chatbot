from fbchat import Client, log
from fbchat.models import *

import credentials
import apiai, codecs, json


class Jarvis(Client) :
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "ENTER_YOUR_API_KEY"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de' #defualt : english
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def onMessage( self, author_id = None, message_object = None, thread_id = None, thread_type = ThreadType.USER, **kwargs) : 
        self.markAsRead(author_id)

        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))
        self.apiaiCon()
        msgText = message_object.text

        self.request.query = msgText

        response = self.request.getresponse()

        obj = json.load(response)
        
        reply = obj['result']['fulfillment']['speech']

        if author_id != self.uid : 
            self.send(Message(text = reply), thread_id = thread_id, thread_type = thread_type)


        self.markAsDelivered(author_id, thread_id)

client = Jarvis(credentials.username, credentials.password)
client.listen()
