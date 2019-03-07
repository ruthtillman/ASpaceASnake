#!/usr/bin/env python
import re, glob, json
# this script is intended to take a .txt of raw 650 fields content broken by lines. The data should not have indicators or the quotation marks which may wrap a term if it contains commas and was extracted from a CSV.

###############
# Sample Data #
###############
# $aAfrican American artists$vInterviews
# $aMennonites$xSocial life and customs
# $aMexican War, 1846-1848$zPennsylvania$zLewistown (Mifflin County)$vPosters
# It can handle |a instead of $a, but it does expect some kind of delimiter and you'll need to substitute them.

def get_title(subject):
    '''Generates the title by substituing all subfield keys with -- and then removing the -- which replaced subfield $a.'''
    title = re.sub(r'\$\w', '--', subject).lstrip('--')
    return title

def get_subfields(subject):
    '''Breaks down the subject into subfields, each beginning with the subfield code, e.g. a, d, z, 1 (if you left in 1, which you should not as this script can't handle it w/o your changes.)'''
    subfields = subject.lstrip('$').split('$') # have to strip off the initial $ or it will create a null item in the array.
    terms = parse_subfields(subfields)
    return terms

def parse_subfields(subfields):
    '''Builds an array of terms. Note that this contains some hardcoding that you should review against your data and your repository before you run this script! Hardcoded fields are commented.'''
    subfield_dict = {'a': 'topical', 'b': 'topical', 'c' : 'geographic', 'd': 'temporal', 'v': 'genre_form', 'x': 'topical', 'y': 'temporal', 'z': 'geographic'} # HARDCODED DICTIONARY. You will need to strip other subfields or update this dictionary.
    terms_array = []
    for each in subfields:
        term_entry = {'jsonmodel_type':'term','vocabulary': '/vocabularies/1'} # HARDCODED VOCABULARY
        term_entry['term_type'] = subfield_dict[each[:1]]
        term_entry['term'] = each[1:]
        terms_array.append(term_entry)
    return terms_array

def make_subject(field):
    '''Builds the subjects. Note that this contains some hardcoding that you should review against your data and your repository before you run this script! Hardcoded fields are commented.'''
    real_field = field.strip('\n').strip('"') # abundance of caution
    title = get_title(real_field)
    subfields = get_subfields(real_field)
    base_subject='{"jsonmodel_type":"subject", "publish": true, "source": "Library of Congress Subject Headings","vocabulary":"/vocabularies/1"}' # HARDCODED VOCABULARY
    base = json.loads(base_subject)
    base['title'] = title
    base['terms'] = subfields
    return base

def write_subjects(source_file,filestem,target_dir):
    '''Writes out your subjects into the directory of your choice'''
    subject_num = 1 # this just creates some numbering to differentiate the files. ASpace will number them differently!
    with open(source_file, 'r') as source:
        for line in source:
            output = make_subject(line)
            filename = target_dir + "/" + filestem + str(subject_num) + '.json'
            with open(filename, 'w') as subject_file:
                json.dump(output, subject_file, indent=4)
            subject_num += 1

target_dir = input("What's the relative or full path to the directory where you'd like to output these subject files? (must already exist ) ")
source = input("What's the name of the source file? ")
filestem = input("What filestem should I use? ")

write_subjects(source,filestem,target_dir)
