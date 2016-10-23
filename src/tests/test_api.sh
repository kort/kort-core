#!/bin/bash

HTTP=$(which http)

if [ ! -x "$HTTP" ]; then
    echo 'You need HTTPie to run this script!'
    echo 'sudo pip3 install httpie'
    exit 1
fi

URL=:5000/v0.1

set -x

http PUT $URL/users/1 name=foo name=test username=username mission_count:=0 koin_count:=0 oauth_provider=google oauth_user_id=ouser pic_url=htttp://gravatar.com secret=nosecret token=token logged_in:=true last_login=2015-07-07T15:49:51.230+02:00
http $URL/users/1
http PUT $URL/users/1 name=otherfoo name=othertest username=username mission_count:=0 koin_count:=0 oauth_provider=google oauth_user_id=ouser pic_url=htttp://gravatar.com secret=nosecret token=token logged_in:=true last_login=2015-07-07T15:49:51.230+02:00
http $URL/users/1
http $URL/users name==test
http DELETE $URL/users/1