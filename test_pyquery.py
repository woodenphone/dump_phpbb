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

# Get the board ID





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

    # Find all the attachments in the post (if any)

    # Store the post object away
    posts.append(post)
    continue

thread['posts'] = posts

print('{0}'.format(thread))











def main():
    pass

if __name__ == '__main__':
    main()
