import pysickle.inout as io
import os
import sys


def choose_file():
    file_list = os.listdir(os.getcwd())
    print('Which file would you like to analyse?')

    # print files in current directory
    i = 1
    for x in file_list:
        print('%s: %s' % (i, x))
        i += 1

    # ask for input file number until no error
    _cont = False
    while _cont is False:
        try:
            file_number = int(input('Input file number')) - 1
            file_name = file_list[file_number]
            _cont = True
        except Exception as e:
            print(e)
            print('Could not choose file. Try again.')
    print('Analysing ' + file_name)

    file_path = os.path.join(os.getcwd(), file_name)
    return file_path

file_path = sys.argv[1:]
if file_path is None:
    file_path = (choose_file(), )
    io.parse_files(file_path)

else:
    io.parse_files()

# sys.stdout = sys.__stdout__
input('Press enter to continue...')
