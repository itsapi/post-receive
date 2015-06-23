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

    options = json.load(open('options.json'))

    build_cmd = load_option(options, 'build_cmd')
    copy_from = load_option(options, 'copy_from')
    copy_to = load_option(options, 'copy_to')
    start_cmd = load_option(options, 'start_cmd')
    ignore = load_option(options, 'ignore')
    url = load_option(options, 'url')
    email = load_option(options, 'email')

    if build_cmd: run_commands(build_cmd)

    if copy_to:
        os.system('mkdir ' + copy_to)

        if not ignore: ignore = []
        ignore += ['options.json', 'node_modules']

        if copy_from: wk_path = os.path.join(wk_path, copy_from)

        clear_dir(copy_to, ignore)
        move_files(wk_path, copy_to, ignore)
        os.chdir(copy_to)

        if start_cmd: run_commands(start_cmd)

    else:
        error(name, email, 'no output directory specified in options.json')

    log('finished')
    if (url): log('site should now be live at ' + url)


def log(string):
    print('post-receive:', string)


def load_option(options, option_name):
    try:
        return options['hosts'][os.uname()[1]][option_name]
    except KeyError:
        return options.get(option_name)


def run_commands(commands):
    for cmd in commands:
        log('running "{}"'.format(cmd))
        if os.system(cmd): error(name, email, '{} failed'.format(cmd))


def clear_dir(directory, patterns):
    wk_path = os.getcwd()
    os.chdir(directory)

    log('removing files from ' + directory)
    patterns = [(p + '/*' if os.path.isdir(p) else p) for p in patterns]

    d = "' ! -path './"
    cmd = "find . ! -path './{}' -delete".format(d.join(patterns))
    os.system(cmd)
    os.chdir(wk_path)


def move_files(input_dir, copy_to, patterns):
    log('copying files to ' + copy_to)
    os.system('rsync -r --exclude="{pattern}" {input}/. {out}'
        .format(
            pattern = '" --exclude="'.join(patterns),
            input = input_dir,
            out = copy_to
        )
    )


def error(name, email, error):
    if email:
        subject = '{} build failed'.format(name)
        body = ('{} failed to build correctly at {}\nError message: {}'
               .format(name, time.strftime('%c'), error))

        p = os.popen('mail -s "{}" {}'.format(subject, ' '.join(email)), 'w')
        p.write(body)
        p.close()

    sys.exit('post-receive [error]: '+error)


if __name__ == '__main__':
    main()
