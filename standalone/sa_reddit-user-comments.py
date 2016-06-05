#!/usr/bin/python3

# This is a script by reddit user /u/kilotango421
# Public domain
#
# A friend was having trouble adding site packages
# under windows, so I modifed this script to use
# packages bundled in the zip file it comes in.
#
# Based on an idea I found at:
# https://vilimpoc.org/blog/2012/11/23/bundling-up-distributable-python-package-libraries-using-pip-and-zip/ 
#
# Modified: Jun 4,2016 by /u/Robgambrill



import sys
if not ('packages' in sys.path):
    sys.path.insert(0, 'packages')
import io
import praw
import time

comment_limit = None

def info(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


################################################################################

if len(sys.argv) < 3:
    raise Exception('Usage: %s USERNAME OUTPUT_FILE' % sys.argv[0])

redditor_name = sys.argv[1]
output_file   = sys.argv[2]

# set up API objects
info('fetching comments by ' + redditor_name)
r = praw.Reddit(user_agent='reddit-user-comments.py')
user = r.get_redditor(redditor_name)
things = user.get_overview(limit=comment_limit)

# fetch data from Reddit
bodies = []
for thing in things:
    if isinstance(thing, praw.objects.Submission):
        thing_type = 'submission'
        body = thing.selftext
    else:
        thing_type = 'comment'
        body = thing.body

    bodies.append(': %s @ [%s](%s)***\n\n%s\n___\n' % (thing_type,
                                                       time.strftime('%Y-%m-%d %H:%M:%S UTC',
                                                                     time.gmtime(thing.created_utc)),
                                                       thing.permalink,
                                                       body.strip()))
    info('\rdownloaded %d comments' % len(bodies), end='', flush=True)
info('')

# write output file
info('writing ' + output_file)
with io.open(output_file, 'w', encoding='utf-8') as out:
    for n, body in enumerate(reversed(bodies)):
        print('___\n***#' + str(n+1) + body, file=out)

info('done!')
