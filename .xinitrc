#!/bin/bash
# Need to look into if I even still need this portion of it
eval $(dbus-launch --sh-syntax)
export XDG_RUNTIME_DIR="/run/user/$(id -u)"

openbox-session &
/home/justin/run-chores.sh > /home/justin/chores.log 2>&1
