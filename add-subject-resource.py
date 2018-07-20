import re, json, csv, requests, glob, logging
# add ASnake Client
from asnake.client import ASnakeClient

# validate ASnake client
# open CSV and get two values. value 1 is the resource_id, value 2 should be split on | and put into an array. is there a way to put it into an array and attach the `/subjects/` at the same time?
# for resource_id, download the JSON object.
# test if its subjects array is empty. if so, run a function which just appends the pairing into subjects.
# if subject array is NOT empty, then extract the values of subject/ref into their own array. Then use for item in new_array: / if item not in mine: \ mine.append thing into subjects itself (NOT into the little list?)
# then dump resource as JSON file with the resource_id as the name. then write a script to upload resources for the same CSV with resource_id being passed to each.
# is it possible to make this also into this file and then simply choose which function one wanted to run, a la bash?
# test subject fields: 1129|1168|1169|117|1275|1293
#  new_subjects =
#
#
#


# Create and authorize a client to ASnake!
client = ASnakeClient()
client.authorize()


working_csv = 'Collection_Subjects.csv'
with open(working_csv) as csvfile:
    pairs = csv.reader(csvfile)
    next(pairs,None) # skips header! Remove this line if your data does not have headers
    for row in pairs:
        print(row[0])
        print(row[1])

ASpaceID,subject_ids


# Getting subjects from the CSV, turning them into a usable array.

new_subjects = ["/subjects/" + sub for sub in csv_subjects.split("|")]

# get the JSON object's value. Assign subjects to "original_subjects"

original_subjects = client.get('repositories/3/resources/' + resource_id).json()["subjects"]
starter_subjects = []
for sub in original_subjects:
    starter_subjects.append(sub["ref"])


# "if not original_subjects" == it's an empty array, just put stuff on it. else, do the other function.
