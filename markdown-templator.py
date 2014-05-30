import sys
import os
import re
import markdown as mk

jn = os.path.join


class Templator:
    def __init__(self, site_d, output_d, template_exts=()):
        self.template_exts = tuple(template_exts) + ('.html', '.htm')
        self.output_d = output_d
        self.site_d = site_d
        self.content = []
        self.templates = []

    def add(self, path):
        if jn(self.site_d, path).lower().endswith('.md'):
            self.content.append(path)
        elif jn(self.site_d, path).lower().endswith(self.template_exts):
            self.templates.append(path)

    def template(self):
        for template_f in self.templates:
            filename = jn(self.site_d, template_f)
            try:
                with open(filename) as f:
                    template = f.read()
            except:
                print('Failed to read: ' + filename)

            finished_f = re.sub(r'{{.+}}', self.match_template, template)

            # Make sure dir exists
            print(template_f)
            parts = ''
            for part in os.path.split(jn(self.output_d, template_f))[:-1]:
                parts = jn(parts, part)
                if not os.path.isdir(parts):
                    os.mkdir(parts)

            with open(jn(self.output_d, template_f), 'w') as f:
                f.write(finished_f)

    def match_template(self, template_match):
        template = template_match.group()[2:-2]
        try:
            content_f = [filename for filename in self.content if filename.endswith(template + '.md')][0]
            found = True
        except IndexError:
            print('Couldn\'t find markdown file: ' + template)
            return template_match.group()

        if found:
            with open(jn(self.site_d, content_f)) as f:
                content = f.read()
            return mk.markdown(content, extensions=['attr_list'])


def main():
    try:
        site_d = sys.argv[1]
        output_d = sys.argv[2]
    except IndexError:
        sys.exit('Usage: python main.py site_dir output_dir')
    for f in (site_d, output_d):
        if not os.path.isdir(f):
            sys.exit('Not a directory: ' + f)

    tmpltr = Templator(site_d, output_d)
    explore(site_d, tmpltr.add)
    tmpltr.template()


def explore(initial, func, path=[]):
    abs_path = jn(*([initial] + path))
    for file_ in os.listdir(abs_path):
        abs_f_path = jn(abs_path, file_)
        f_path = path + [file_]

        if os.path.isdir(abs_f_path):
            explore(initial, func, f_path)

        elif os.path.isfile(abs_f_path):
            func(jn(*f_path))


if __name__ == '__main__':
    main()
