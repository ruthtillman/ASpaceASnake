import os, json

# This file downloads all resources by repository

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

def get_all_resources(tar_dir,repo_num):
    all_ids = client.get('repositories/' + repo_num + '/resources?all_ids=true').json()
    for resource_id in all_ids:
        newJSON = tar_dir + "/" + str(resource_id) + '.json'
        resource = client.get('repositories/' + repo_num + '/resources/' + str(resource_id)).json()
        with open(newJSON, 'w') as outfile:
            json.dump(resource, outfile, sort_keys=True, indent=4)

tar_dir = input("Name of target directory: ")
repo_num = input("Repository number: ")
get_all_resources(tar_dir,repo_num)
