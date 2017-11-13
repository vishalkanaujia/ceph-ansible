#!/bin/bash
isnum() {
    num=$1 
    [ ! -z "${num##*[!0-9]*}" ] && echo "1" || echo "0"
}

generate_rate_limit() {
    num=$1
    if [ "$num" == "" ]; then
	num=$(ansible rgws -i ../hosts/$D42_APPID --list-hosts | wc -l)
	if [ $num -eq 0 ]; then
		echo "Invalid number of rgw hosts"
		exit 1
	fi
    fi
    python generate_rate_limits.py $num
}
