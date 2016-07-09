#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     09/07/2016
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
from bs4 import BeautifulSoup


file_path = os.path.join('debug','thread_page_response.htm')
with open(file_path, 'r') as f:
    page_html = f.read()

page_soup = BeautifulSoup(page_html, "html.parser")
# Grab the posts from the page
bs_posts = page_soup.find_all(name='div', attrs='post')
# Parse each post
for bs_post in bs_posts:
    post = {}
    post_html = str(bs_post)
    post['post_html'] = post_html
    post_soup = BeautifulSoup(post_html, "html.parser")
    # Find the remote ID of the board
    board_id = re.search('<a\ href=\"./report\.php\?f\=(\d+)', post_html).group(1)
    post['board_id'] = board_id
    # Find the remote ID of the thread
    thread_id = re.search('', post_html).group(1)
    post['thread_id'] = thread_id
    # Find the remote ID of the post
    post_id = re.search('id="p(\d+)"', post_html).group(1)
    post['post_id'] = post_id

    # Find the post content field, which contains the actual post text
    post_body_soup = post_soup.find(name='div', attrs='content')
    post_body = str(post_body_soup)
    post['post_body'] = post_body

    # Seperate out the profile box next to the post
    bs_post_profile = post_soup.find(name='dl', attrs='postprofile')
    post_profile_html = str(bs_post_profile)
    post_profile_soup = BeautifulSoup(post_profile_html, "html.parser")
    # Find the username of the poster, there are severel occurances of this
    poster_username = post_profile_soup.find(name='span', attrs='username-coloured').text
    post['poster_username'] = poster_username
    # Not all posts will have this, i think user accounts can be deleted or something, removing the value?
    poster_id = re.search('/memberlist\.php\?mode=viewprofile\&amp;u=(\d+)', post_html).group(1)
    post['poster_id'] = poster_id
    avatar_url = re.search('.(/download/file\.php\?avatar=[^"])', post_profile_html).group(1)
    post['avatar_url'] = avatar_url
    print(repr(post))



def main():
    pass

if __name__ == '__main__':
    main()
