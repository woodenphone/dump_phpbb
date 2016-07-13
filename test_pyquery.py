#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     11/07/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# stdlib
import logging
import logging.handlers
import time
import datetime
import os
import random
import argparse
import sys
import re
# libs
import requests
from pyquery import PyQuery
#from io import StringIO, BytesIO
#from lxml import etree
#from bs4 import BeautifulSoup


file_path = os.path.join('debug','thread_page_response.htm')
file_path = os.path.join('debug','thread_page_response.b53.t2182.start2580.htm')
with open(file_path, 'r') as f:
    page_html = f.read()

d = PyQuery(page_html)




# Get thread level information
thread = {}

# Get the thread title
thread_title_path = '#page-body > h2 > a'
thread_title_element = d(thread_title_path)
thread_title = thread_title_element.text()
thread['title'] = thread_title

# Get the thread ID
thread_id_path = '#page-body > h2 > a'
thread_id_element = d(thread_id_path)
thread_id_html = thread_id_element.outer_html()
thread_id = re.search('<a\shref="./viewtopic\.php\?f=\d+&amp;t=(\d+)(?:&amp;start=\d+)">', thread_id_html).group(1)
thread['thread_id'] = thread_id

# Get the board ID
board_id_path = '#page-body > h2 > a'
board_id_element = d(board_id_path)
board_id_html = board_id_element.outer_html()
board_id = re.search('<a\shref="./viewtopic\.php\?f=(\d+)&amp;t=\d+(?:&amp;start=\d+)">', board_id_html).group(1)
thread['board_id'] = board_id




# Get post IDs
post_ids = re.findall('<div\sid="p(\d+)"\sclass="post\sbg\d">', page_html)

# Get post level information
posts = []
# With the post IDs, we can generate paths to the items we want
for post_id in post_ids:
    post = {
        'post_id': post_id,
        'time_of_retreival': str( time.time() ),
    }

    # Get the title of the post
    post_title_path = '#p{pid} > div > div.postbody > h3 > a'.format(pid=post_id)
    post_title_element = d(post_title_path)
    post_title = post_title_element.text()
    post['title'] = post_title

    # Get the Username
    username_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
    username_element = d(username_path)
    username = username_element.text()
    post['username'] = username

    # Get the userID
    userid_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
    userid_element = d(userid_path)
    userid_html = userid_element.outer_html()
    userid = re.search('memberlist.php\?mode=viewprofile&amp;u=(\d+)', userid_html).group(1)
    post['userid'] = userid

    # Get the post time
    post_time_path = '#p{pid} > div > div.postbody > p'.format(pid=post_id)
    post_time_element = d(post_time_path)
    post_time_box = post_time_element.text()
    post_time = re.search('(\w+\s\w+\s\d+,\s\d{4}\s\d+:\d+\s\w+)', post_time_box).group(1)
    post['time'] = post_time

    # Get the post content/body/text
    content_path = '#p{pid} > div > div.postbody > div'.format(pid=post_id)
    content_element = d(content_path)
    content = content_element.outer_html()
    post['content'] = content

    # Get the avatar URL
    avatar_path = '#profile{pid} > dt > a:nth-child(1) > img'.format(pid=post_id)
    avatar_element = d(avatar_path)
    if avatar_element:
        avatar_html = avatar_element.outer_html()
        # <img src="./download/file.php?avatar=5_1350103435.jpg"
        avatar_url = re.search('<img\ssrc=".(/download/file.php\?avatar=[\w\d_\.]+)', avatar_html).group(1)
        post['avatar_url'] = avatar_url
    else:
        post['avatar_url'] = None

    # Find all the attachments in the post (if any) (There can be 0, 1 2, 3,... attachments per post)
    # inline-attachment:    #p1053528 > div > div.postbody > div > div > dl > dt > img
    # attachbox:            #p2404876 > div > div.postbody > dl > dd > dl > dt > a
    # attachbox(text file): #p2467990 > div > div.postbody > dl > dd > dl > dt > a
    # #p2404876 > div > div.postbody > dl
    attachment_path = '#p{pid} > div > div.postbody > dl > dd > dl > dt > a'.format(pid=post_id)
    attachment_elements = d(attachment_path)
    if attachment_elements:
        attachments = []
        for attachment_child in attachment_elements.items():
            attachment = {}
            # Find the url of this attachment
            #attachment_url = attachment_child.attrib['href'][1:]#None#TODO FIXME
            #attachment['url'] = attachment_url

            # Find the comment for this attachment, if there is a comment for it
            attachment_comment = None#TODO FIXME
            attachment['comment'] = attachment_comment

            # Find the filename for the attachment, if there is one next to it
            attachment_filename = None#TODO FIXME
            attachment['attachment_filename'] = attachment_filename

            attachments.append(attachment)
            continue
    else:
        attachments = None
    post['attachments'] = attachments


    # Get the signature
    signature_path = '#sig{pid}'.format(pid=post_id)
    signature_element = d(signature_path)
    signature = signature_element.outer_html()
    post['signature'] = signature


    # Store the post object away
    posts.append(post)
    if len(posts) == 2:# DEBUG
        break# Stop at first post for debug
    continue

thread['posts'] = posts

print('thread: {0!r}'.format(thread))











def main():
    pass

if __name__ == '__main__':
    main()
