#!/usr/bin/env python

import os
import sys
import mutagen
from subprocess import check_output

# lookup list of possible tags
TAGS = set()
ptags = check_output(['tageditor', '--print-field-names']).splitlines()[0:3]
for line in ptags:
    for tag in line.split():
        TAGS.add(tag)

print TAGS

import argparse

parser = argparse.ArgumentParser(description='Fill in missing tags')
parser.add_argument('root', metavar='root', nargs='+',
                    help='file or directory')
parser.add_argument('-n', dest='noop', action='store_true',
                    help='just simulate')

for tag in TAGS:
    parser.add_argument('--%s' % tag, dest=tag)

args = parser.parse_args()
print(args)


#import mutagen
def fix_file(args, fname):
    todo = []
    for tag in TAGS:
        if getattr(args, tag):
            out = check_output(['tageditor', '-e', '-n', tag, '-f', fname])
            #if mutagen.File(fname)['TPE1'].encoding == mutagen.id3.Encoding.UTF16:
            #    print "broken"
            #    out = False

            if not out:
                todo += ['-n', u"%s=%s" %(tag, unicode(getattr(args, tag)))]
    if todo:
        cmd=['tageditor', '-s', '--id3v2-version=4', '--encoding=utf8'] + todo + ['-f', fname]
        if args.noop:
            print "would run: %s" %cmd
        else:
            print "run: %s" %cmd
            check_output(cmd)



for base in args.root:
    if os.path.isfile(base):
        fix_file(args, base)
    else:
        for root, dirs, files in os.walk(base):
            if '.git/' in root:
                continue
            print "Visiting", root
            for filename in files:
                if '.' not in filename:
                    continue
                (f, ext) = filename.rsplit('.', 1)
                if ext not in ['flac', 'opus', 'mp3', 'ogg', 'mp4']:
                    continue

                infile = os.path.join(root, filename)
                fix_file(args, infile)

#
#
# basedir = sys.argv[1]
# for root, dirs, files in os.walk(basedir):
#     #cmd = 'avconv -i "{infile}" -map 0:a -codec:a \
#     #    opus -b:a 48k -vbr on "{outfile}"'
#     # cmd = 'opusenc --bitrate 256 "{infile}" "{outfile}"'
#     if '.git/' in root:
#         continue
#     print "Visiting", root
#     for filename in files:
#         if '.' not in filename:
#             continue
#         (f, ext) = filename.rsplit('.', 1)
#         if ext not in ['flac', 'opus', 'mp3', 'ogg', 'mp4']:
#             continue
#
#         # outdir = os.path.join("opus", root[len(basedir):])
#         # try:
#         #     os.makedirs(outdir)
#         # except OSError, e:
#         #     if e.errno != 17:
#         #         raise
#         outdir = root
#
#         infile = os.path.join(root, filename)
#         # outfile = os.path.join(outdir, f + ".opus")
#         print "Infile:   {infile}\n".format(
#             infile=infile)
