import re, json, csv, requests, glob, datetime
import asnake.logging as logging

# fuk u logging

logname = 'logs/subject_resource_processing_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'

logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger("add-subjects-log")

# add ASnake Client
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# validate ASnake client
# open CSV and get two values. value 1 is the resource_id, value 2 should be split on | and put into an array. is there a way to put it into an array and attach the `/subjects/` at the same time?
# for resource_id, download the JSON object.

# This function downloads the record (note, it must take in both fields of the CSV row), holds onto it, and pulls out the subject for testing and one of two future functions ... WRITE OUT THE ORIGINAL TO ANOTHER DIRECTORY AS A BACKUP
def quick_backup(resource_id,resource):
    original = "backups/original-" + resource_id + ".json"
    with open(original, "w") as backup:
        json.dump(resource, backup, indent=4)

# This function is what we do if the subject array is empty
def no_original_subjects(resource,new_subjects):
    subjects = []
    for subject in new_subjects:
        subjects.append({"ref": subject})
    resource["subjects"] = subjects
    logger.info("process_resource", action="new_subjects", data={"resource_uri": resource["uri"], "subjects" : subjects})
    return resource

# This function is what we do if the subject array is not empty

def adding_subjects(resource,new_subjects,original_subjects):
    for subject in new_subjects:
        if subject not in original_subjects:
            original_subjects.append({"ref": subject})
    resource["subject"] = original_subjects
    logger.info("process_resource", action="append_subjects", data={"resource_uri": resource["uri"], "subjects" : original_subjects})
    return resource

def process_resource(resource_id,subject_list):
    resource = client.get('repositories/3/resources/' + resource_id).json()
    quick_backup(resource_id,resource)
    new_subjects = ["/subjects/" + sub for sub in subject_list.split("|")]
    original_subjects = resource["subjects"]
    if not original_subjects:
        new_resource = no_original_subjects(resource,new_subjects)
    else:
        new_resource = adding_subjects(resource,new_subjects,original_subjects)
    return new_resource

def process_csv(working_csv):
    with open(working_csv) as csvfile:
        pairs = csv.reader(csvfile)
        next(pairs,None) # skips header! Remove this line if your data does not have headers
        for row in pairs:
            new_resource = process_resource(row[0],row[1])
            new_filename = "new_resources/new-resource" + row[0] + ".json"
            with open(new_filename, "w") as makenew:
                json.dump(new_resource, makenew, indent=4)
        logfile.close()

working_csv = 'test_coll_subject.csv'

def decision_point(choice):
    if choice == "1":
        process_csv(working_csv)
    elif choice == "2":
        upload_resources(working_csv)
    else:
        print("You chose something else. Either you made a mistake or aborted the process, in which case safe call!")

choice = input("Type '1' to download resources and add subjects or '2' to upload the resources: ")

decision_point(choice)

# working_csv = 'Collection_Subjects.csv'

# input("What's the name of the CSV or something? ") # this line allows one to pass as a parameter
