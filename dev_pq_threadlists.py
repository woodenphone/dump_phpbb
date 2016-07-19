#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     14/07/2016
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



posts_per_page = 15
board_id = 6


#file_path = os.path.join('tests', 'phpbb.viewforum.f6.offset0.htm')
file_path = os.path.join('tests', 'phpbb.b64.listing.htm')
file_path = os.path.join('tests', 'aryion.viewforum.f21.htm')
file_path = os.path.join('tests', 'electricalaudio.f5.htm')
file_path = os.path.join('tests', 'arstechnica-civis.viewforum.b6.htm')

with open(file_path, 'r') as f:
    page_html = f.read()

d = PyQuery(page_html)

topics = []
rows = d('.topiclist .row')
for row in rows.items():
    topic_info = {
        'posts_per_page': posts_per_page,
        'locked': None,
        'board_id': board_id,
        'topic_id': None,
        'topic_type': None,
    }

    t = PyQuery(row.outer_html())

    # Get the link to the topic (Always exists)
    page_1_link_html = t('.topictitle').outer_html()
    topic_id = re.search(';t=(\d+)', page_1_link_html).group(1)
    topic_info['topic_id'] = topic_id

    # Get any links to subsequent pages
    page_numbers = [1]
    page_links = t('.pagination a')
    for page_link in page_links.items():
        page_link_html = page_link.outer_html()
        page_number_str = page_link.text()
        page_number = int(page_number_str)
        page_numbers.append(page_number)
##        if 'start=' in page_link_html:
##            page_offset_str = re.search('start=(\d+)', page_link_html).group(1)
##            page_offset = int(page_offset_str)
##            offsets.append(page_offset)
    last_page_number = max(page_numbers)
    topic_info['pages'] = last_page_number

    # Find if the topic is a sticky/announcement/etc
    # Global announcement detection

    # Sticky detection
    sticky_element = t('[class*=sticky]')# Match substring
    #print('sticky_element: {0!r}'.format(sticky_element))

    # Announcement detection
    # background-image: url(./styles/grey3_3_0_0/imageset/announce_read.gif); background-repeat: no-repeat;
    announce_search = re.search('/[\w_]*announce[\w_]*\.gif', row.outer_html())
    announce_element = t('[class*=announce]')# Match substring
    #print('announce_search: {0!r}'.format(announce_search))
    #print('announce_element: {0!r}'.format(announce_element))

    if sticky_element:
        topic_info['thread_type'] = 'sticky'
    elif (announce_element or announce_search):
        topic_info['thread_type'] = 'announce'
    else:
        topic_info['thread_type'] = 'normal'

    # Try to determine if topic is locked
    # Is there a class with 'locked' in the name?
    locked_element = t('[class*=locked]')# Match substring
    locked_search = re.search('/topic_\w+_locked.gif', row.outer_html())
    #print('locked_element: {0!r}'.format(locked_element))
    #print('locked_search: {0!r}'.format(locked_search))
    if (locked_element or locked_search):
        topic_info['locked'] = True
    else:
        topic_info['locked'] = False


    topics.append(topic_info)
    continue

print('topics: {0!r}'.format(topics))





def main():
    pass

if __name__ == '__main__':
    main()
