#!/bin/bash
while true; do
	echo "starting Chore App" >> /home/justin/chores.log
	/usr/bin/python3 /usr/code/pyChore/MainWindow.py
	echo "App Crashed with code $?" >> /home/justin/chores.log
	sleep 3
done
