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
# Local
import parse_viewtopic



# from dev_pq_threadlists.py
def viewforum_detect_if_locked(post_query_obj):
    locked_element = post_query_obj('[class*=locked]')# Match substring
    locked_search = re.search('/topic_\w+_locked.gif', post_query_obj.outer_html())
    return (locked_element or locked_search)


def viewforum_detect_if_globalannounce(post_query_obj):
    globalannounce_element = post_query_obj('[class*=global-announce]')# Match substring
    return bool(globalannounce_element)


def viewforum_detect_if_announce(post_query_obj):
    announce_search = re.search('/[\w_]*announce[\w_]*\.gif', post_query_obj.outer_html())
    announce_element = post_query_obj('[class*=announce]')# Match substring
    return (announce_search or announce_element)


def viewforum_detect_if_sticky(post_query_obj):
    sticky_element = post_query_obj('[class*=sticky]')# Match substring
    return bool(sticky_element)


def viewforum_detect_if_locked(post_query_obj):
    locked_element = post_query_obj('[class*=locked]')# Match substring
    locked_img_search = re.search('/topic_\w+_locked.gif', post_query_obj.outer_html())
    locked_message_element = post_query_obj('[title*="This topic is locked, you cannot edit posts or make further replies."]')# Match substring
    return (locked_element or locked_img_search or locked_message_element)


def parse_threads_listing_page(html, board_id, posts_per_page):
    """Extract data about threads from the board thread list page
    Return a list of dicts for each thread listed on the page
    Things this needs to extract:
        topic ID
        ?Number of pages?
        Locked status
        Topic type
    """

    d = PyQuery(html)

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
        topic_info['topic_id'] = int(topic_id)

        # Get any links to subsequent pages
        page_numbers = [1]
        page_links = t('.pagination a')
        for page_link in page_links.items():
            page_link_html = page_link.outer_html()
            page_number_str = page_link.text()
            page_number = int(page_number_str)
            page_numbers.append(page_number)
        last_page_number = max(page_numbers)
        topic_info['pages'] = last_page_number

        # Find if the topic is a sticky/announcement/etc
        if viewforum_detect_if_globalannounce(post_query_obj=t):
            topic_info['thread_type'] = 'global-announce'
        elif viewforum_detect_if_announce(post_query_obj=t):
            topic_info['thread_type'] = 'announce'
        elif viewforum_detect_if_sticky(post_query_obj=t):
            topic_info['thread_type'] = 'sticky'
        else:
            topic_info['thread_type'] = 'normal'

        # Try to determine if topic is locked
        if viewforum_detect_if_locked(post_query_obj=t):
            topic_info['locked'] = True
        else:
            topic_info['locked'] = False


        topics.append(topic_info)
        continue
    #print('topics: {0!r}'.format(topics))
    return topics
# /from dev_pq_threadlists.py






def parse_thread_level_items(page_one_html, board_id, thread_id):
    """Parse out information that is more thread-level than post-level.
    ex. Thread name, reported number of pages,
    Return a dict of these values."""
    # Values we were given can be dropped in as-is.
    thread['board_id'] = board_id
    thread['thread_id'] = thread_id

    # Get the thread title
    thread_title_path = 'h2 > a'
    thread_title_element = d(thread_title_path)
    assert(thread_title_element)
    thread_title = thread_title_element.text()
    thread['title'] = thread_title



    # Check if locked
    if ('title="This topic is locked, you cannot edit posts or make further replies."' in page_html):
        thread['locked'] = True
    else:
        thread['locked'] = False

    return thread




def parse_thread_page(page_html, board_id, topic_id, offset):
    """Parse a page of posts.
    Return a list of dicts, each dict being the values for a single post."""

    return parse_viewtopic.parse_thread_page(page_html, board_id, topic_id, offset)
##
##
##    d = PyQuery(page_html)
##
##    # Get post IDs
##    post_ids = re.findall('<div\sid="p(\d+)"\sclass="post\s(?:has-profile\s)?bg\d(?:\s*online\s*)?">', page_html)
##    print('Found {0} post_ids'.format(len(post_ids)))
##    print('post_ids: {0!r}'.format(post_ids))
##
##    # Get post level information
##    posts = []
##    # With the post IDs, we can generate paths to the items we want
##    for post_id in post_ids:
##        print('post_id: {0}'.format(post_id))
##        post = {
##            'post_id': post_id,
##            'time_of_retreival': str( time.time() ),
##        }
##        # Lock ourselves to only this one post
##        post_outer_html = d('#p{pid}'.format(pid=post_id)).outer_html()
##        p = PyQuery(post_outer_html)
##        # Get the title of the post
##    ##    post_title_path = '#p{pid} > div > div.postbody > h3 > a'.format(pid=post_id)
##        post_title_path = 'div > div.postbody h3 a'
##        post_title_element = p(post_title_path)
##        post_title = post_title_element.text()
##        post['title'] = post_title
##
##        # Get the Username
##    ##    username_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
##        username_path = '.author strong'
##        username_element = p(username_path)
##        username = username_element.text()
##        assert(len(username) >= 1)
##        post['username'] = username
##
##        # Get the userID
##    ##    userid_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
##        userid_path = '.author strong'
##        userid_element = p(userid_path)
##        userid_html = userid_element.outer_html()
##        if ('href' not in userid_html):
##            print('No userID for this post! post_id: {0}'.format(post_id))
##            userid = None
##        else:
##            userid = re.search('./memberlist.php\?mode=viewprofile&amp;u=(\d+)(?:&amp;sid=\w+)?', userid_html, re.IGNORECASE|re.MULTILINE).group(1)
##            assert(len(userid) >= 1)
##        post['userid'] = userid
##
##        # Get the post time
##    ##    post_time_path = '#p{pid} > div > div.postbody > p'.format(pid=post_id)
##        post_time_path = '.author'
##        post_time_element = p(post_time_path)
##        post_time_box = post_time_element.text()
##        post_time = re.search('(\w+\s\w+\s\d+,\s\d{4}\s\d+:\d+\s\w+)', post_time_box).group(1)
##        assert(len(post_time) >= 5)
##        post['time'] = post_time
##
##        # Get the post content/body/text
##    ##    content_path = '#p{pid} > div > div.postbody > div'.format(pid=post_id)
##    ##    content_path = 'div > div.postbody > div'
##        content_path = '.content'
##        content_element = p(content_path)
##        content = content_element.outer_html()
##        post['content'] = content
##
##        # Get the avatar URL
##    ##    avatar_path = '#profile{pid} > dt > a:nth-child(1) > img'.format(pid=post_id)
##        avatar_path = '[alt="User avatar"]'
##        avatar_element = p(avatar_path)
##        if avatar_element:
##            avatar_html = avatar_element.outer_html()
##            # <img src="./download/file.php?avatar=5_1350103435.jpg"
##            avatar_url = re.search('<img\s(?:class="avatar"\s*)?src="([^"<>]+)', avatar_html).group(1)
##            post['avatar_url'] = avatar_url
##        else:
##            post['avatar_url'] = None
##
##        # Find all the attachments in the post (if any) (There can be 0, 1 2, 3,... attachments per post)
##        # inline-attachment:    #p1053528 > div > div.postbody > div > div > dl > dt > img
##        # attachbox:            #p2404876 > div > div.postbody > dl > dd > dl > dt > a
##        # attachbox(text file): #p2467990 > div > div.postbody > dl > dd > dl > dt > a
##        # #p2404876 > div > div.postbody > dl
##    ##    attachment_path = '#p{pid} > div > div.postbody > dl > dd > dl'.format(pid=post_id)
##    ##    attachment_path = 'div > div.postbody > dl > dd > dl'
##        attachment_path = '.inline-attachment, .thumbnail, .file'
##        attachment_elements = p(attachment_path)
##        if attachment_elements:
##            post_attachments = []
##            for attachment_child in attachment_elements.items():
##                attachment = {}
##                attachment_child_outer_html = attachment_child.outer_html()
##                #print('attachment_child_outer_html: {0!r}'.format(attachment_child_outer_html))
##
##
##                # Record the type/class of attachment
##                if attachment_child.has_class('thumbnail'):
##                    attachment_class='thumbnail'
##                elif attachment_child.has_class('inline-attachment'):
##                    attachment_class='inline-attachment'
##                elif attachment_child.has_class('file'):
##                    attachment_class='file'
##                else:
##                    raise Exception('Unexpected attachment class.')
##                attachment['class'] = attachment_class
##
##                # Find the url of this attachment
##                if (
##                    ('href' not in attachment_child_outer_html) and
##                    ('src' not in attachment_child_outer_html) and
##                    ('[<div.inline-attachment>]' == repr(attachment_child))
##                    ):
##                    print('No download URL for this attachment!')
##                    attachment_dl_url = None# This can happen sometimes in quotes
##                else:
##                    attachment_dl_url = re.search('"(./download/file\.php\?id=\d+(?:&amp;mode=view|&amp;sid=\w+)*)"', attachment_child_outer_html).group(1)
##                attachment['dl_url'] = attachment_dl_url
##
##                # Find the comment for this attachment, if there is a comment for it
##                attachment_comment = attachment_child.text()
##                #print('attachment_comment: {0!r}'.format(attachment_comment))
##                attachment['comment'] = attachment_comment
##
##                # Attachment title
##                if 'title="' in attachment_child_outer_html:# Some don't have this
##                    attachment_title = re.search('title="([^"]*)"', attachment_child_outer_html).group(1)
##                else:
##                    attachment_title = None
##                attachment['title'] = attachment_title
##
##                # Find the alt text for the attachment, if there is one
##                if 'alt="' in attachment_child_outer_html:# Some don't have this
##                    attachment_alt_text = re.search('alt="([^"]*)"', attachment_child_outer_html).group(1)
##                else:
##                    attachment_alt_text = None
##                attachment['alt_text'] = attachment_alt_text
##
##                post_attachments.append(attachment)
##                continue
##        else:
##            post_attachments = None
##        post['attachments'] = post_attachments
##
##        # Get the signature
##        signature_path = '#sig{pid}'.format(pid=post_id)
##        signature_element = p(signature_path)
##        signature = signature_element.outer_html()
##        post['signature'] = signature
##
##
##        # Store the post object away
##        posts.append(post)
##    ##    if len(posts) == 200:# DEBUG
##    ##        break# Stop at first post for debug
##        continue
##    #print('posts: {0!r}'.format(posts))
##    return posts





def main():
    pass

if __name__ == '__main__':
    main()
