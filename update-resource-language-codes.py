import json, os, glob

def updating_language_codes(sourceDirectory,targetDirectory):
    os.chdir(sourceDirectory)
    resources = glob.glob("*.json")
    for resource in resources:
        with open(resource, "r") as myJSON:
              recorddata = json.loads(myJSON.read())
              if recorddata['finding_aid_language'] == "und" or recorddata['finding_aid_script'] == "Zyyy":
                  if recorddata['finding_aid_language'] == "und":
                      recorddata['finding_aid_language'] = "eng"
                  if recorddata['finding_aid_script'] == "Zyyy":
                      recorddata['finding_aid_script'] = "Latn"
                  output = targetDirectory + "/" + resource
                  with open(output, 'w') as outfile:
                      json.dump(recorddata, outfile, sort_keys=True, indent=4)


sourceDirectory=input("Path to the directory containing resources: ")
tarDirectory=input("Path to the output directory: ")

updating_language_codes(sourceDirectory,tarDirectory)
