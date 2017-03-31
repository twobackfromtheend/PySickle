import os
import sys
import subprocess as sp
from pickle import load, dump
import json
import re
from pysickle.game import Game


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)

        logPath = os.path.join(application_path, 'log.txt')

        self.log = open(logPath, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(*args):
        pass

# sys.stdout = Logger()


def parse_files(file_paths=None):
    # import input files from system.
    if file_paths is None:
        file_paths = sys.argv[1:]

    input_files_count = len(file_paths)

    # lists of [(file_name, file path)]
    replay_file_names = []
    json_file_names = []

    # find jsons and replays
    i = 0
    while i < len(file_paths):
        _file_path = file_paths[i]
        replay_match = re.search(r'(\w*.replay)$', _file_path)
        json_match = re.search(r'(\w*.json)$', _file_path)
        if replay_match:
            _file_name = replay_match.group(1)
            replay_file_names.append((_file_name, _file_path))
            i += 1
        elif json_match:
            _file_name = json_match.group(1)
            json_file_names.append((_file_name, _file_path))
            i += 1
        else:
            print('Not parsing %s ' % _file_path)
            print('Make sure file ends in .replay or .json')
            file_paths.remove(_file_path)

    if replay_file_names:
        replay_files_count = len(replay_file_names)
        print('JSONING %s/%s files with Octane.' % (replay_files_count, input_files_count))
        octane_replay_files(replay_file_names)
    if json_file_names:
        json_files_count = len(json_file_names)

        print('Parsing %s / %s files.' % (json_files_count, input_files_count))
        parse_json_files(json_file_names)


def octane_replay_files(replay_file_names):
    octanes = 0
    skipped = 0
    custom_directory = None

    replay_files_count = len(replay_file_names)

    for i in range(replay_files_count):
        _file_name, _file_path = replay_file_names[i]

        print('\nAnalysing ' + str(_file_name))
        try:
            # create directory for parsed replay files if necessary
            if custom_directory:
                directory = os.path.join(os.path.dirname(_file_path), custom_directory)
            else:
                directory = os.path.dirname(_file_path)
            os.makedirs(directory, exist_ok=True)

            # skip if .data exists
            output_file_path = os.path.join(directory, _file_name[:-7] + '.json')
            if os.path.isfile(output_file_path):
                skipped += 1
                print('Skipping file as .json exists already.')
                continue

            # set directory and write output
            os.chdir("C:\\Users\\Harry\\Documents\\Rocket League\\NEW")
            cmd = ["octane.exe", _file_path]
            print("CMD:", cmd)
            octane_data = sp.run(cmd, stdout=sp.PIPE)

            with open(output_file_path, 'wb') as f:
                f.write(octane_data.stdout)

            # tell success story
            print('Output octane success (%s).' % _file_name)
            octanes += 1

            if replay_files_count > 1:
                remaining = replay_files_count - octanes - skipped
                print('Finished file %s of %s. (%s remaining)\n' % (octanes, replay_files_count, remaining))

        except KeyError:  # need to change error to except.
            # print error message if octane fails.
            print('Could not octane ' + str(_file_name))
            print(sys.exc_info())
            print('\n')

    print('Octaned %s files.' % octanes)


def parse_json_files(json_file_names):
    pysickles = 0
    custom_directory = 'pysickle'
    json_files_count = len(json_file_names)

    for i in range(json_files_count):
        try:
            _file_name, _file_path = json_file_names[i]
            print('\nAnalysing ' + str(_file_name))

            if custom_directory:
                directory = os.path.join(os.path.dirname(_file_path), custom_directory)
            else:
                directory = os.path.dirname(_file_path)
            os.makedirs(directory, exist_ok=True)

            output_file_path = os.path.join(directory, _file_name[:-5] + '.pysickle')

            # print(_file_path)
            with open(_file_path, 'r') as f:
                replay = json.load(f)
            _pysickle = Game(replay)

            with open(output_file_path, 'wb') as f:
                dump(_pysickle, f)

            # try fix memory leak
            for player in _pysickle.players:
                del player
            del _pysickle
            Game.reset_all()

            pysickles += 1
            remaining = json_files_count - i - 1
            print('Finished file %s of %s. (%s remaining)\n' % (pysickles, json_files_count, remaining))
            print('Output written to: %s' % output_file_path)
        except UnicodeError:  # CHANGE TO KEYERROR
            print('Could not parse %s' % _file_name)
            print(sys.exc_info())
            print('\n')

    print('Pysickled %s files.' % pysickles)
