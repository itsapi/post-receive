import json
import sys
import os
from glob import glob

import replace_keys as rk


def main():
    wk_path = os.getcwd()

    options = load_options('options.json')

    def test_opt(option_name):
        try:
            opt = options[option_name]
        except KeyError:
            return False
        return opt

    if test_opt('replace-keys'):
        print('\nReplacing Keys...')
        rk.replace(wk_path, '/home/pi/data.json')

    if test_opt('grunt'):
        print('\nGrunting Stuff...')
        grunt()

    output_dir = test_opt('output')
    ignore_list = test_opt('ignore')

    if output_dir:
        print('\nOutputting to ', output_dir)

        if not ignore_list:
            print('    No files to ignore')
            ignore_list = []
        ignore_list.append('options.json')

        clear_dir(output_dir, ignore_list)
        move_files(wk_path, output_dir, ignore_list)

    else:
        print('\nNo output directory specified in options.json')


def load_options(filename):
    with open(filename) as f:
        options = json.loads(f.read())
    return options


def clear_dir(directory, patterns):
    files = os.listdir(directory)

    ignore = []
    for pattern in patterns:
        ignore += glob(pattern)

    remove = [file for file in files if file not in ignore]
    if remove:
        print('    Removing from {}: {}'.format(directory, ', '.join(remove)))
        os.system('rm -r ' + ' '.join(os.path.join(directory, file) for file in remove))
    else:
        print('    No files to remove from output')


def move_files(input_dir, output_dir, patterns):
    files = os.listdir(input_dir)
    os.system('rsync -r --exclude="{pattern}" {input}/* {out}'
        .format(
            pattern = '" --exclude="'.join(patterns),
            input = input_dir,
            out = output_dir
        )
    )
    print('    Moving files from {} to {}'.format(input_dir, output_dir))

def grunt():
    os.system('npm install > /dev/null')
    os.system('grunt')

if __name__ == '__main__':
    main()
