#!/bin/bash
jq_cmd="curl --silent 'http://10.33.65.0:8080/apps/$2/instances' | jq .[] | jq 'select(.primary_ip ==\"$1\")' | jq .zone | sed -e 's/^\"//'  -e 's/\"$//' "
eval $jq_cmd
