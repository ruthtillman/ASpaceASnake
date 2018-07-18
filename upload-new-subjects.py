# Import the various client libraries needed to make this work. And some friends for now.

import os, requests, glob, json, logging, csv, configparser, datetime
# Bring in the client to work at a very basic level.
from asnake.client import ASnakeClient

# Create and authorize a client to ASnake!
client = ASnakeClient()
client.authorize()

def upload_json_as_new_subjects(file_dir):
    os.chdir(file_dir)
    subjects = glob.glob("*.json")
    init_job = name_log()
    results = []
    for file in subjects:
        subject = json.load(open(file))
        response = client.post('subjects', json=subject).json()
        response['title'] = subject['title']
        results.append(response)
    os.chdir('..')
    create_log(init_job, results)

# I swear too much of my time was spent on logging concerns. However part of that is that I just need to be sure I end up with a good log for the next phase of my project.

# This names the log based on when the script starts running and gets a start time.
# It returns them as a tuple because that's how it is. So it's called to the variable init_job above, then passed to the creation and the values can be accessed that way.

def name_log():
    logName = datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + "_subject_upload_log.json"
    jobStart = datetime.datetime.now().isoformat()
    return (logName, jobStart)

# Makes use of init_log and the dictionary of responses received. Note that this dictionary includes responses which have had titles added to them. That's mostly for my own use.

def create_log(init_job, results):
    logName = 'logs/' + init_job[0]
    log = json.loads('{"jobType" : "upload_subjects"}')
    log['user'] = 'rkt6'
    log['dateTimeStart'] = init_job[1]
    log['dateTimeEnd'] = datetime.datetime.now().isoformat()
    log['responses'] = results
    with open(logName, "w") as logging:
        json.dump(log, logging, indent=4)

# This can be made into an input at some point but right now we'll just set to the files directory

subject_location = 'files'

# Call the main function

upload_json_as_new_subjects(subject_location)
