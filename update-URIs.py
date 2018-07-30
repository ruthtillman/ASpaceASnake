#!/usr/bin/env python

#This script exists so that we can work separately with ASpace data, create a spreadsheet (CSV) of the IDs of subjects which should be updated to include any authority_id but probably a URI.

# The data is easiest to get through MySQL queries, which are a simple way to retrieve all the subjects as strings along with their IDs. One then reconciles that spreadsheet against LCSH in OpenRefine and extracts URIs into their own column. Then one drops the subject as string.

import os, json, csv, datetime

def write_URI(subject_id,uri):
    '''This assumes that when you downloaded your subjects, you didn't prefix them with anything, so subject 9035 is 9035.json, etc. It will write out with a filestem of "new-" but you can also edit that to be something like "new/" + jsonFile, which would put it in a directory called new.'''
    jsonFile = subject_id + '.json'
    subject = json.load(open(jsonFile))
    newJson = 'new-' + jsonFile # to put in a directory called 'new', change the '-' to a '/'. And ensure the directory exists.
    if subject.has_key('authority_id'):
        if subject['authority_id'] == '':
            subject['authority_id'] = uri
            write_subject_JSON(subject,newJson)
        elif subject['authority_id'] == ' ':
            subject['authority_id'] = uri
            write_subject_JSON(subject,newJson)
        else:
    else:
        subject['authority_id'] = uri
        write_subject_JSON(subject,newJson)


def write_to_JSON(content,newJson):
    '''Does that thing.'''
    with open(newJson, 'w') as outfile:
        json.dump(content, outfile, sort_keys=True, indent=4)

def process_CSV(csvName):
    '''Opens the CSV which has been provided as input by the user, opens and passes to a CSV parser, and for each row calls the function to add test for and add authority_ids if they don't exist, passing along the values for the id column and URI column from the CSV.'''
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            write_URI(row['id'],row['uri'])

csvName = input('Enter the CSV name: ')

# needs to take a directory where the subjects exist
# we need a script just to download subjects based on feeding them some kind of list of IDs.

process_CSV(csvName)
