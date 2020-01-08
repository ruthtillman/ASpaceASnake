#!/usr/bin/env python
import json, glob, datetime, re, os
import asnake.logging as logging

# set up logging. mutter profanity.

logname = 'logs/uploading_updated_resources_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'

logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger('upload_updated_resources')

# add ASnake Client
from asnake.client import ASnakeClient
# validate ASnake client
client = ASnakeClient()
client.authorize()

def upload_updated_resources(file_directory,file_prefix,repo_num):
    '''This scans the entire directory which the user has supplied and globs JSON files. It gets the resource number from using the prefix which the person supplied.'''
#    filename_strip = '.*' + file_prefix
    os.chdir(file_directory)
    resources = glob.glob('*.json')
    for file in resources:
        res_num = file.rstrip('.json')
#        res_num = re.sub(filename_strip, '', res_num)
        resource = json.load(open(file))
        response = client.post('repositories/' + repo_num + '/resources/' + res_num, json=resource).json()
        logger.info('process_resource', action='upload_resource', resource_id=res_num, response=response)
    logfile.close()

file_directory = input("What's the relative or full filepath of the directory where the JSON objects are stored? Do not include trailing slash: ")

file_prefix = input("What's the prefix of the file before the resource number, including hyphens? ")

repo_num = input("What repository will you be using? ")

upload_updated_resources(file_directory, file_prefix,repo_num)
