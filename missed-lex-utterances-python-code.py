#importing all lib and interdependencies for solution

from itertools import count
import json
from datetime import datetime
import sys
from pip._internal import main
import csv
import pandas as pd


#this is to make sure that we always get latest boto3 library and upgraded version
main(['install', '-I', '-q', 'boto3', '--target', '/tmp/', '--no-cache-dir','--upgrade', '--disable-pip-version-check', ])
sys.path.insert(0,'/tmp/')


import boto3
#using lex models boto3 lib and ClientError lib
from botocore.exceptions import ClientError 
client = boto3.client('lex-models')

#Enter your Bot name?
botName="BotName"

# function that returns list of utterances of that bot
def get_utterances_view(botName):
  
	client = boto3.client('lex-models')
	return utterances_all
	
#API only allows to fetch up to 1000 utterances at once. 
    
MaxResults = 1000
    
utterances_all = ''
    

#get list of Lex Missed Utterances in the specific Bot and the version, please note version must be updated when changed in Lex Bot
response = client.get_utterances_view(
    botName='BotName',
    botVersions=[
        '25',
    ],
    statusType='Missed'
)
Utterances=response['utterances']
utterances_all = [*utterances_all,*Utterances]
    
def lambda_handler(event, context):
	
#Amazon LexBotName and utterance view from global directory
	global botName
	botName= 'BotName'
	global get_utterances_view

#Headers for our CSV-file
headers="Words,Count"+"\r\n"
	
#csv-file name of the missed utterances
csv_file='/tmp/csv_files_name.csv'
	
#S3 bucket name
s3_bucket='S3Bucket Name'
	
#Using S3 boto3 client
s3 = boto3.client('s3')
data_file = open(csv_file, 'w+')
data_file.write(headers)

#Using lex boto3 client
client = boto3.client('lex-models') 
    
#get list of Missed Utterances
utterances=get_utterances_view(botName)
	
#getting the lex Directory from the List, make sure to have correct version of bot
for utterances in utterances:
		Utterance=utterances['utterances']
		UtteranceString_1=Utterance[0:200]
#getting missed utternaces from the lex bot	
		response = client.get_utterances_view(
    botName='BotName',
    botVersions=[
        '25',
    ],
    statusType='Missed'
    
)

print(Utterance) #prints the list of dictonaries of missed utterances


#Extracting two directories for two most used Keys and values Utterances and their Counts from the Lists
Utterance_new =[i["utteranceString"] for i in Utterance]
Count=[i["count"] for i in Utterance]
#print(Utterances_new)
#print(Count)

#Combining two directories together to get Key of "utteranceString" and the respective value of "Count"
combinedDict = dict(zip(Utterance_new,Count))
#printing the output
print(combinedDict)

#Writing the combined dict to coloumns and assigning each coloumn to respective Key and Value in Excel
with open(csv_file, 'w') as output:
    writer = csv.writer(output)
    for key, value in combinedDict.items():
        writer.writerow([key, value])
        
#Importing python package for pandas, which is a data structure like sql.
#The process below reads existing data file of CSV, without headers
#Then adds headers in the data frame
#Converts the Data Frame to CSV
#Then uploads to S3 bucket.

import pandas as pd

# read contents of csv file
file = pd.read_csv("/tmp/csv_files_name.csv")
print("\nOriginal file:")
print(file)

# adding header
headerList = ['Words', 'Count']

# converting data frame to csv
file.to_csv(csv_file, header=headerList, index=False)

# display modified csv file
file2 = pd.read_csv(csv_file)
print('\nModified file:')
print(file2)


	#upload CSV file to S3
s3.upload_file(csv_file, s3_bucket , csv_file)
