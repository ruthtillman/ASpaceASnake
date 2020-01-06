import os, json, csv, datetime

# This file downloads subjects as full strings
# it puts them in a CSV to be reconciled.
# it can limit by just a kind of like LCSH

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

def write_subject_csv(csvName):
    fieldnames = ['ASpaceID', 'subject', 'LC_URI']
    with open(csvName, 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
        writer.writeheader()
        get_all_subs(writer)

def get_all_subs(writer):
    all_ids = client.get('/subjects?all_ids=true').json()
    for sub_id in all_ids:
        subject = client.get('/subjects/' + str(sub_id)).json()
        if subject['source'] == 'Library of Congress Subject Headings':
            writer.writerow({'ASpaceID': str(sub_id), 'subject' : subject['title']})

csvName = input("Name of new CSV: ")
write_subject_csv(csvName)
