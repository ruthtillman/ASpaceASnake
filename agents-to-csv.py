import csv, json

def startCSV(CSV):
    '''Creates the CSV with field names and writes header'''
    fieldnames = ['name','uri','contact','used','auth_id']
    with open(CSV, 'w', newline='',encoding='utf-8') as outputCSV:
         writer = csv.DictWriter(outputCSV, fieldnames=fieldnames)
         writer.writeheader()

def addtoCSV(CSV, name, uri, contact, used,auth_id):
    '''Opens CSV, appends row'''
    fieldnames = ['name','uri','contact','used','auth_id']
    with open(CSV, 'a', newline='',encoding='utf-8') as outputCSV:
         writer = csv.DictWriter(outputCSV, fieldnames=fieldnames)
         writer.writerow({'name': name, 'uri': uri, 'contact': contact, 'used' : used, 'auth_id': auth_id })

def create_agent_csv(CSV):
  startCSV(CSV)
  for agent in client.get_paged('/agents/people'):
      name = agent['title']
      uri = agent['uri']
      contact = agent['agent_contacts']
      used = agent['used_within_published_repositories']
      if 'authority_id' in agent['display_name']:
          auth_id = agent['display_name']['authority_id']
      else:
          auth_id = ''
      addtoCSV(CSV, name, uri, contact, used, auth_id)

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

CSV = input("Name your CSV: ")
create_agent_csv(CSV)
