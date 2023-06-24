import PyInstaller.__main__
import os

print(os.name) 

if os.name=='nt':
    PyInstaller.__main__.run([ 'D:\Projects\python-durak\windows\PythonDurak.spec', 'D:\Projects\python-durak\window.py' ])
else:
    PyInstaller.__main__.run([ '/home/alla/Projects/python-durak/dist_linux/PythonDurak.spec', '/home/alla/Projects/python-durak/window.py' ])
