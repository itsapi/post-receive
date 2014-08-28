import os
import sys
import json

from glob import glob


def main():
    wk_path = os.getcwd()

    with open('options.json') as f:
        options = json.loads(f.read())

    output_dir = load_option(options, 'output')
    ignore_list = load_option(options, 'ignore')
    grunt_enabled = load_option(options, 'grunt')
    node_enabled = load_option(options, 'node')
    command = load_option(options, 'command')
    url = load_option(options, 'url')

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

        os.system('mkdir ' + output_dir)

        if not ignore_list:
            print('    No files to ignore')
            ignore_list = []

        ignore_list += [
            'options.json',
            'package.json',
            'Gruntfile.js'
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


def load_option(options, option_name):
    try:
        return options['hosts'][os.uname()[1]][option_name]
    except KeyError:
        pass

    try:
        return options[option_name]
    except KeyError:
        return False

def clear_dir(directory, patterns):
    wk_path = os.getcwd()
    os.chdir(directory)
    files = os.listdir()

    patterns += ['node_modules']
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
