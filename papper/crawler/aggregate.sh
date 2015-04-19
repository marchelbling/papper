#!/bin/bash

# pip install xmlutils
for data in *.xml
do
    if [ ! -e arxiv.csv ]
    then
        # create header
        xml2csv --input "${data}" --output "header.csv" --tag "{http://www.openarchives.org/OAI/2.0/}record" --delimiter ";" --limit 1 >/dev/null
        head -1 header.csv > arxiv.csv && rm header.csv
    fi
    xml2csv --input "${data}" --output "convert.csv" --tag "{http://www.openarchives.org/OAI/2.0/}record" --delimiter ";" --noheader >/dev/null
    # concatenate lines: http://superuser.com/a/565566/218469 & http://unix.stackexchange.com/a/14221
    vim convert.csv "+:v/^\"oai:/-1j" "+wq"
    # append to global csv
    cat convert.csv >> arxiv.csv && rm convert.csv
    echo "."
done
