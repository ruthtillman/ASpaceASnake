import json, csv

def parse_subject_upload_IDs(log,newCSV):
  fieldnames = ['id','subject']
  with open(newCSV, 'w', newline='') as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for line in open(log):
      resource = json.loads(line)
      if 'response' in resource:
        response = resource['response']
        if 'status' in response:
          writer.writerow({'id': response['id'], 'subject': response['title']})
        elif 'error' in response:
          id = response['error']['conflicting_record'][0].replace('/subjects/','')
          writer.writerow({'id': id, 'subject': response['title']})


#log = input("path to log and logname: ")
#newCSV = input("name your new CSV: ")

log = "logs/new_subject_upload_2020-02-27-T-11-06.log"
newCSV = "data/bad_subjects_3_replacements.csv"

parse_subject_upload_IDs(log,newCSV)
