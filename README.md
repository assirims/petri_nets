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

### Microsoft Windows installation guide:

1. Download .msi file from https://www.python.org/downloads/release/python-279/ and install Python 2.7.9
2. Edit PATH system variable - add paths to Python and Python\Script, e.g. "C:\Python27;C:\Python27\Scripts"
3. Download Visual C++ Compiler for Python 2.7 from http://www.microsoft.com/en-us/download/details.aspx?id=44266
	(downloaded file included in sources)
4. Run command prompt and go to project directory: "cd <path_to_project>/back_end/"
5. Type and run "pip install -r requirements.txt"
6. Run the server "python server.py"

NOTE: If point 5 does not succed try following commands:
"pip install --upgrade setuptools" or "easy_install -U setuptools"