### Ubuntu/Debian installation guide:

In order to solve the problem with 
>“ImportError: cannot import name _compare_digest” 

please install python 2.7.9:

```sh
$ wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
$ tar xf Python-2.7.9.tar.xz
$ cd Python-2.7.9
$ mkdir ~/.localpython
$ ./configure --prefix=/home/<user>/.localpython
$ make
$ make install
```

Create virtual environment and install requirements:

```sh
$ mkvirtualenv -p ~/.localpython/bin/python2.7 petri_net --no-site-packages
$ workon petri_net
$ cd <path_to_project>/back_end/
$ pip install -r requirements.txt
```

Run server:

```sh
$ python server.py
```