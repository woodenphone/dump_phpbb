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
posts = []
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
    #thread_id = re.search('', post_html).group(1)
    #post['thread_id'] = thread_id

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

    # Some posts don't have avatars
    avatar_url_search = re.search('.(/download/file\.php\?avatar=[^"])', post_profile_html)
    if avatar_url_search:
        avatar_url = avatar_url_search.group(1)
    else:
        avatar_url = None
    post['avatar_url'] = avatar_url

    bs_post_author = post_soup.find(name='p', attrs='author')
    post_author_html = str(bs_post_author)
    # Find the post time
    post_time = re.search('(\w+\s\w+\s\d+,\s\d{4}\s\d+:\d+\s\w+)', post_author_html).group(1)
    post['post_time'] = post_time

    # Post signature
    bs_post_signature = post_soup.find(name='div', attrs='signature')
    post_signature = str(bs_post_signature)
    post['post_signature'] = post_signature

    # post_subject
    # <h3><a href="#p2371872">Re: Eka Chat</a></h3>
    #post_subject = re.search('<h3><[^<>]+>([^<>]+)<[^<>]+></h3>', post_html, re.IGNORECASE|re.MULTILINE).group(1)

    print(post)
    posts.append(post)
    continue

print(posts)

thread = {}
#thread['topic_id'] =
#thread['time_of_retreival'] = str(time.time())
thread['posts'] = posts

# This sort of thread-level stuff might be better to grab from the boards thread listing page instead
# Find thread level status things
thread_lock_search = page_soup.find_all(name='div', attrs='locked-icon')
thread_locked = bool(thread_lock_search)



def main():
    pass

if __name__ == '__main__':
    main()
