#!/bin/sh

# First, kill off any potentially
# running daemons by sending them all a SIGINT...
killall -2 mongod >/dev/null 2>&1
sleep 2

# Now, if there's a lock file still present then mongod wasn't running
# and we need to clean things up.
if [ -f /data/db/mongod.lock ]; then
   rm -f /data/db/mongod.lock
   mongod --repair >/tmp/mongod.repair.log 2>&1
fi

# Now, run mongod and have it fork off to become a daemon.  
# Logs will be discarded
mongod --fork --logpath /dev/null --logappend

