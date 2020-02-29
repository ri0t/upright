#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Upright - A sourcecode copyright maintenance tool

Application
===========

See README.rst for Build/Installation and setup details.

URLs & Contact
==============

Mail: riot@c-base.org

Project repository: http://github.com/ri0t/upright

"""

import os
import re
import json
from datetime import datetime
from pprint import pprint, pformat

import click
import pystache
from click_didyoumean import DYMGroup

__author__ = "Heiko 'riot' Weinen <riot@c-base.org>"
__copyright__ = "Copyright (C) Heiko 'riot' Weinen"
__license__ = "GPLv3, see LICENSE"

CATEGORIES = [
    'shebang',
    'docstring',
    'empty',
    'hash',
    'unknown',
    'imports',
    'broken',
    'comment',
    'outdated'
]


def header(filename, n):
    result = ""

    with open(filename, "r") as f:
        for _ in range(n):
            result += f.readline()

    return result


@click.group(cls=DYMGroup)
@click.option("--folder", default=".", type=click.Path(exists=True),
              help="Specify a folder to operate on")
@click.option('--file', '-f', help='Only act on specific file', default=None)
@click.option('--file-type', '-t', default=".py", help="Specify file type to act on")
@click.option('--file-category', '-c', default='all',
              type=click.Choice(CATEGORIES + ['all']),
              help='Select only a specified file classification')
@click.option('--write', '-w', help='Actually write changes to files',
              default=False, is_flag=True)
@click.option('--dump', '-d', help='Dump changes to console',
              default=False, is_flag=True)
@click.option('--debug', help='Enable debugging output', default=False,
              is_flag=True)
@click.option('--ignore', '-i', multiple=True)
@click.option('--years', '-y', default=5, type=int,
              help="Check this many years back for obsolete copyright ends")
@click.option("--line", "-l", default=20,
              help="Inspect and replace only up until given line number")
@click.pass_context
def cli(ctx, folder, file, file_type, file_category, write, dump, debug, ignore,
        years, line):
    """Upright - a sourcecode copyright maintenance tool"""

    ctx.obj['folder'] = folder
    ctx.obj['file_type'] = file_category
    ctx.obj['write'] = write
    ctx.obj['dump'] = dump
    ctx.obj['debug'] = debug
    ctx.obj['line'] = line

    all_types, copyright, total = analyse(ctx, folder, ignore, file_type, years, line)

    ctx.obj['total'] = total

    if file_category == 'all':
        types = all_types
    else:
        try:
            types = {file_category: all_types[file_category]}
        except KeyError:
            print(all_types.keys())

    if file is not None:
        for key, group in types.items():
            new_group = []

            for item in group:
                if item == file:
                    new_group.append(item)

            types[key] = new_group

    if debug:
        click.secho("Files:\n" + pformat(types), fg="red")

    ctx.obj['file_lists'] = types
    ctx.obj['copyright'] = copyright


@cli.command()
@click.pass_context
def stats(ctx):
    """Generate various statistics about source files"""

    counters = ctx.obj['file_lists']
    total = ctx.obj['total']

    if ctx.obj['debug']:
        pprint(counters)
    copyright = ctx.obj['copyright']
    copyright_stats = {}
    copyright_total = 0
    for name, stuff in counters.items():
        copyright_stats[name] = len(stuff)

        for file_name in stuff:
            if file_name in copyright:
                copyright_stats[name] -= 1
            else:
                copyright_total += 1

    for counter, file_list in sorted(counters.items()):
        color = 'green' if copyright_stats[counter] == 0 else 'yellow'
        click.secho("%10s : %4i (%4i without copyright)" % \
                    (counter,
                     len(file_list),
                     copyright_stats[counter]
                     ), fg=color)

    color = 'green' if copyright_total == 0 else 'yellow'
    click.secho("%10s : %4i (%4i without copyright)" % \
                ("total",
                 len(total),
                 copyright_total
                 ), fg=color)


@cli.command()
@click.pass_context
def lists(ctx):
    """Generate lists of source files by classification"""

    counters = ctx.obj['file_lists']
    copyright = ctx.obj['copyright']
    for counter, file_list in sorted(counters.items()):
        click.secho("=" * 34 + " %9s " % counter + "=" * 34, fg='cyan')
        for item in sorted(file_list):
            color = "green" if item in copyright else "red"
            click.secho(item, fg=color)


def print_filename(filename, color='white'):
    click.secho('{:*^79}'.format(" " + str(filename)[-50:] + " "),
                fg=color)


@cli.command()
@click.option("--faulty", "-f", is_flag=True, default=False,
              help="Show only files with missing copyright")
@click.pass_context
def headers(ctx, faulty):
    """Show headers of source files by classification"""

    copyright = ctx.obj['copyright']
    counters = ctx.obj['file_lists']

    def print_headers(counter, data, copyright=[]):
        click.secho("=" * 34 + " %9s " % (counter) + "=" * 34, fg='cyan')

        for filename in sorted(data):
            if filename in copyright:
                if faulty:
                    continue
                color = 'green'
            else:
                color = 'yellow'
            print_filename(filename, color)
            print(header(filename, 10))

    for counter, file_list in sorted(counters.items()):
        print_headers(counter, file_list, copyright)


@cli.group('remove')
@click.pass_context
def remove(ctx):
    pass


@remove.command()
@click.argument('txt')
@click.pass_context
def startswith(ctx, txt):
    click.secho('Removing ' + str(txt))
    file_lists = ctx.obj['file_lists']

    for files in sorted(file_lists.values()):
        for item in sorted(files):
            print_filename(item, color='magenta')
            output = ""
            with open(item, "r") as input_file:
                for i, input_line in enumerate(input_file):
                    if not input_line.startswith(txt):
                        output += input_line
                        if ctx.obj['dump']:
                            click.secho(input_line.rstrip('\n'), fg="green")
                    elif ctx.obj['dump']:
                        click.secho(input_line.rstrip('\n'), fg="red")

            if ctx.obj['write']:
                with open(item, "w") as output_file:
                    output_file.write(output)


@remove.command()
@click.pass_context
def comment(ctx):
    file_lists = ctx.obj['file_lists']

    for files in sorted(file_lists.values()):
        for item in sorted(files):
            print_filename(item, color='magenta')
            output = ""
            comment = True
            with open(item, "r") as input_file:
                for i, input_line in enumerate(input_file):
                    if not comment or (not input_line.startswith("#") and
                                       not input_line.isspace()):
                        output += input_line
                        comment = False
                        if ctx.obj['dump']:
                            click.secho(input_line.rstrip('\n'), fg="green")
                    elif ctx.obj['dump']:
                        click.secho(input_line.rstrip('\n'), fg="red")

            if ctx.obj['write']:
                with open(item, "w") as output_file:
                    output_file.write(output)


@cli.command("update")
@click.option("--year-from", "-yf", default=None, help="Update only this year")
@click.option("--year-to", "-yt", default=None, help="Update to this year")
@click.pass_context
def update(ctx, year_from, year_to):
    """Update a copyright year.
    If you do not specify year-from or year-to, only last year's number will
    be updated to the current one."""

    line = ctx.obj['line']
    file_lists = ctx.obj['file_lists']

    year_now = datetime.now().year
    year_previous = year_now - 1

    if year_from is None:
        year_from = year_previous
    if year_to is None:
        year_to = year_now

    year_from = str(year_from)
    year_to = str(year_to)

    modified = 0
    all_files = 0

    for files in sorted(file_lists.values()):
        for item in sorted(files):
            print_filename(item, color='magenta')
            all_files += 1
            changed = False

            with open(item, "r") as input_file:
                content = input_file.read().split("\n")

            for no, old_line in enumerate(content[:line]):
                new_line = old_line.replace(year_from, year_to)
                if new_line != old_line:
                    changed = True
                    modified += 1
                    if ctx.obj["debug"]:
                        click.secho(old_line + "->" + new_line, fg="red")
                content[no] = new_line

            if ctx.obj["write"] and changed:
                with open(item, "w") as output_file:
                    if ctx.obj["debug"]:
                        click.secho("Writing file:", )
                    output_file.write("\n".join(content))

            if ctx.obj["debug"] and changed:
                click.secho("\n".join(content[:line]), fg="yellow")

    click.secho("All files: %i Modified files: %i" % (all_files, modified), fg="red")


@cli.group("template")
@click.option('--template-file', '-t', help='Use specified template file',
              default=None)
@click.option('--settings-file', '-s', help='Use specified field data file',
              default=None)
@click.pass_context
def template_group(ctx, template_file, settings_file):
    """Handle template operations (GROUP)"""

    if settings_file is not None:
        print(settings_file)
        settings_file = os.path.normpath(os.path.expanduser(settings_file))

        with open(settings_file, "r") as f:
            settings = json.load(f)
    else:
        settings = {}

    print(settings)
    template_file = settings.get("template", "copyright.tpl") if \
        template_file is None else template_file

    print(template_file)
    if template_file.startswith('./'):
        if 'template' in settings:
            template_file = template_file.replace('./', os.path.dirname(settings_file) + "/")
        else:
            template_file = template_file.replace('./', os.getcwd() + "/")

    print(template_file)
    template_file = os.path.normpath(template_file)

    print(template_file)

    with open(template_file, "r") as f:
        ctx.obj['template'] = f.read()

    if settings['copyright_end'] is False:
        settings['copyright_end'] = datetime.now().year

    ctx.obj['settings'] = settings

    if ctx.obj['debug']:
        click.secho(pformat(ctx.obj['template']), fg='green')
        click.secho(pformat(settings), fg='cyan')


@template_group.command("insert")
@click.option('--line', '-l', help='Insert on specified line number',
              default=0)
@click.pass_context
def insert(ctx, line):
    """Insert a template somewhere"""
    template = ctx.obj['template']
    settings = ctx.obj['settings']
    file_lists = ctx.obj['file_lists']

    copyright_text = pystache.render(template, settings)

    if ctx.obj['debug']:
        click.secho(str(copyright_text), fg='magenta')

    for files in sorted(file_lists.values()):
        for item in sorted(files):
            print_filename(item, color='magenta')
            output = ""
            with open(item, "r") as input_file:
                for i, input_line in enumerate(input_file):
                    if i == line:
                        output += copyright_text
                    output += input_line

            if ctx.obj['dump']:
                click.secho(output, fg="cyan")
            if ctx.obj['write']:
                with open(item, "w") as output_file:
                    output_file.write(output)


cli.add_command(template_group)


def analyse(ctx, folder, ignore, file_type=".py", years=5, line=20):
    """Collect statistics and classify source code files"""

    file_lists = {}

    for item in CATEGORIES:
        file_lists[item] = []

    total = []
    copyright = []

    year_now = datetime.now().year

    old_years = [str(x) for x in range(year_now - years, year_now)]

    def is_ignored(_filename):

        for term in ignore:
            if re.search(term, _filename):
                if ctx.obj["debug"]:
                    print('IGNORED:', _filename, term)
                return True

        # print('NOT IGNORED:', file)
        return False

    def _check_year(text):

        for year in old_years:
            text_header = "\n".join(text.split("\n")[:line])
            if year in text_header:
                return True
        return False

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(folder):
        path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            if is_ignored(os.path.join(root, file)):
                continue

            if file.endswith(file_type):
                # print(len(path) * '---', file)
                filename = os.path.join("/".join(path), file)
                # print(path, file)

                with open(filename, "r") as f:
                    try:
                        content = f.read()
                    except Exception as e:
                        click.secho("Could not handle file:" + filename + str(e), fg="red")
                        file_lists['broken'].append(filename)
                        continue
                    # print(content)

                    if re.search("copyright", content, re.IGNORECASE):
                        copyright.append(filename)
                    if _check_year(content):
                        file_lists['outdated'].append(filename)

                    if content.startswith('"""'):
                        file_lists['docstring'].append(filename)
                    elif content.startswith('import') or \
                            content.startswith('from'):
                        file_lists['imports'].append(filename)
                    elif content.startswith('#!/'):
                        file_lists['shebang'].append(filename)
                    elif content == "" or content.isspace():
                        file_lists['empty'].append(filename)
                    elif content.startswith('#'):
                        file_lists['hash'].append(filename)
                    elif content.startswith('/*'):
                        file_lists['comment'].append(filename)
                    else:
                        file_lists['unknown'].append(filename)

                total.append(filename)

    #print(file_lists)
    return file_lists, copyright, total


if __name__ == "__main__":
    cli(obj={})
