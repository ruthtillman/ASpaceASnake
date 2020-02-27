#!/usr/bin/env python
import json, csv, datetime
import asnake.logging as logging

# set up logging. mutter profanity.

logname = 'logs/deleting_subjects_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'

logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger('delete_subjects')

# add ASnake Client
from asnake.client import ASnakeClient
# validate ASnake client
client = ASnakeClient()
client.authorize()

# expects a CSV file with column subject_id of subjects to be deleted

def delete_subjects(data):
    '''This opens the CSV file, reads the subject_id column, deletes subject, and logs response. Records target ID in case it's not found or other error.'''
    with open(data, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            sub_id = str(row['subject_id']) #typing just in case
            response = client.delete('subjects/' + sub_id).json()
            logger.info('delete', target=sub_id, action='delete_subject', response=response)
    logfile.close()

data = input("What is the name of or path to the CSV? ")

delete_subjects(data)
