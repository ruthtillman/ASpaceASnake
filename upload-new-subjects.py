# Import the various client libraries needed to make this work. And some friends for now.
import os, requests, glob, json, logging, csv, configparser, datetime

# import and set up logging BEFORE touching the client or anything
import asnake.logging as logging

logname = 'logs/new_subject_upload_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'

logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger("upload-new-subjects")

# Bring in the client to work at a very basic level.
from asnake.client import ASnakeClient

# Create and authorize a client to ASnake!
client = ASnakeClient()
client.authorize()

def upload_json_as_new_subjects(file_dir):
    logger.info("upload_start", batch_name=batch)
    os.chdir(file_dir)
    subjects = glob.glob("*.json")
    for file in subjects:
        subject = json.load(open(file))
        response = client.post('subjects', json=subject).json()
        response['title'] = subject['title']
        logger.info("upload_subject", response=response)
    os.chdir('..') # if taking full filepaths be sure to grab a cwd at the start so you can go back to it
    logfile.close()

# This can be made into an input at some point but right now I'm managing manually.

subject_location = 'reserve-batch'

# Call the main function

batch = input("Name your upload batch: ")

upload_json_as_new_subjects(subject_location)
