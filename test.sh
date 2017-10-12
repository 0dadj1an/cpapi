#!/bin/bash
python3 cpapiweb/run.py &

sleep 5

CODE=$(curl -s -I -X GET http://127.0.0.1:8080/login | awk '/HTTP/{print $2}')

echo $(CODE)

if [[ $CODE == "200" ]]; then
    exit
else
    exit 1
fi
