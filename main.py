import os
import sys
import json

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

    output_dir = test_opt('output')
    ignore_list = test_opt('ignore')
    grunt_enabled = test_opt('grunt')
    node_enabled = test_opt('node')
    command = test_opt('command')
    url = test_opt('url')

    if grunt_enabled and node_enabled:
        raise error('    Grunt and Node cannot be enabled together')

    if not os.path.isdir('src'): grunt_enabled = False

    if grunt_enabled:
        print('\nGrunting Stuff...')

        wk_path += '/src'
        if run_grunt(): sys.exit('Exiting because Grunt failed')
        wk_path = os.getcwd() + '/build'

    if output_dir:
        print('\nOutputting to ', output_dir)

        if not ignore_list:
            print('    No files to ignore')
            ignore_list = []

        if grunt_enabled:
            ignore_list += [
                'package.json',
                'Gruntfile.js'
            ]

        ignore_list += [
            'options.json',
            'node_modules'
        ]

        clear_dir(output_dir, ignore_list)
        move_files(wk_path, output_dir, ignore_list)

        os.chdir(output_dir)

        if node_enabled:
            print('\nUpdating node dependencies')
            os.system('npm install')

        if command:
            print('\nRunning custom command')
            os.system(command)
    else:
        print('\nNo output directory specified in options.json')

    print('\nFinished. Site should now be live' +
        (' at ' + url if url else '.'))


def load_options(filename):
    with open(filename) as f:
        options = json.loads(f.read())
    return options


def clear_dir(directory, patterns):
    wk_path = os.getcwd()
    os.chdir(directory)
    files = os.listdir()

    ignore = []
    for pattern in patterns:
        ignore += glob(pattern)

    remove = [file for file in files if file not in ignore]
    if remove:
        print('    Removing from {}: {}'.format(directory, ', '.join(remove)))
        os.system('rm -r ' + ' '.join(file for file in remove))
    else:
        print('    No files to remove from output')

    os.chdir(wk_path)


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


def run_grunt():
    os.system('npm install')
    return os.system('grunt --no-color')


if __name__ == '__main__':
    main()
