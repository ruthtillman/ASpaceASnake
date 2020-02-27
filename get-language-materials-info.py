import os, json, re, csv, glob

# assumes we are iterating over a full download of resources... which I just happen to have right now.

def get_language(source_dir,tar_dir):
    os.chdir(source_dir)
    files = glob.glob("*.json")
    for jsonFile in files:
          res_num = jsonFile.rstrip('.json')
          resource = json.load(open(jsonFile))
          for language in resource['lang_materials']:
              if 'language_and_script' in language:
                langcode = language['language_and_script']['language']
                if langcode == 'und':
                    language['language_and_script']['language'] = 'eng'
                    filepath = tar_dir + "/" + jsonFile
                    with open(filepath, 'w') as outfile:
                        json.dump(resource, outfile, sort_keys=True, indent=4)

## get all the ones without language keys?

def no_lang_key(source_dir):
    files = glob.glob("*.json")
    for jsonFile in files:
      res_num = jsonFile.rstrip('.json')
      subject = json.load(open(jsonFile))
      for language in subject["lang_materials"]:
        if "language_and_script" not in language:
          language


source_dir = input("Name of soure directory: ")
tar_dir = input("Relative path from source to output directory (no trailing slash): ")
get_language(source_dir,tar_dir)
