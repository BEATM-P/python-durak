#/bin/bash

alacritty  -e /bin/python /home/alla/Projects/python-durak/server.py -l &
alacritty -e /bin/python /home/alla/Projects/python-durak/window.py lel 192.168.0.101:8080 &
alacritty -e /bin/python /home/alla/Projects/python-durak/window.py 22 192.168.0.101:8080 &
