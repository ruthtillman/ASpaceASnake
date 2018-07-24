import re, json, csv, requests, glob, datetime, os
import asnake.logging as logging

# fuk u logging
# expects a 2-column CSV in which the first column has the resource ID and the second has the subject ID. Multiple subject IDs should be pipe-separated, e.g. "24|133|1313|234" or just 24. These subjects should only be _new_ subjects you're adding.

logname = 'logs/resource_processing_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'

logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger("add-subjects-log")

# add ASnake Client
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

# WRITE OUT THE ORIGINAL TO ANOTHER DIRECTORY AS A BACKUP. This is a place where one could take a param. Remember to either commit your backups each time or move them entirely because otherwise you'll end up with them being undone.
def quick_backup(resource_id,resource):
    original = "backups/original-" + resource_id + ".json"
    with open(original, "w") as backup:
        json.dump(resource, backup, indent=4)

# This function is what we do if the subject array is empty. Simply builds the array and fills subjects.
def no_original_subjects(resource,new_subjects):
    subjects = []
    for subject in new_subjects:
        subjects.append({"ref": subject})
    resource["subjects"] = subjects
    logger.info("process_resource", action="new_subjects", data={"resource_uri": resource["uri"], "subjects" : subjects})
    return resource

# This function is what we do if the subject array is not empty. You have already cleaned it up to move it from dicts with ref to an array of parallel subject URIs as the new_subjects. First you append the new subjects WHICH ARE NOT DUPLICATES onto subjects. Then you rewrite them all out. Then you write it in the same way. It logs differently so you can check.

def adding_subjects(resource,new_subjects,original_subjects):
    full_subjects = []
    for subject in new_subjects:
        if subject not in original_subjects:
            original_subjects.append(subject)
    for subject in original_subjects:
      full_subjects.append({"ref": subject})
    resource["subjects"] = full_subjects
    logger.info("process_resource", action="append_subjects", data={"resource_uri": resource["uri"], "subjects" : full_subjects})
    return resource

# turns the original subjects into a vanilla list. Because subjects are modeled as an array of dicts and we need to get them into a regular array.

def get_original_subjects(sublist):
  list = []
  for item in sublist:
    list.append(item["ref"])
  return list

# Gets the resource from our API (note that we are not using repository number in config but maybe I should ask for that too? right now it's hardcoded.) Runs quick backup. Turns string that is subjects with pipe separation, e.g" "2324|1313" into "/subjects/2324", "/subjects/1313". Figure out if the resource already had subjects. Then pass it off to functions to manage it accordingly. Retrun the new resource to the previous function so we can write it back out.

def process_resource(resource_id,subject_list):
    resource = client.get('repositories/3/resources/' + resource_id).json()
    quick_backup(resource_id,resource)
    new_subjects = ["/subjects/" + sub for sub in subject_list.split("|")]
    original_subjects = resource["subjects"]
    if not original_subjects:
        new_resource = no_original_subjects(resource,new_subjects)
    else:
        original_subjects = get_original_subjects(original_subjects)
        new_resource = adding_subjects(resource,new_subjects,original_subjects)
    return new_resource

# opens the working CSV, gets values, runs processing script, makes new filename, and dumps into JSON file. Stops log.

def process_csv(working_csv):
    with open(working_csv) as csvfile:
        pairs = csv.reader(csvfile)
        next(pairs,None) # skips header! Comment out this line if your data does not have headers
        for row in pairs:
            new_resource = process_resource(row[0],row[1])
            new_filename = "new_resources/new-resource-" + row[0] + ".json" # note if filename is being made differently check this + place in upload_resources because these pair.
            with open(new_filename, "w") as makenew:
                json.dump(new_resource, makenew, indent=4)
        logfile.close()

working_csv = input("What's the name of the CSV which has your pairings? ")
