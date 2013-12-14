#! /bin/bash

minute=$(date '+%M')
let "m = minute % 10"

if [ $m != 0 ]; then
    exit
fi

if [ -f /tmp/shouter.run ]; then
    exit
fi
if [ -f $OPENSHIFT_DATA_DIR/db.sqlite3.new ]; then
    exit
fi

echo "shouter" > /tmp/shouter.run

cd $OPENSHIFT_REPO_DIR/wsgi/mechanicalbear/shouter
/bin/env python shouter.py >> /tmp/shouter.run 2>&1
#cp ../db.sqlite3 $OPENSHIFT_DATA_DIR

rm /tmp/shouter.run

date > /tmp/last_date_cron_ran
