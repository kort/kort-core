#!/bin/bash

HTTP=$(which http)

if [ ! -x "$HTTP" ]; then
    echo 'You need HTTPie to run this script!'
    echo 'sudo pip3 install httpie'
    exit 1
fi

#URL=:5000/v1.0
URL=https://test.kort.dev.ifs.hsr.ch/v1.0
set -x

http GET $URL/achievements user_id==-1 lang==en

http GET $URL/highscore type==all limit==10

http GET $URL/missions user_id==-1 lat==47.23 lon==8.12 radius==5000 limit==1 lang==en

http GET $URL/missions/osm/node/2810732510

http POST $URL/missions/15/43394950/solution solution:='{"koins": 0, "lang": "en", "option": "string", "osm_id": 0, "solved": false, "userId": 0, "value": "string"}'

http GET $URL/users/-1 Authorization:'the_secret'

http GET $URL/statistics

