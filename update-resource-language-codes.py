import json

fileName = "new-5.json"

with open(fileName, "r") as myJSON:
      recorddata = json.loads(myJSON.read())
      if recorddata['finding_aid_language'] == "und" or recorddata['finding_aid_script'] == "Zyyy":
          if recorddata['finding_aid_language'] == "und":
              recorddata['finding_aid_language'] = "eng"
          if recorddata['finding_aid_script'] == "Zyyy":
              recorddata['finding_aid_script'] = "Latn"
          with open("test.json", 'w') as outfile:
              json.dump(recorddata, outfile, sort_keys=True, indent=4)
      else:
          print("nope")
