# ArchivesSpace and ArchivesSnake Scripts

This is a project to collect and document my scripts which engage with our local ArchivesSpace using the ArchivesSnake Python library. It uses the Configuration https://github.com/archivesspace-labs/ArchivesSnake#configuration kept in my home folder. Of note -- the repository is a hardcoded value in these scripts.

The script expects the `backups` directory and `logs` directory to exist! Don't delete these.

Code is commented. Please read the comments! There is substantial potential for reuse, but you'll need to know what's hardcoded.

These scripts were built for a specific project of creating subjects, updating subjects with URIs, uploading subjects, adding subjects to resources, and uploading the updated resources. I am slowly updating and genericizing them for my own reuse (e.g. a script which takes more params and uploads multiple types of objects).

## Build Subjects - build-subjects.py

This script is intended to take a .txt of raw 650 fields content broken by lines. Subfields which were not being imported were already stripped. The data should not have indicators or the quotation marks which may wrap a term if it contains commas and was extracted from a CSV. It could handle delimiters other than `$` but you would need to find and hardcode those in.

Sample data:

```
$aAfrican American artists$vInterviews
$aMennonites$xSocial life and customs
$aMexican War, 1846-1848$zPennsylvania$zLewistown (Mifflin County)$vPosters
```

It asks you to provide the name of the source file and a filestem for the subjects you're creating.

It does hardcode a couple values related to the vocabulary which you're using. Ensure you check these match the vocabulary name/number in your ArchivesSpace repo. It can handle the following subfields. You would need to add any others and determine whether they needed specialized behaviors (e.g $2, which I stripped from the initial document): $a, $b, $c, $d, $v, $x, $y, $z.

Note that it does not yet handle $0 (or $1) URIs as I wanted to work with these directly because we have almost no $0s and no $1s in our MARC records for archival materials.

There is no need to identify existing terms with ASpace TERM URIs, as ArchivesSpace will match them to the appropriate URIs.

## Upload New Subjects - upload-new-subjects.py

Takes a batch name and path to the directory where your new subjects exist. It's a pretty straightforward upload script which posts every JSON object in the directory to ArchivesSpace.

Important ArchivesSpace note: ArchivesSpace will detect any duplicates and reject them. As mentioned above, it matches terms.

## Update URIs in Subject JSON - update-URIs.py

Once you've reconciled authorities with URIs, this takes the ID and the URI and updates.

(This is currently properly working for subjects but should probably be checked to ensure it can handle other kinds of authorities. Do they use the same field?)

## Update Resources - update-resources.py

Updates the resource object with relationships to subjects by IDs. It expects a 2-column CSV in which the first column has the resource ID and the second has the subject ID. Multiple subject IDs should be pipe-separated, e.g. "24|133|1313|234" or just 24. These subjects should only be _new_ subjects you're adding. The script checks to ensure a relationship doesn't already exist. It appends them to the existing record. If ordering is important, you'll need to ensure your subject IDs are ordered properly in the CSV. If appending to existing records, you would need to check the resulting resource objects.

## Upload Updated Resources - upload-updated-resources.py

Uploads the updated resource objects. Look into consolidating this with subjects into just one upload script...

## Build CSV of Containers Information - container-to-csv.py

Gathers data for the management and updating of containers. Downloads paged containers list, iterates through each record, and extracts the lock ID, the indicator, the URI, the collection ID (if exists), and the series ID (if exists). If there is more than one series, creates a separate row for each series entry.

CSV headers are:

`lock_version, indicator, uri,	collection_identifier,	series_identifier`

Expects input of the repository number with which you're working and a name for the CSV you want to output.

## Batch Update Top Containers - batch-update-top-containers.py

Uses the API to add locations to top container records. Requires only a CSV pairing the ID of the top container(s) and the URI of the location. Updates expect one location_uri which may be added to any number of top containers. Excepts the CSV to have two columns, as shown below, with rows of multiple ids pipe-separated.

Sample data:
```
location_uri,id
/locations/6423,6631
/locations/4025,24592|23842|23232
```

To create this data from pairings, e.g.

```
location_uri,id
/locations/4025,24592
/locations/4025,23842
/locations/4025,23232
```

upload your data into OpenRefine. Blank down the 'location_ur' column. In the 'id' column, choose Edit Cells from the drop-down, join multi-valued cells, use | separator. Download as CSV. The script can also run against paired data, but will take longer to process.

Note: Admin rights seem to be needed to run these updates.

## Download All Subjects as JSON - download-subject.py

Connects, downloads all subject records as JSON files to a specified directory. Ensure directory exists.

## Download Data from Subject Records - download-subject-data.py

Generic script to get all subject IDs and download. Downloads data to a CSV while allowing one to specify filtering criteria and also fields downloaded. Can be adapted to get various fields.

## Future Work

* Update logging when ASnake updates logging methods
* Generic upload and download scripts. Determine possible sources of data. Determine how much/little breakdown there should be.
