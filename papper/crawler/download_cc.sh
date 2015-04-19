#!/bin/bash

artifact_dir="./cc"
creative_commons="${artifact_dir}/arxiv.cc"
request_delay=25

if [ ! -d "${artifact_dir}" ]
then
    mkdir -p "${artifact_dir}"
fi

grep -i creativecommon arxiv.csv | cut -d';' -f1 | tr -d '"' | cut -d':' -f3 | sort | uniq > "${creative_commons}"

while read arxiv_id
do
    artifact="${artifact_dir}/${arxiv_id}.gz"

    if [ ! -e "${artifact}" ]
    then
        curl --header 'Host: arxiv.org' \
             --header 'DNT: 1' \
             --header 'Connection: keep-alive' \
             "http://arxiv.org/e-print/${arxiv_id}" -o "${artifact}" -L   
        sleep ${request_delay}
    fi
done < "${creative_commons}"