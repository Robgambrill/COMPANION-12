# Companion-12.py - Bleep Bloop, I am an abominatio-bot 
# Run as a chron job
# Portions taken from Cryse-'s code E_book.py (MIT License)
# Rob Gambrill May 31,2016

import itertools
import operator
import os
import errno
import textwrap
import codecs
import time
from datetime import datetime


import praw

# Name of Author to watch
USERNAME = '_9MOTHER9HORSE9EYES9'

# Follow API guidelines: https://github.com/reddit/reddit/wiki/API#rules
# Get App Credentials: https://www.reddit.com/prefs/apps
# Then take the info and edit these lines below.

USER_AGENT = 'your_scipt_id'
CLIENT_ID = 'your_client_id'
CLIENT_SECRET='your_client_secret'
# Account you want to send post notifications to
EMAIL_TO = 'some_reddit_user
'
fmt = 'MHE_%Y-%m-%d_%H:%M:%S.txt'
fmt2 = '%Y-%m-%d_%H:%M:%S UCT'



def main():
    parts = {}

    client = praw.Reddit(user_agent=USER_AGENT)
    client.set_oauth_app_info(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri="http://127.0.0.1:65010/authorize_callback")
            
    
    r = client.get_redditor(USERNAME)
    count = 0
    for index, thing in enumerate(itertools.chain(r.get_comments(limit=None), r.get_submitted(limit=None)), start=1):
      
        count = count + 1
        content = getattr(thing, 'body_html', getattr(thing, 'selftext_html', None))
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
            client.send_message(EMAIL_TO, mesg_header, text_content )
            print mesg_header 
            print file_name
            with os.fdopen(file_handle,"w") as file_obj:
                # Using `os.fdopen` converts the handle to an object that acts like a
                # regular Python file object, and the `with` context manager means the
                # file will be automatically closed when we're done with it.
                file_obj.write(text_content.encode('ascii','replace'))
               



if __name__ == '__main__':
    main()
