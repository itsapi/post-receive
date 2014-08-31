import os
import sys
import json
import time


def main():
    wk_path = os.getcwd()

    try:
        repo = sys.argv[1]
    except IndexError:
        repo = 'unknown repo'

    with open('options.json') as f:
        options = json.loads(f.read())

    output_dir = load_option(options, 'output')
    ignore_list = load_option(options, 'ignore')
    grunt_enabled = load_option(options, 'grunt')
    node_enabled = load_option(options, 'node')
    command = load_option(options, 'command')
    url = load_option(options, 'url')
    addr = load_option(options, 'email')

    if grunt_enabled and node_enabled:
        error(repo, addr, 'grunt and node cannot be enabled together')

    if grunt_enabled and not os.path.isdir('src'):
        print('post-receive [warning]: src directory does not exist - disabling grunt')
        grunt_enabled = False

    if grunt_enabled:
        print('post-receive: running grunt')

        if os.system('npm install'): error(repo, addr, 'npm install failed')
        if os.system('grunt --no-color'): error(repo, addr, 'grunt failed')
        wk_path += '/build'

    if output_dir:
        print('post-receive: outputting to {}'.format(output_dir))

        os.system('mkdir ' + output_dir)

        if not ignore_list: ignore_list = []
        if grunt_enabled: ignore_list += ['package.json', 'Gruntfile.js']
        ignore_list += ['options.json', 'node_modules']

        clear_dir(output_dir, ignore_list)
        move_files(wk_path, output_dir, ignore_list)

        os.chdir(output_dir)

        if node_enabled:
            print('post-receive: updating node dependencies')
            if os.system('npm install'): error(repo, addr, 'npm install failed')

        if command:
            print('post-receive: running custom command')
            if os.system(command): error(repo, addr, 'custom command failed')
    else:
        error(repo, addr, 'no output directory specified in options.json')

    print('post-receive: finished, site should now be live' +
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

    print('post-receive: removing files from ' + directory)

    patterns = [(p + '/*' if os.path.isdir(p) else p) for p in patterns]

    d = "' ! -path './"
    cmd = "find . ! -path './{}' -delete".format(d.join(patterns))
    os.system(cmd)
    os.chdir(wk_path)


def move_files(input_dir, output_dir, patterns):
    print('post-receive: copying files to ' + output_dir)

    os.system('rsync -r --exclude="{pattern}" {input}/* {out}'
        .format(
            pattern = '" --exclude="'.join(patterns),
            input = input_dir,
            out = output_dir
        )
    )


def error(repo, addr, error):
    if addr:
        subject = '{} build failed'.format(repo)
        body = ('{} failed to build correctly at {}\nError message: {}'
               .format(repo, time.strftime('%c'), error))

        p = os.popen('mail -s "{}" {}'.format(subject, ' '.join(addr)), 'w')
        p.write(body)
        p.close()

    sys.exit('post-receive [error]: '+error)


if __name__ == '__main__':
    main()
