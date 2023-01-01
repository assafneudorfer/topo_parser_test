import random
import threading

from flask import Flask, jsonify
from topo_parser import TopologyParser, DeviceNode
import io
from contextlib import redirect_stdout
import os


# This class will help to parser file on background
class ParserThread(threading.Thread):
    def __init__(self, file_name):
        self.t_parser = TopologyParser()
        self.file_name = file_name
        super().__init__()

    def run(self):
        self.t_parser(self.file_name)


# will use as memory to track all parsed files
parser_threads = {}

app = Flask(__name__)


@app.route('/')
def index():
    return "This server help to parser topology files"


@app.route('/parser/<path:file_path>')
def parser(file_path):
    global parser_threads
    if not os.path.isfile(file_path):
        return f"file does not exsit {file_path}"

    thread_id = random.randint(0, 10000)
    parser_threads[thread_id] = ParserThread(file_path)
    parser_threads[thread_id].start()

    return jsonify(mesage="start parser", thread_id=thread_id, file_name=file_path)


@app.route('/progress/<int:thread_id>')
def parser_progress(thread_id):
    global parser_threads
    if thread_id not in parser_threads:
        return 'Id not found'
    progress_percent = parser_threads[thread_id].t_parser.progress_percent
    return jsonify(mesage=f'parsed {progress_percent}% from the file')


@app.route('/print/<int:thread_id>')
def print_topology_file(thread_id):
    global parser_threads
    if thread_id not in parser_threads:
        return 'Id not found'
    with io.StringIO() as buf, redirect_stdout(buf):
        t_parser = parser_threads[thread_id].t_parser
        t_parser.print_topology(file=buf)
        return buf.getvalue()


@app.route('/parsed')
def get_parsed_file_names():
    global parser_threads
    names = {i: t.file_name for i, t in parser_threads.items()}
    return jsonify(names)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
