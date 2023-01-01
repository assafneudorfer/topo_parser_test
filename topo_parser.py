"""
Usage:
topo_parser.py [-f FILE -o FILE]
topo_parser.py [-p -o FILE]
topo_parser.py -h | --help

-h --help    show this
-f --file FILE      specify output file
-o --output FILE     output pickle file path [Default: topo_net.pickle]
-p --print  sorted output


"""

from docopt import docopt
from collections import OrderedDict
import pickle
import os
import logging

PERCENT = [25, 50, 75, 100]

logging.basicConfig()
logger = logging.getLogger('topo_parser')
logger.setLevel(logging.INFO)


def get_guid_value(guid, d_guid):
    hex_key = hex(int(d_guid, 16))
    # caguid without parenthesis
    return hex_key if guid == 'caguid' else f'{hex_key}({str(hex_key)[2:]})'


def update_progress(file_name, percent):
    p = int(percent)
    if p in PERCENT:
        logger.info(f"parsed {PERCENT[PERCENT.index(p)]}% from file {file_name}")
        PERCENT.remove(PERCENT[0])


class DeviceNode:

    def __init__(self):
        self.sys_guid = None
        self.guid = None
        self.type = None
        self.port_id = None
        self.connected_device = []

    def add_connected_device(self, line):
        line = line[1].split('"')
        d_type, d_guid = line[1].split('-')

        # for host line the port number will contain [port](port_id)
        port, d_type = (eval(line[2])[0], 'Switch') if d_type == 'S' else (eval(line[2][:3])[0], 'Host')

        self.connected_device += [[d_type, d_guid, port]]


class TopologyParser:

    def __init__(self):
        self.progress_percent = 0
        # Print the devices in order of connectivity
        self.topology = OrderedDict()

    def __call__(self, t_file):
        file_size = os.path.getsize(t_file)
        with open(t_file, 'r') as f:
            # flag for track if we handle switch or host block
            in_block = False
            d_node = None
            progress = 0
            for line in f:
                # update progress
                progress = progress + len(line)
                self.progress_percent = (100 * progress) / file_size
                update_progress(t_file, self.progress_percent)

                line = line.strip()
                if line.startswith('sysimgguid'):
                    # new block
                    d_node = DeviceNode()
                    in_block = True
                    d_node.sys_guid = line.split("=")[1]
                elif line.startswith('switchguid') or line.startswith('caguid'):
                    # update type and guid
                    d_node.type = 'Switch' if line.startswith('switchguid') else 'Host'
                    d_node.guid = line.split("=")[1]

                    # insert new node for the net
                    self.topology[d_node.guid] = d_node
                elif line.startswith('Switch') or line.startswith('Ca'):
                    # not relevant information for the task
                    continue
                elif len(line) == 0 or line.isspace():
                    # finish with the block
                    in_block = False
                    d_node = None
                elif in_block:
                    # handle connected_devices
                    line = line.split()
                    d_node.add_connected_device(line)
        logger.info('Finish to parser file')

    def save_parser_net(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_parser_net(file_path='topo_net.pickle'):
        with open(file_path, 'rb') as f:
            parsed_net = pickle.load(f)
        return parsed_net

    def print_topology(self, file=None):
        for key, d_node in self.topology.items():
            print(f'{d_node.type}: sysimgguid={d_node.sys_guid}', file=file)
            if d_node.type == 'Switch':
                print(f'switchguid:= {d_node.guid}', file=file)
            else:
                print(f'Port_id:= {d_node.guid.replace("0x", "")}', file=file)
            for device in d_node.connected_device:
                d_type, d_guid, d_port = device
                guid_type = 'switchguid' if d_type == 'Switch' else 'caguid'
                print(
                    f'\tConnected to {d_guid.lower()}: {guid_type}={get_guid_value(guid_type, d_guid)}, port={d_port}',
                    file=file)
            print("\n", file=file)


def main():
    args = docopt(__doc__)
    file_path = args['--file']
    to_print = args['--print']
    output_file = args['--output']
    try:
        if file_path:
            t_parser = TopologyParser()
            t_parser(file_path)
            t_parser.save_parser_net(output_file)
        elif to_print:
            t_parser = TopologyParser.load_parser_net(output_file)
            t_parser.print_topology()
    except FileNotFoundError:
        print('File not exists')
        print('Make you enter valid input or run python topo_parser.py -f <topo_file> first')


if __name__ == '__main__':
    main()
