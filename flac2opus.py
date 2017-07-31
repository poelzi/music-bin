#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    print "flac2opus requires one argument: path"
    sys.exit(1)

basedir = sys.argv[1]
for root, dirs, files in os.walk(basedir):
    #cmd = 'avconv -i "{infile}" -map 0:a -codec:a \
    #    opus -b:a 48k -vbr on "{outfile}"'
    cmd = 'opusenc --bitrate 256 "{infile}" "{outfile}"'
    if '.git/' in root or root.endswith('.git'):
        continue
    print "Visiting", root
    for filename in files:
        if '.' not in filename:
            continue
        (f, ext) = filename.rsplit('.', 1)
        if ext == 'flac':
            # outdir = os.path.join("opus", root[len(basedir):])
            # try:
            #     os.makedirs(outdir)
            # except OSError, e:
            #     if e.errno != 17:
            #         raise
            outdir = root

            infile = os.path.join(root, filename)
            outfile = os.path.join(outdir, f + ".opus")
            print "Infile:   {infile}\n Outfile: {outfile}".format(
                infile=infile, outfile=outfile)
            if not os.path.exists(outfile):
                try:
                    rv = os.system(cmd.format(infile=infile, outfile=outfile))
                    if rv == 2:
                        raise KeyboardInterrupt
                    if rv != 0:
                        print "Error encoding file: %sl" %(infile)
                except KeyboardInterrupt:
                    print "Keyboard interrupt detected. Cleaning up"
                    os.unlink(outfile)
                    sys.exit(1)
