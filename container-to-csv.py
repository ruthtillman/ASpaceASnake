import csv, json

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

def startCSV(CSV):
    '''Creates the CSV with field names and writes header'''
    fieldnames = ['lock_version', 'indicator', 'uri', 'collection_identifier', 'series_identifier']
    with open(CSV, 'w', newline='') as outputCSV:
         writer = csv.DictWriter(outputCSV, fieldnames=fieldnames)
         writer.writeheader()

def addCSV(CSV, lock, ind, uri, coll_id, ser_id):
    '''Opens CSV, appends row'''
    fieldnames = ['lock_version', 'indicator', 'uri', 'collection_identifier', 'series_identifier']
    with open(CSV, 'a', newline='') as outputCSV:
         writer = csv.DictWriter(outputCSV, fieldnames=fieldnames)
         writer.writerow({'lock_version' : lock, 'indicator' : ind, 'uri' : uri, 'collection_identifier' : coll_id, 'series_identifier' : ser_id})

def generate_csv(CSV,repo_num):
    '''Calls ASpace API to return paged repositories. Checks to be sure the record isn't None. Gets fields lock version, indicator, URI, determins whether it's in a collection or series, gets the identifiers from the collection or series. Otherwise returns them as blank. Writes results into CSV.'''
    startCSV(CSV)
    for record in client.get_paged('repositories/' + repo_num + '/top_containers'):
        if record is not None:
            lock = record["lock_version"]
            indicator = record["indicator"]
            uri = record["uri"]
            if record["collection"] != []:
                collection_id = record["collection"][0]["identifier"] # because collection is a list
            else:
                collection_id = ''
            if record["series"] != []:
                for instance in record["series"]:
                    series_id = instance["identifier"] # getting the identifier if it exists
                    addCSV(CSV, lock, indicator, uri, collection_id, series_id)
            else:
                series_id = ''
                addCSV(CSV, lock, indicator, uri, collection_id, series_id)

newCSV = input("Name your new CSV (include '.csv'): ")
repo_num = input("Input the repository number to call from, e.g. '4': ")
generate_csv(newCSV, repo_num);
