# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:00:07 2019

@author: shiagraw
"""
import os
import requests
import time
from xml.etree import ElementTree

#text = "Once upon a time, there was a beautiful girl named Cinderella. She lived with her wicked stepmother and two stepsisters. They treated Cinderella very badly. One day, they were invited for a grand ball in the king’s palace. But Cinderella’s stepmother would not let her go. Cinderella was made to sew new party gowns for her stepmother and stepsisters, and curl their hair. They then went to the ball, leaving Cinderella alone at home."
text = "We know that running your own business is rewarding. But sometimes, the paperwork can be a drag! Meet Mathew. Matthew is very busy running his own business. Tax time always overwhelms him with paperwork. Paperwork from vendors, the IRS and customers to name a few. So Matthew searches online for a solution and discovers Acme Tax. Acme Tax offers solutions for managing payroll, monthly financial statements and IRS statement reviews. Now Matthew can focus less on paperwork and more on growing his business!"

'''
If you prefer, you can hardcode your subscription key as a string and remove
the provided conditional statement. However, we do recommend using environment
variables to secure your subscription keys. The environment variable is
set to SPEECH_SERVICE_KEY in our sample.
For example:
subscription_key = "Your-Key-Goes-Here"
'''
subscription_key = "75712fd9c3e64a0c8456c674b5441b64"

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.tts = text
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://eastus2.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://eastus2.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': '2019Hackathon'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', 'en-US-BenjaminRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

if __name__ == "__main__":
    app = TextToSpeech(subscription_key)
    app.get_token()
    app.save_audio()