Ubuntu/Debian installation guide:

In order to solve the problem with “ImportError: cannot import name _compare_digest” please install python 2.7.9:
Download Python (recommended version: 2.7.9):

1. wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
2. tar xf Python-2.7.9.tar.xz
3. cd Python-2.7.9
4. mkdir ~/.localpython
5. ./configure --prefix=/home/<user>/.localpython
6. make
7. make install

Create virtual environment and install requirements:

1. mkvirtualenv -p ~/.localpython/bin/python2.7 petri_net --no-site-packages
2. workon petri_net
3. cd <path_to_project>/back_end/
4. pip install -r requirements.txt