#! /bin/bash

minute=$(date '+%M')
let "m = minute % 10"

if [ $m != 0 ]; then
    exit
fi

if [ -f /tmp/shouter.run ]; then
    echo Already running
    exit
fi

if [ -f $OPENSHIFT_DATA_DIR/db.sqlite3.new ]; then
    echo Database exists
    exit
fi

echo "shouter" > /tmp/shouter.run

cd $OPENSHIFT_REPO_DIR/wsgi/mechanicalbear/shouter
/bin/env python shouter.py >> /tmp/shouter.run 2>&1

mv /tmp/shouter.run $OPENSHIFT_DATA_DIR/shouter.log
echo Exitting normally

date > /tmp/last_date_cron_ran
