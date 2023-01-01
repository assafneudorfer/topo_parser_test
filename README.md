# Topology Parser

### This is my solution for the home task:

First install the requirement:

```
pip install -r requirement
```

Topo_parser commands:

```
python topo_parser.py -f <topo_file_path> -o (optional)
python topp_parser.py -p -o (optional)
python topo_parser.py -h
```
Usage:
topo_parser.py [-f FILE -o FILE] 
topo_parser.py [-p -o FILE]  
topo_parser.py -h | --help  

-h --help    show this  
-f --file FILE      specify output file  
-o --output FILE     output pickle file path [Default: topo_net.pickle]  
-p --print  sorted output
  
To run the improve topo_parser run the flask server before.  

```
flask run -h 0.0.0.0 -p 5000
```

And use improve_parser.py like topo_parser.py


To run unitest:
```
python -m pytest
```