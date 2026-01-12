# Topology Parser

A simple Python tool for parsing and analyzing network topology files. This project provides both a command-line interface and a Flask-based server for parsing topology files that describe network devices (switches and hosts) and their interconnections.

## Installation

First install the requirements:

```
pip install -r requirement
```

## Usage

### Basic Command Line Parser

Parse a topology file:
```bash
python topo_parser.py -f <topo_file_path> -o <output_file>
```

Print parsed topology:
```bash
python topo_parser.py -p -o <output_file>
```

Show help:
```bash
python topo_parser.py -h
```

**Options:**
- `-h --help` - Show help message
- `-f --file FILE` - Specify input topology file
- `-o --output FILE` - Output pickle file path [Default: topo_net.pickle]
- `-p --print` - Print sorted topology output


### Server Mode (Background Parsing)

For improved performance with large topology files, you can use the Flask server which supports background parsing with progress tracking.

Start the Flask server:
```bash
python parser_server.py
```

Or:
```bash
flask run -h 0.0.0.0 -p 5000
```

Then use the client to interact with the server:
```bash
python improve_parser.py -f <topo_file_path>
python improve_parser.py -p <thread_id>
python improve_parser.py --progress <thread_id>
python improve_parser.py -s
```

## Testing

Run the unit tests:
```bash
python -m pytest
```