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
# Local
import parse_post




class Topic():
    # Topic level stuff
    def get_topic_title(self):
        # Get the thread title
        thread_title_path = 'h2 > a'
        thread_title_element = self.d(thread_title_path)
        assert(thread_title_element)
        thread_title = thread_title_element.text()
        return thread_title

    def get_topic_id(self):
        # Get the thread ID
        thread_id_path = 'h2 > a'
        #print('get_topic_id() self.d: {0!r}'.format(self.d))
        thread_id_element = self.d(thread_id_path)
        thread_id_html = thread_id_element.outer_html()
        assert(thread_id_html)
        thread_id = re.search('<a\shref="./viewtopic\.php\?f=\d+&amp;t=(\d+)(?:&amp;start=\d+)?(?:&amp;sid=\w+)?">', thread_id_html).group(1)
        return thread_id

    def get_board_id(self):
        # Get the board ID
        board_id_path = 'h2 > a'
        board_id_element = self.d(board_id_path)
        board_id_html = board_id_element.outer_html()
        assert(board_id_html)
        board_id = re.search('<a\shref="./viewtopic\.php\?f=(\d+)&amp;t=\d+(?:&amp;start=\d+)?(?:&amp;sid=\w+)?">', board_id_html).group(1)
        return board_id

    def get_post_ids(self):
        # Get post IDs
        post_ids = re.findall('<div\sid="p(\d+)"\sclass="post\s(?:has-profile\s)?bg\d(?:\s*online\s*)?">', self.page_html)
        #print('Found {0} post_ids'.format(len(post_ids)))
        #print('post_ids: {0!r}'.format(post_ids))
        return post_ids
    # /Topic level stuff

    def parse_topic(self, page_html, board_id=None, topic_id=None, offset=None):
        """Parse a single page of posts
        return the information from the page as a dict"""
        self.page_html = page_html
        self.board_id = board_id
        self.topic_id = topic_id
        self.offset = offset

        self.d = PyQuery(self.page_html)

##        # Get thread level information
##        topic_dict = {}
##
##        topic_dict['title'] = self.get_topic_title()
##        topic_dict['thread_id'] = self.get_topic_id()
##        topic_dict['board_id'] = self.get_board_id()

        post_ids = self.get_post_ids()

        # Get post level information
        posts = []
        # With the post IDs, we can generate paths to the items we want
        for post_id in post_ids:
            #print('post_id: {0}'.format(post_id))
            # Lock ourselves to only this one post
            post_outer_html = self.d('#p{pid}'.format(pid=post_id)).outer_html()

            # Parse the post
            post = parse_post.Post()
            post_dict = post.parse_post(post_id, post_outer_html)
            # Store the post object away
            posts.append(post_dict)
    ##        if len(posts) == 200:# DEBUG
    ##            break# Stop at first post for debug
            continue
        #print('posts: {0!r}'.format(posts))

        #topic_dict['posts'] = posts

        #print('thread: {0!r}'.format(topic_dict))
        return posts


def parse_thread_page(page_html, board_id, topic_id, offset):
    """Parse a page of posts.
    Return a list of dicts, each dict being the values for a single post."""

    #return parse_viewtopic.parse_topic(page_html)


    topic = Topic()
    posts = topic.parse_topic(page_html)
    return posts


def main():
    pass

if __name__ == '__main__':
    main()
    # Test and debug stuff
    #file_path = os.path.join('debug','thread_page_response.htm')
    file_path = os.path.join('debug','thread_page_response.b53.t2182.start2580.htm')
    file_path = os.path.join('tests','aryion.b38.t45427.htm')
    #file_path = os.path.join('tests', 'phpbb.b64.t2377101.htm')
    file_path = os.path.join('tests', 'aryion.b38.t44962.htm')
    file_path = os.path.join('tests', 'phpbb.b64.t2103285.htm')
    file_path = os.path.join('tests', 'electricalaudio.b5.t64830.htm')
    file_path = os.path.join('tests', 'aryion.b53.t2182.offset2560.htm')
    ##file_path = os.path.join('tests', 'phpbb.b6.t362219.offset270.htm')
    file_path = os.path.join('tests', 'aryion.viewtopic.f38.t695.htm')
    #file_path = os.path.join('tests', 'phpbb.b6.t362219.offset270.htm')
    #file_path = os.path.join('tests', 'aryion.viewtopic.f38.t695.htm')
    #file_path = os.path.join('tests', 'phpbb.b6.t362219.offset270.htm')
    #file_path = os.path.join('tests', 'cichlid-forum.viewtopic.f4.t246181.htm')
    #file_path = os.path.join('tests', 'phpbb.b6.t2259706.offset15.htm')
    #file_path = os.path.join('tests', 'aryion.viewtopic.f55.t11882.offset30.htm')# has swf attachment
    #file_path = os.path.join('tests', 'aryion.viewtopic.f79.t17592.htm')# has swf attachment



    with open(file_path, 'r') as f:
        page_html = f.read()


    topic = Topic()
    result = topic.parse_topic(page_html)
    print('result: {0!r}'.format(result))