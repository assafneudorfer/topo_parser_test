"""
Usage:
server_parser.py [-f FILE]
server_parser.py [-p id]
server_parser.py [--progress id]
server_parser.py [-s]
server_parser.py -h | --help


-h --help    show this
-f --file FILE      specify output file
--progress id  show the parser progress on file
-p --print id  sorted output
-s --show      show all parsed file names


"""

from docopt import docopt
from topo_parser import TopologyParser, DeviceNode
import requests
import subprocess

URL = 'http://127.0.0.1:5000'


# Simple function that run the parsed process on background
# Decided not to use in my solution
def improve_parser():
    args = docopt(__doc__)
    file_path = args['--file']
    to_print = args['--print']
    t_parser = TopologyParser()
    if file_path:
        subprocess.Popen(["python", "topo_parser.py", "-f", file_path])
    elif to_print:
        t_parser.topology = TopologyParser.load_parser_net()
        t_parser.print_topology()


# Client function that work similar to topo_parser.py
def client_main():
    args = docopt(__doc__)
    file_path = args['--file']
    to_print = args['--print']
    # more options
    id_progress = args['--progress']
    to_show = args['--show']
    if file_path:
        res = requests.get(f'{URL}/parser/{file_path}')
        print(res.content.decode('utf-8'))
    elif to_print:
        res = requests.get(f'{URL}/print/{to_print}')
        print(res.content.decode("utf-8"))
    elif id_progress:
        res = requests.get(f'{URL}/progress/{id_progress}')
        print(res.content.decode("utf-8"))
    elif to_show:
        res = requests.get(f'{URL}/parsed')
        print(res.content.decode("utf-8"))


if __name__ == '__main__':
    client_main()
