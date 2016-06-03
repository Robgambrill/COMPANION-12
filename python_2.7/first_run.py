#! /usr/bin/python

# first_run.py - Bleep Bloop, I am an abominatio-bot 
# Run first_run.py prior to running companion-12 or your inbox will fill up!
# This should not be run as a chron job.
# Portions taken from  Chris Braun's code make_e_book.py (MIT License)
# Ver 0.2  Rob Gambrill Jun 3,2016

import ConfigParser
import webbrowser
import itertools
import operator
import os
import errno
import textwrap
import codecs
import time
from datetime import datetime

import praw


fmt = 'MHE_%Y-%m-%d_%H:%M:%S.txt'
fmt2 = '%Y-%m-%d_%H:%M:%S UCT'


Config = ConfigParser.ConfigParser()
if not (Config.read("C-12.ini")):
     print 'INI file C-1.ini Missing'
     exit()
else:
    USER_AGENT = Config.get('Credentials','USER_AGENT')
    CLIENT_ID = Config.get('Credentials','CLIENT_ID')
    CLIENT_SECRET = Config.get('Credentials','CLIENT_SECRET')
    FOLLOW_USER = Config.get('Follow','FOLLOW_USER') 
    sc_limit=int( Config.get('Posts','NUMBER_POSTS'))
    PM_TO=''


if (not USER_AGENT or not CLIENT_ID or not CLIENT_SECRET or not FOLLOW_USER):
    print 'FATAL ERROR: Missing Script Credentials!'
    print 'Please Register your script at https://www.reddit.com/prefs/apps '
    print 'and paste your script credential info into file C-12.ini'
    print ''
    print 'See the file: Creating_and_Authorizing_Reddit_Apps.txt'
    print 'for instructions.'
    exit()
else:
     client = praw.Reddit(user_agent=USER_AGENT)

print "No Personal Messages"
try:
    client.set_oauth_app_info(client_id = CLIENT_ID,
                              client_secret = CLIENT_SECRET,
                              redirect_uri="http://127.0.0.1:65010/authorize_callback")
except:
    print"FATAL"
    exit()


print 'Collecting Posts From:'
print FOLLOW_USER

r = client.get_redditor(FOLLOW_USER)


count = 0
for index, thing in enumerate(itertools.chain(r.get_comments(limit=None), r.get_submitted(limit=None)), start=1):

    count = count + 1
    text_content = getattr(thing, 'body', getattr(thing, 'selftext', None))

    text_content= thing.permalink + "  \n" + text_content

    time_temp = thing.created_utc
    file_name = datetime.utcfromtimestamp(time_temp).strftime(fmt)
    mesg_header = "COMPANION-12: Bleep, Bloop, New post detected at " + datetime.utcfromtimestamp(time_temp).strftime(fmt2)     

    try:
        file_handle = os.open(file_name, os.O_CREAT |os.O_EXCL | os.O_WRONLY,0600)
    except OSError as e:
        if e.errno == errno.EEXIST:  # Failed as the file already exists.
            print "-skipping"
            pass
        else:  # Something unexpected went wrong so reraise the exception.
            raise
    else:  # No exception, so the file must have been created successfully.
        if(PM_TO):
            client.send_message(PM_TO, mesg_header, text_content )
            print mesg_header

        print file_name
        with os.fdopen(file_handle,"w") as file_obj:
            # Using `os.fdopen` converts the handle to an object that acts like a
            # regular Python file object, and the `with` context manager means the
            # file will be automatically closed when we're done with it.
            file_obj.write(text_content.encode('ascii','replace'))


exit()

