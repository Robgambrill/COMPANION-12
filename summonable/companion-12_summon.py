#! /usr/bin/python3

# Companion-12.py - Bleep Bloop, I am an abominatio-bot 
# This bot responds to mentions of its name in comments.
# Reply's with latest post of _9MOTHER9HORSE9EYES9
#
# Requires user permission to run. Add Access and Refresh Tokens
# to ini file.
# 
# Portions taken from  Chris Braun's code make_e_book.py (MIT License)
# Ver 0.2  Rob Gambrill May 31,2016

import configparser
import itertools
import operator
import io
import os
import re
import errno
import textwrap
import codecs
import time
from datetime import datetime
from pprint import pprint

import praw


fmt = 'MHE_%Y-%m-%d_%H:%M:%S.txt'
fmt2 = '%Y-%m-%d_%H:%M:%S UCT'


Config = configparser.ConfigParser()
if not (Config.read("C-12.ini")):
     print ('INI file C-1.ini Missing')
     exit()
else:
    USER_AGENT = Config.get('Credentials','USER_AGENT')
    CLIENT_ID = Config.get('Credentials','CLIENT_ID')
    CLIENT_SECRET = Config.get('Credentials','CLIENT_SECRET')
    PM_TO = Config.get('Recipient','PM_TO')
    ACCESS_TOKEN = Config.get('Tokens','ACCESS_TOKEN')
    REFRESH_TOKEN = Config.get('Tokens','REFRESH_TOKEN')
    FOLLOW_USER = Config.get('Follow','FOLLOW_USER') 
    sc_limit=int( Config.get('Posts','NUMBER_POSTS'))


if (not USER_AGENT or not CLIENT_ID or not CLIENT_SECRET or not FOLLOW_USER):
    print ('FATAL ERROR: Missing Script Credentials!')
    print ('Please Register your script at https://www.reddit.com/prefs/apps ')
    print ('and paste your script credential info into file C-12.ini')
    print ('')
    print ('See the file: Creating_and_Authorizing_Reddit_Apps.txt')
    print ('for instructions.')
    exit()
else:
     client = praw.Reddit(user_agent=USER_AGENT)

if (not ACCESS_TOKEN or not REFRESH_TOKEN):
    print("FATAL:Required Tokens not in C-12.ini")
    exit()
else:        
    from prawoauth2 import PrawOAuth2Mini
    scopes =['identity','history','privatemessages', 'submit', 'read']
    oauth_helper = PrawOAuth2Mini(client,app_key = CLIENT_ID, 
                              app_secret = CLIENT_SECRET,
                              access_token = ACCESS_TOKEN,
                              refresh_token = REFRESH_TOKEN,
                              scopes=scopes)

    
if not os.path.isfile("posts_replied_to.txt"):
     posts_replied_to = []
else:
     with open("posts_replied_to.txt", "r") as f:
       posts_replied_to = f.read()
       posts_replied_to = posts_replied_to.split("\n")
       posts_replied_to = filter(None, posts_replied_to)
       posts_replied_to = list (posts_replied_to)
   
mentions = list (client.get_mentions(limit=None));

for mention in mentions:
     mid =mention.id
     perm = mention.permalink
     if mid not in posts_replied_to:
          posts_replied_to.append(mid)
          r = client.get_redditor(FOLLOW_USER)

          for index, thing in enumerate(itertools.chain( r.get_submitted(limit=1)), start=1):
               last_submission= thing.permalink
               s_time=thing.created_utc
          for index, thing in enumerate(itertools.chain( r.get_comments(limit=1)), start=1):
               last_comment= thing.permalink
               c_time=thing.created_utc
          postbody= "COMPANION-12: Bleep, Bloop, I am an Abominatio-Bot!  \n  Most Recent Post of _9MOTHER9HORSE9EYES9  \n  \n"

          if s_time > c_time:
               postbody= postbody + "At " +  datetime.utcfromtimestamp(s_time).strftime(fmt2) +" The Author Submitted:  \n" + last_submission + "  \n"
              
          if c_time > s_time: 
               postbody= postbody + "At " + datetime.utcfromtimestamp(c_time).strftime(fmt2) +" The Author Commented:  \n" + last_comment + "  \n" 
         
          postbody = re.sub(r"www.reddit.com","np.reddit.com", postbody)     
          postbody= postbody + "\n  [*All beings of flesh can interface here....*](https://www.reddit.com/r/9M9H9E9/)  \n"
          print(postbody)
          mention.reply(postbody)
          mention.mark_as_read()  

print  ("Run Complete!")        
print  (posts_replied_to)
with open("posts_replied_to.txt", "w") as f:
     for post_id in posts_replied_to:
          f.write(post_id + "\n") 

exit()
