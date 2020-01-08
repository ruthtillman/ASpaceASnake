import os, json, re, csv, glob

# assumes we are iterating over a full download of resources... which I just happen to have right now.

def get_restrictions(writer):
    files = glob.glob("*.json")
    for jsonFile in files:
          res_num = jsonFile.rstrip('.json')
          resource = json.load(open(jsonFile))
          for language in resource['language_and_script']:
              if 'language_and_script' in language:
                language['language_and_script']['language']
              else:
                language

          for note in resource['notes']:
            if 'type' in note and note['type'] == 'userestrict':
              for sub in note['subnotes']:
                writer.writerow({'ASpace_ID' : res_num, 'Note_ID' : note['persistent_id'], 'Note_Type' : note['type'], 'Note_Content': sub['content'] })


def write_notes_csv(csvName):
    fieldnames = ['ASpace_ID', 'Note_ID', 'Note_Type', 'Note_Content']
    with open(csvName, 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
        writer.writeheader()
        get_restrictions(writer)

write_notes_csv('../userestrict_notes.csv')
