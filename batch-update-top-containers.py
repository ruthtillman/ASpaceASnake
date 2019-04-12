import os, json, csv, datetime
import asnake.logging as logging

# This file performs batch updates to top container records, adding locations. The API expects to add a single location to every top container which is in that location. It expects a two-column CSV with columns 'location_uri' and 'id'. 'id' is comma-separated (Excel, OpenRefine, etc. will add "") list with all the IDs of top containers in that location.
# Sample data:
# location_uri,id
# /locations/6423,6631
# /locations/4025,"24592, 23842, 23232"
#  Admin rights seem to be needed to run these updates.
# See README.md for information on preparing the data.

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

logname = 'logs/update_top_containers_' + datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + '.log'
logfile = open(logname, 'w')
logging.setup_logging(stream=logfile)
logger = logging.get_logger('batch-update-top-containers')

def post_batch_updates(csvName,batch,repo_num):
    '''Starts logger batch, opens CSV and reads lines. Creates an integer-based list of IDs from column 'id'. Posts updates to ASpace, collects response and writes it out to log along with info about which resources were updated (since this is not part of ASpace response). Closes logfile.'''
    logger.info('updates', batch_name=batch)
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            id_group = [] # ASpace is really particular that it get a list of integers and no dang strings.
            for id in row['id'].split(","):
                id_group.append(int(id))
            location = row['location_uri']
            response = client.post('repositories/' + repo_num + '/top_containers/batch/location', params={'ids': id_group , 'location_uri': location } ).json()
            logger.info('add-location', ids=row['id'], location=location, response=response)
        logfile.close()

csvName = input("Name of source CSV: ")
batch = input("Provide a name for your upload batch: ")
repo_num = input("Input the repository number to call from, e.g. '4': ")
post_batch_updates(csvName,batch,repo_num)
