#!/bin/bash

HTTP=$(which http)

if [ ! -x "$HTTP" ]; then
    echo 'You need HTTPie to run this script!'
    echo 'sudo pip3 install httpie'
    exit 1
fi

URL=:5000

set -x

http PUT $URL/user/1 name=foo name=test
http $URL/user/1
http PUT $URL/user/1 name=foo name=otherTest
http $URL/user/1
http $URL/user name==test
http DELETE $URL/pets/1