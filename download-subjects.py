import os, json

# This file downloads all subjects

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

def get_all_subjects(tar_dir):
    all_ids = client.get('/subjects?all_ids=true').json()
    for sub_id in all_ids:
        newJSON = tar_dir + "/" + str(sub_id) + '.json'
        subject = client.get('/subjects/' + str(sub_id)).json()
        with open(newJSON, 'w') as outfile:
            json.dump(subject, outfile, sort_keys=True, indent=4)

tar_dir = input("Name of target directory: ")
get_all_subjects(tar_dir)
