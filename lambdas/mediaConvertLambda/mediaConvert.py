#Create a MediaConvert job by reading the metadata.xml file provided by SnapStream.
#The xml file and the file name provide Network, Date, StartTime details.
#the settings.json file stored in the lambda provide all the other details needed to run MediaConvert.
#Note: the timedelta(hours = -5) in the local_time function needs to be updated for daylight savings.
import json
import boto3
import csv
import urllib
import shlex
import datetime as dt
from io import StringIO
import time

mediaconvert_client = boto3.client('mediaconvert', endpoint_url='https://excqsnx7a.mediaconvert.us-east-1.amazonaws.com')
s3 = boto3.client('s3')
settings = {} #starts with an empty dict, will be filled with all the settings from the metadata.xml file.

def network_finder(station):
    if station.find('WKRN') != -1:
        network = 'ABC'
    elif station.find('FNCHD') != -1:
        network = 'FNC'
    elif station.find('WTVFDT') != -1:
        network = 'CBS'
    elif station.find('WSMVDT') != -1:
        network = 'NBC'
    elif station.find('CNNHD') != -1:
        network = 'CNN'
    else:
        network = 'ERROR'
    return(network)
    
def local_time(timeIn):
    converted = dt.datetime.strptime(timeIn[:-3],'%Y-%m-%dT%H:%M:%S.%f') #notice I trimmed out the tail of the RCF3339 data.
    new  = converted + dt.timedelta(hours = -5) #this converts to Central time, needs to be updated manually for daylight savings.
    new = dt.datetime.time(new)
    ms = new.strftime('%f')[:2]
    newStr = new.strftime('%H:%M:%S:') + ms
    return(newStr)

def burnin_date(timeIn):
    converted = dt.datetime.strptime(timeIn[:-3],'%Y-%m-%dT%H:%M:%S.%f')
    new  = converted + dt.timedelta(hours = -5)
    new = new.strftime('%m/%d/%Y')# the date for burnin: MM/DD/YYYY
    return(new)

def filename_date(timeIn):
    converted = dt.datetime.strptime(timeIn[:-3],'%Y-%m-%dT%H:%M:%S.%f')
    new = converted + dt.timedelta(hours = -5)
    new = new.strftime('%Y%m%d') # the date formated for finding the file
    return(new)


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],encoding='utf-8')
    filename =  event['Records'][0]['s3']['object']['key']   
    response = s3.get_object(Bucket=bucket, Key=key)
    text = response['Body'].read().decode('utf-8')    
    text = shlex.split(text)
    
    with open("media-convert-settings.json", "r") as jsonfile:
        job_object = json.load(jsonfile)
        
    for property in text:
        try:
            newValue = property.split('=')
            settings.update({str(newValue[0]) : str(newValue[1])})
        except:
            pass
    stationName = settings['StationName']
    network = network_finder(settings['StationCallsign'])
    recordtime = str(local_time(settings['ActualStartTime']))
    burndate = burnin_date(settings['ActualStartTime'])
    filenameDate = filename_date(settings['ActualStartTime'])
    videoInput = filename.replace('.xml','.ts')
    print('Station Name: '+ stationName)
    print('Network: '+ network)
    print('Timecode Burnin Start: '+ recordtime)
    print('Timecode Burnin Date: '+ burndate)
    print('Video Input: '+ videoInput)
    
    job_object['Settings']['OutputGroups'][0]['Outputs'][0]['VideoDescription']['VideoPreprocessors']['TimecodeBurnin']['Prefix'] = network+'    '+burndate + '    '

    job_object['Settings']['Inputs'][0]['FileInput'] = 's3://vu-tvnews-'+network.lower()+'/'+videoInput

    job_object['Settings']['TimecodeConfig']['Start'] = recordtime
    time.sleep(30)
    mediaconvert_client.create_job(**job_object)
    #If you pulled this from a public repo, you will need to go into the TimeStampTemplate.json file and update Roles and Queue with your AWS account number.