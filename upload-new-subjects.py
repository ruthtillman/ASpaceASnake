#!/usr/bin/env python
import glob, json, datetime

# Setting up the log
import asnake.logging as logging

logname = 'logs/new_subject_upload_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'

logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger("upload-new-subjects")

# Bring in the client to work at a very basic level.
from asnake.client import ASnakeClient

# Create and authorize the client
client = ASnakeClient()
client.authorize()

def upload_json_as_new_subjects(file_dir,batch):
    '''Actually run the upload. Simply sets up the log, gathers the JSON, and then uploads each. This is a simple post because it's creating new ones and doesn't need any kind of number.'''
    logger.info("upload_start", batch_name=batch)
    subjects = glob.glob(file_dir + "/" + "*.json") # globs all the .json objects in the directory where the files are located.
    for file in subjects:
        subject = json.load(open(file))
        response = client.post('subjects', json=subject).json()
        response['title'] = subject['title']
        logger.info("upload_subject", response=response)
    logfile.close()

batch = input("Name your upload batch: ")
subject_location = input("The full or relative path to your batch: ")

upload_json_as_new_subjects(subject_location,batch)
