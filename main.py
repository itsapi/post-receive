#!/usr/bin/env python3

import os
import sys
import json
import time


def main():
    arg = 1
    try: wk_path = sys.argv[arg]; arg += 1
    except IndexError: wk_path = os.getcwd()
    try: name = sys.argv[arg]; arg += 1
    except IndexError: name = wk_path

    os.chdir(wk_path)

    with open('options.json') as f:
        options = json.loads(f.read())

    output_dir = load_option(options, 'output')
    build_dir = load_option(options, 'build_dir')
    ignore_list = load_option(options, 'ignore')
    build_cmd = load_option(options, 'build_cmd')
    grunt_enabled = load_option(options, 'grunt')
    node_enabled = load_option(options, 'node')
    command = load_option(options, 'command')
    url = load_option(options, 'url')
    addr = load_option(options, 'email')

    if grunt_enabled:
        print('post-receive: grunt option is deprecated - use build_cmd instead')
        build_cmd = 'grunt'

    if build_cmd:
        print('post-receive: running {}'.format(build_cmd))
        if os.system('npm install'): error(name, addr, 'npm install failed')
        if os.system(build_cmd): error(name, addr, '{} failed'.format(build_cmd))

    if output_dir:
        print('post-receive: outputting to {}'.format(output_dir))
        os.system('mkdir ' + output_dir)

        if not ignore_list: ignore_list = []
        ignore_list += ['options.json', 'node_modules']

        if build_dir: wk_path = os.path.join(wk_path, build_dir)

        clear_dir(output_dir, ignore_list)
        move_files(wk_path, output_dir, ignore_list)
        os.chdir(output_dir)

        if node_enabled:
            print('post-receive: updating node dependencies')
            if os.system('npm install'): error(name, addr, 'npm install failed')

        if command:
            print('post-receive: running custom command')
            if os.system(command): error(name, addr, 'custom command failed')
    else:
        error(name, addr, 'no output directory specified in options.json')

    print('post-receive: finished')
    if (url):
        print('post-receive: site should now be live at ' + url)


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

    print('post-receive: removing files from ' + directory)
    patterns = [(p + '/*' if os.path.isdir(p) else p) for p in patterns]

    d = "' ! -path './"
    cmd = "find . ! -path './{}' -delete".format(d.join(patterns))
    os.system(cmd)
    os.chdir(wk_path)


def move_files(input_dir, output_dir, patterns):
    print('post-receive: copying files to ' + output_dir)
    os.system('rsync -r --exclude="{pattern}" {input}/. {out}'
        .format(
            pattern = '" --exclude="'.join(patterns),
            input = input_dir,
            out = output_dir
        )
    )


def error(name, addr, error):
    if addr:
        subject = '{} build failed'.format(name)
        body = ('{} failed to build correctly at {}\nError message: {}'
               .format(name, time.strftime('%c'), error))

        p = os.popen('mail -s "{}" {}'.format(subject, ' '.join(addr)), 'w')
        p.write(body)
        p.close()

    sys.exit('post-receive [error]: '+error)


if __name__ == '__main__':
    main()
