from topo_parser import TopologyParser, DeviceNode
import os
import time
import io
from contextlib import redirect_stdout

t_parser = TopologyParser()


def test_default_parser():
    global t_parser
    file_path = 'topo_files/small_topo_file'
    output_file = 'topo_net.pickle'
    if os.path.exists(output_file):
        os.remove(output_file)
    t_parser(file_path)
    t_parser.save_parser_net()
    assert os.path.exists(output_file)


def test_load_function():
    # wait some time for generate the pickle file
    time.sleep(1)
    pickle_path = 'topo_net.pickle'
    t_parser = TopologyParser.load_parser_net(pickle_path)
    assert isinstance(t_parser, TopologyParser)


def test_default_print():
    # wait some time for generate the pickle file
    time.sleep(1)
    global t_parser
    with io.StringIO() as buf, redirect_stdout(buf):
        t_parser.print_topology(file=buf)
        with open('example_output.txt', 'r') as f:
            assert f.read() == buf.getvalue()


def test_d_node_add_connected_device():
    d_node = DeviceNode()
    buf = io.StringIO(
        '[1](ec0d9a03007d7d0a) 	"S-b8599f0300fc6de4"[23]		# lid 9 lmc 0 "MF0;r-ufm-sw95:MQM8700/U1" lid 13 4xEDR')
    line = buf.getvalue().split()
    d_node.add_connected_device(line)
    assert d_node.connected_device == [['Switch', 'b8599f0300fc6de4', 23]]
    d_node = DeviceNode()
    buf = io.StringIO('[3]	"H-e41d2d03005cf34c"[1](e41d2d03005cf34c) 		# "r-dmz-ufm128 HCA-1" lid 3 4xFDR')
    line = buf.getvalue().split()
    d_node.add_connected_device(line)
    assert [['Host', 'e41d2d03005cf34c', 1]]
