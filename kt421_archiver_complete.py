#!/usr/bin/python3

# Code posted to /s/9M9H9E  by KiloTango421
# License: Public Domain
# I added the oauth stuff back in a generic way and found it works great!
# R.Gambrill

 
USER_AGENT='Put Name Here'
CLIENT_ID='Put Id Here'
CLIENT_SECRET='Put Secret Here'


import io
import praw
import sys
import time
 
comment_limit = None
 
def info(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
 
 
################################################################################
 
if len(sys.argv) < 3:
    raise Exception('Usage: %s USERNAME OUTPUT_FILE' % sys.argv[0])
 
redditor_name = sys.argv[1]
output_file   = sys.argv[2]

client = praw.Reddit(user_agent=USER_AGENT)
client.set_oauth_app_info(client_id = CLIENT_ID, client_secret= CLIENT_SECRET, redirect_uri="http://127.0.0.1:65010/authorize_callback")

 
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
