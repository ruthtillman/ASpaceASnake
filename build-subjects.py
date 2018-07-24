import re, glob, json
# this script is intended to take a .txt of raw 650 fields content broken by lines. The data should not have indicators or the quotation marks which may wrap a term if it contains commas and was extracted from a CSV.

###############
# Sample Data #
###############
# $aAfrican American artists$vInterviews
# $aMennonites$xSocial life and customs
# $aMexican War, 1846-1848$zPennsylvania$zLewistown (Mifflin County)$vPosters
# It can handle |a instead of $a, but it does expect some kind of delimiter and you'll need to substitute them.

# Generates the title by substituing all subfield keys with -- and then removing the -- which replaced subfield $a.

def get_title(subject):
  title = re.sub(r"\$\w", "--", subject).lstrip("--")
  return title

def get_subfields(subject):
  subfields = subject.split('$')
  del subfields[0]
  terms = parse_subfields(subfields)
  return terms

def parse_subfields(subfields):
  subfield_dict = {"a": "topical", "b": "topical", "d": "temporal", "v": "genre_form", "x": "topical", "y": "temporal", "z": "geographic"}
  terms_array = []
  for each in subfields:
    term_entry = {"jsonmodel_type":"term","vocabulary": "/vocabularies/1"}
    term_entry["term_type"] = subfield_dict[each[:1]]
    term_entry["term"] = each[1:]
    terms_array.append(term_entry)
  return terms_array

def make_subject(field):
  real_field = field.strip("\n").strip('"') # abundance of caution
  title = get_title(real_field)
  subfields = get_subfields(real_field)
  base_subject='{"jsonmodel_type":"subject", "publish": true, "source": "Library of Congress Subject Headings","vocabulary":"/vocabularies/1"}'
  base = json.loads(base_subject)
  base["title"] = title
  base["terms"] = subfields
  return base

def write_subjects(source_file,filestem):
  subject_num = 1
  with open(source_file, "r") as source:
    for line in source:
      output = make_subject(line)
      filename = filestem + str(subject_num) + ".json"
      with open(filename, "w") as subject_file:
        json.dump(output, subject_file, indent=4)
        subject_num += 1

source = input("What's the name of the source file? ")
filestem = input("What filestem should I use? ")

write_subjects(source, filestem)
