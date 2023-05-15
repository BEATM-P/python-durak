#/bin/bash

alacritty  -e /bin/python /home/pm/Projects/python-durak/server.py -l &
sleep 2
#//lacritty -e /bin/python /home/pm/Projects/python-durak/window.py lel 192.168.0.108:8080 &
alacritty -e /bin/python /home/pm/Projects/python-durak/window.py 1232124 192.168.0.108:8080 &
alacritty -e /bin/python /home/pm/Projects/python-durak/window.py asfdf 192.168.0.108:8080 &
