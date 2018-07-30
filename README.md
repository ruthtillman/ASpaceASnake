# ArchivesSpace and ArchivesSnake Scripts

This is a project to collect and document my scripts which engage with our local ArchivesSpace using the ArchivesSnake Python library. It uses the Configuration https://github.com/archivesspace-labs/ArchivesSnake#configuration kept in my home folder. Of note -- the repository is a hardcoded value in these scripts.

Code is commented. Please read the comments! There is substantial potential for reuse, but you'll need to know what's hardcoded.

These scripts were built for a specific project of creating subjects, updating subjects with URIs, uploading subjects, adding subjects to resources, and uploading the updated resources. I slowly updating and genericizing them for my own reuse (e.g. a script which takes more params and uploads multiple types of objects).

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
