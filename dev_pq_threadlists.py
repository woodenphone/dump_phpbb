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


file_path = os.path.join('tests', 'phpbb.viewforum.f6.offset0.htm')

with open(file_path, 'r') as f:
    page_html = f.read()

d = PyQuery(page_html)

topics = []
rows = d('.topiclist .row')
for row in rows.items():
    topic_info = {'posts_per_page': posts_per_page}
    t = PyQuery(row.outer_html())

    # Get the link to the topic (Always exists)
    page_1_link_html = t('.topictitle').outer_html()
    topic_id = re.search(';t=(\d+)', page_1_link_html).group(1)
    topic_info['board_id'] = board_id
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
    topics.append(topic_info)
    continue








def main():
    pass

if __name__ == '__main__':
    main()
