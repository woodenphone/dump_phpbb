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



#file_path = os.path.join('tests','aryion.b38.t45427.htm')
#file_path = os.path.join('tests', 'phpbb.b64.t2377101.htm')
#file_path = os.path.join('tests', 'aryion.b38.t44962.htm')
#file_path = os.path.join('tests', 'phpbb.b64.t2103285.htm')
#file_path = os.path.join('tests', 'electricalaudio.b5.t64830.htm')
file_path = os.path.join('tests', 'phpbb.b14.t2111378.htm')

with open(file_path, 'r') as f:
    page_html = f.read()

d = PyQuery(page_html)




# Get thread level information
thread = {}

# Get the thread title
thread_title_path = 'h2 > a'
thread_title_element = d(thread_title_path)
assert(thread_title_element)
thread_title = thread_title_element.text()
thread['title'] = thread_title

# Get the thread ID
thread_id_path = 'h2 > a'
thread_id_element = d(thread_id_path)
thread_id_html = thread_id_element.outer_html()
assert(thread_id_html)
thread_id = re.search('<a\shref="./viewtopic\.php\?f=\d+&amp;t=(\d+)(?:&amp;start=\d+)?(?:&amp;sid=\w+)?">', thread_id_html).group(1)
thread['thread_id'] = thread_id

# Get the board ID
board_id_path = 'h2 > a'
board_id_element = d(board_id_path)
board_id_html = board_id_element.outer_html()
assert(board_id_html)
board_id = re.search('<a\shref="./viewtopic\.php\?f=(\d+)&amp;t=\d+(?:&amp;start=\d+)?(?:&amp;sid=\w+)?">', board_id_html).group(1)
thread['board_id'] = board_id


# Get post IDs
post_ids = re.findall('<div\sid="p(\d+)"\sclass="post\s(?:has-profile\s)?bg\d(?:\s*online\s*)?">', page_html)
print('Found {0} post_ids'.format(len(post_ids)))
print('post_ids: {0!r}'.format(post_ids))


# Check if locked
if ('title="This topic is locked, you cannot edit posts or make further replies."' in page_html):
    thread['locked'] = 1


print('thread: {0!r}'.format(thread))











def main():
    pass

if __name__ == '__main__':
    main()
