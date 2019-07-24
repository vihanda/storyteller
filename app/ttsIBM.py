# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:29:50 2019

@author: shiagraw
"""

#import requests
#url = 'https://gateway-lon.watsonplatform.net/text-to-speech/api/v1/synthesize'
#payload = open("request.json")
#headers = {'content-type': 'application/json', 'Accept': 'audio/wav'}
#auth = {'apikey':'lrbPIbK-pnw6YCRylPSAPQLsQIK3IQZIeF23ESaKq3bD'}
#r = requests.post(auth, url, data=payload, headers=headers, output="narrativePython.wav")
    
# coding=utf-8
from __future__ import print_function
import json
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback

def ttsIBM():
    # If service instance provides API key authentication
    service = TextToSpeechV1(
        ## url is optional, and defaults to the URL below. Use the correct URL for your region.
        url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
        iam_apikey='lrbPIbK-pnw6YCRylPSAPQLsQIK3IQZIeF23ESaKq3bD')

    with open('narrativeIBMpython.wav',
              'wb') as audio_file:
        response = service.synthesize(
            'We know that running your own business is rewarding. But sometimes, the paperwork can be a drag! Meet Mathew. Matthew is very busy running his own business. Tax time always overwhelms him with paperwork. Paperwork from vendors, the IRS and customers to name a few. So Matthew searches online for a solution and discovers Acme Tax. Acme Tax offers solutions for managing payroll, monthly financial statements and IRS statement reviews. Now Matthew can focus less on paperwork and more on growing his business!', accept='audio/wav',
            voice="en-US_AllisonVoice").get_result()
        audio_file.write(response.content)

