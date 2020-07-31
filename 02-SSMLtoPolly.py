"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import simplejson as json 

filename='creds.json'
file = open(filename,'rb')
creds=json.load(file)
file.close() 
completePath=os.path.abspath(creds['path']) 
fullPath=completePath




polly = Session(aws_access_key_id=creds['aws_access_key_id'],aws_secret_access_key=creds['aws_secret_access_key'],region_name=creds['region_name']).client('polly')
print("CONNETED") 
text="""
<speak>

1. Select a row <mark name='mark1'/>for your choice (in this example either U, or D). <mark name='mark1'/> Once you have selected a row, it will be outlined, and the label <break strength="weak"/>My Choice<break strength="weak"/> will be added. <mark name='mark1'/> My choice will also be updated on the period summary.

</speak>
"""

filename=fullPath+"generatedFiles/01-ssml.txt"
file = open(filename,'r')
text=file.read()
file.close() 

print("About to send a document with the following length to AWS:") 
print(len(text))
input()  
input()  
try:
    response = polly.start_speech_synthesis_task(OutputS3BucketName="instructions-text-to-speech",Engine="neural",Text=text,OutputFormat="mp3",VoiceId="Matthew",TextType="ssml")
    jsonData = polly.start_speech_synthesis_task(OutputS3BucketName="instructions-text-to-speech",Engine="neural",Text=text,SpeechMarkTypes=['ssml','word','sentence'],OutputFormat="json",VoiceId="Matthew",TextType="ssml")
except (BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)
print(jsonData) 
# import pickle
# filename='jsonData.pickle'
# file = open(filename,'wb')
# pickle.dump(jsonData["AudioStream"].read(),file)
# file.close() 
# # print(response) 
# # print(json.loads(jsonData["AudioStream"].read().decode('utf-8')))
# # # this=json.load(jsonData["AudioStream"])
# # filename='out.json'
# # file = open(filename,'wb')
# # file.write(jsonData["AudioStream"])
# # file.close() 

# print("CONNETED") 

# if "AudioStream" in jsonData:
#     with closing(jsonData["AudioStream"]) as stream:
#         output = "test.json"
#         try:
#             with open(output,"wb") as file:
#                 file.write(stream.read())
#         except IOError as error:
#             print(error)
#             sys.exit(-1)
# else:
#     # The response didn't contain audio data, exit gracefully
#     print("Could not stream audio")
#     sys.exit(-1)



# if "AudioStream" in response:
#     with closing(response["AudioStream"]) as stream:
#         output = "speech.mp3"
#         try:
#             with open(output, "wb") as file:
#                 file.write(stream.read())
#         except IOError as error:
#             print(error)
#             sys.exit(-1)
# else:
#     # The response didn't contain audio data, exit gracefully
#     print("Could not stream audio")
#     sys.exit(-1)

