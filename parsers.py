#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     13/07/2016
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
from pyquery import PyQuery





##class TopicParser():# TODO
##    """Parser for whole topics"""
##    def __init__(self, board_id, topic_id):
##        self.topic = {}
##        return
##
##    def ParsePage(self, page_html, offset):
##        """Parse a single page from the topic and add the results to the internal thread object"""
##        return {}
##
##    def GetThreadObj(self):
##        return self.topic
##
##
##
##
##class PostParser():# TODO
##    """Parser for individual posts"""
##    user_id = None
##
##    def __init__(self, topic_page_html, post_id):
##        self.topic_page_html = topic_page_html
##        self.post_id = post_id
##        # Parse the post
##        self.post_userid = self.find_userid()
##        return
##
##    def ParsePost(self, post_obj):
##        """TODO"""
##        raise Exception('TODO: impliment these things')
##
##
##
##    def find_userid(self):
##        userid_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
##        userid_element = d(userid_path)
##        userid_html = userid_element.outer_html()
##        userid = re.search('memberlist.php\?mode=viewprofile&amp;u=(\d+)', userid_html).group(1)
##        return userid







def parse_thread_page(page_html, board_id, topic_id, offset):
    """Parse a page of posts"""
    d = PyQuery(page_html)
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
            avatar_url = re.search('<img\ssrc="(./download/file.php\?avatar=[\w\d_\.]+)', avatar_html).group(1)
            post['avatar_url'] = avatar_url
        else:
            post['avatar_url'] = None

        # Find all the attachments in the post (if any) (There can be 0, 1 2, 3,... attachments per post)
        # inline-attachment:    #p1053528 > div > div.postbody > div > div > dl > dt > img
        # attachbox:            #p2404876 > div > div.postbody > dl > dd > dl > dt > a
        # attachbox(text file): #p2467990 > div > div.postbody > dl > dd > dl > dt > a
        # #p2404876 > div > div.postbody > dl
        attachment_path = '#p{pid} > div > div.postbody > dl > dd > dl'.format(pid=post_id)
        attachment_elements = d(attachment_path)
        if attachment_elements:
            post_attachments = []
            for attachment_child in attachment_elements.items():
                attachment = {}
                attachment_child_outer_html = attachment_child.outer_html()
                #print('attachment_child_outer_html: {0!r}'.format(attachment_child_outer_html))

                # Find the url of this attachment
                attachment_dl_url = re.search('<a\s(?:class="postlink"\s)?href="(./download/file\.php\?id=\d+(?:&amp;mode=view)?)">', attachment_child_outer_html).group(1)
                attachment['dl_url'] = attachment_dl_url

                # Find the comment for this attachment, if there is a comment for it
                attachment_comment = attachment_child.text()
                #print('attachment_comment: {0!r}'.format(attachment_comment))
                attachment['comment'] = attachment_comment

                # Attachment title
                #attachment_title = re.search('title="([^"]+)"', attachment_child_outer_html).group(1)
                #attachment['title'] = attachment_title


                # Find the filename for the attachment, if there is one next to it
                #attachment_filename = None#TODO FIXME
                #attachment['attachment_filename'] = attachment_filename

                post_attachments.append(attachment)
                continue
        else:
            post_attachments = None
        post['attachments'] = post_attachments


        # Get the signature
        signature_path = '#sig{pid}'.format(pid=post_id)
        signature_element = d(signature_path)
        signature = signature_element.outer_html()
        post['signature'] = signature


        # Store the post object away
        posts.append(post)
        if len(posts) == 200:# DEBUG
            break# Stop at first post for debug
        continue
    return posts





def main():
    pass

if __name__ == '__main__':
    main()
