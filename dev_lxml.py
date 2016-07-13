#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     10/07/2016
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
from io import StringIO, BytesIO
from lxml import etree
#from bs4 import BeautifulSoup


file_path = os.path.join('debug','thread_page_response.htm')
with open(file_path, 'r') as f:
    page_html = f.read()

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




    # Store the post object away
    posts.append(post)
    if len(posts) == 2:# DEBUG
        break# Stop at first post for debug
    continue





def main():
    pass

if __name__ == '__main__':
    main()
