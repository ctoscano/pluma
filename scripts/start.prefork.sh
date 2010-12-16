#!/bin/sh
kill `cat /var/tmp/pluma.pid`
rm /var/tmp/pluma.pid 
su www-data -c "./example/manage.py runfcgi method=prefork host=127.0.0.1 port=8000 pidfile=/var/tmp/pluma.pid"