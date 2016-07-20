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













# Attachment-level stuff
def get_attachment_class(attachment_child):
    # Record the type/class of attachment
    if attachment_child.has_class('thumbnail'):
        attachment_class='thumbnail'
    elif attachment_child.has_class('inline-attachment'):
        attachment_class='inline-attachment'
    elif attachment_child.has_class('file'):
        attachment_class='file'
    else:
        raise Exception('Unexpected attachment class.')
    return attachment_class


def get_attachment_dl_url(attachment_child, attachment_child_outer_html):
    # Find the url of this attachment
    if (
        ('href' not in attachment_child_outer_html) and
        ('src' not in attachment_child_outer_html) and
        ('[<div.inline-attachment>]' == repr(attachment_child))
        ):
        print('No download URL for this attachment!')
        attachment_dl_url = None# This can happen sometimes in quotes
    else:
        attachment_dl_url = re.search('"(./download/file\.php\?id=\d+(?:&amp;mode=view|&amp;sid=\w+)*)"', attachment_child_outer_html).group(1)
    return attachment_dl_url


def get_attachment_comment(attachment_child):
    # Find the comment for this attachment, if there is a comment for it
    attachment_comment = attachment_child.text()
    #print('attachment_comment: {0!r}'.format(attachment_comment))
    return attachment_comment


def get_attachment_title(attachment_child_outer_html):
    # Attachment title
    if 'title="' in attachment_child_outer_html:# Some don't have this
        attachment_title = re.search('title="([^"]*)"', attachment_child_outer_html).group(1)
    else:
        attachment_title = None
    return attachment_title


def get_attachment_alt_text(attachment_child_outer_html):
    # Find the alt text for the attachment, if there is one
    if 'alt="' in attachment_child_outer_html:# Some don't have this
        attachment_alt_text = re.search('alt="([^"]*)"', attachment_child_outer_html).group(1)
    else:
        attachment_alt_text = None
    return attachment_alt_text
# /Attachment-level stuff


def parse_attachment(attachment_child):
    """Parse one attachment
    Return the extracted information as a dict"""
    attachment = {}
    attachment_child_outer_html = attachment_child.outer_html()
    #print('attachment_child_outer_html: {0!r}'.format(attachment_child_outer_html))

    attachment['class'] = get_attachment_class(attachment_child)
    attachment['dl_url'] = get_attachment_dl_url(attachment_child, attachment_child_outer_html)
    attachment['comment'] = get_attachment_comment(attachment_child)
    attachment['title'] = get_attachment_title(attachment_child_outer_html)
    attachment['alt_text'] = get_attachment_alt_text(attachment_child_outer_html)

    return attachment


def parse_attachments(p):
    """Parse attachments for one post
    Return the extracted information as a list of dicts"""
    # Find all the attachments in the post (if any) (There can be 0, 1 2, 3,... attachments per post)
    # inline-attachment:    #p1053528 > div > div.postbody > div > div > dl > dt > img
    # attachbox:            #p2404876 > div > div.postbody > dl > dd > dl > dt > a
    # attachbox(text file): #p2467990 > div > div.postbody > dl > dd > dl > dt > a
    # #p2404876 > div > div.postbody > dl
##    attachment_path = '#p{pid} > div > div.postbody > dl > dd > dl'.format(pid=post_id)
##    attachment_path = 'div > div.postbody > dl > dd > dl'
    attachment_path = '.inline-attachment, .thumbnail, .file'
    attachment_elements = p(attachment_path)
    if attachment_elements:
        attachment_dicts = []
        for attachment_child in attachment_elements.items():
            attachment = parse_attachment(attachment_child)
            attachment_dicts.append(attachment)
            continue
        return attachment_dicts

    else:
        return None


# ========== SEPERATOR ========== #


# Post-level stuff
def get_post_title(p):
    # Get the title of the post
##    post_title_path = '#p{pid} > div > div.postbody > h3 > a'.format(pid=post_id)
    post_title_path = 'div > div.postbody h3 a'
    post_title_element = p(post_title_path)
    post_title = post_title_element.text()
    return post_title


def get_post_username(p):
    # Get the Username
##    username_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
    username_path = '.author strong'
    username_element = p(username_path)
    username = username_element.text()
    assert(len(username) >= 1)
    return username


def get_post_userid(p):
    # Get the userID
##    userid_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
    userid_path = '.author strong'
    userid_element = p(userid_path)
    userid_html = userid_element.outer_html()
    if ('href' not in userid_html):
        print('No userID for this post! post_id: {0}'.format(post_id))
        userid = None
    else:
        userid = re.search('./memberlist.php\?mode=viewprofile&amp;u=(\d+)(?:&amp;sid=\w+)?', userid_html, re.IGNORECASE|re.MULTILINE).group(1)
        assert(len(userid) >= 1)
    return userid


def get_post_time(p):
    # Get the post time
##    post_time_path = '#p{pid} > div > div.postbody > p'.format(pid=post_id)
    post_time_path = '.author'
    post_time_element = p(post_time_path)
    post_time_box = post_time_element.text()
    post_time = re.search('(\w+\s\w+\s\d+,\s\d{4}\s\d+:\d+\s\w+)', post_time_box).group(1)
    assert(len(post_time) >= 5)
    return post_time

def get_post_bodytext(p):
    # Get the post content/body/text
##    content_path = '#p{pid} > div > div.postbody > div'.format(pid=post_id)
##    content_path = 'div > div.postbody > div'
    content_path = '.content'
    content_element = p(content_path)
    content = content_element.outer_html()
    return content


def get_post_avatar_url(p):
    # Get the avatar URL
##    avatar_path = '#profile{pid} > dt > a:nth-child(1) > img'.format(pid=post_id)
    avatar_path = '[alt="User avatar"]'
    avatar_element = p(avatar_path)
    if avatar_element:
        avatar_html = avatar_element.outer_html()
        # <img src="./download/file.php?avatar=5_1350103435.jpg"
        avatar_url = re.search('<img\s(?:class="avatar"\s*)?src="([^"<>]+)', avatar_html).group(1)
        return avatar_url
    else:
        return None


def get_post_signature(p, post_id):
    # Get the signature
    signature_path = '#sig{pid}'.format(pid=post_id)
    signature_element = p(signature_path)
    signature = signature_element.outer_html()
    return signature
# /Post-level stuff


def parse_post(post_id, p):
    """Parse a single post
    Return the extracted information as a dict"""
    post = {}
    post['post_id'] = post_id
    post['time_of_retreival'] = str( time.time() )
    post['title'] = get_post_title(p)
    post['username'] = get_post_username(p)
    post['userid'] = get_post_userid(p)
    post['time'] = get_post_time(p)
    post['content'] = get_post_bodytext(p)
    post['avatar_url'] = get_post_avatar_url(p)
    post['attachments'] = parse_attachments(p)
    post['signature'] = get_post_signature(p, post_id)
    return post


# ========== SEPERATOR ========== #


# Topic level stuff
def get_topic_title(d):
    # Get the thread title
    thread_title_path = 'h2 > a'
    thread_title_element = d(thread_title_path)
    assert(thread_title_element)
    thread_title = thread_title_element.text()
    return thread_title


def get_topic_id(d):
    # Get the thread ID
    thread_id_path = 'h2 > a'
    thread_id_element = d(thread_id_path)
    thread_id_html = thread_id_element.outer_html()
    assert(thread_id_html)
    thread_id = re.search('<a\shref="./viewtopic\.php\?f=\d+&amp;t=(\d+)(?:&amp;start=\d+)?(?:&amp;sid=\w+)?">', thread_id_html).group(1)
    return thread_id


def get_board_id(d):
    # Get the board ID
    board_id_path = 'h2 > a'
    board_id_element = d(board_id_path)
    board_id_html = board_id_element.outer_html()
    assert(board_id_html)
    board_id = re.search('<a\shref="./viewtopic\.php\?f=(\d+)&amp;t=\d+(?:&amp;start=\d+)?(?:&amp;sid=\w+)?">', board_id_html).group(1)
    return board_id


def get_post_ids(d):
    # Get post IDs
    post_ids = re.findall('<div\sid="p(\d+)"\sclass="post\s(?:has-profile\s)?bg\d(?:\s*online\s*)?">', page_html)
    print('Found {0} post_ids'.format(len(post_ids)))
    print('post_ids: {0!r}'.format(post_ids))
    return post_ids
# /Topic level stuff


def parse_topic(page_html):
    """Parse a single page of posts
    return the information from the page as a dict"""
    d = PyQuery(page_html)

    # Get thread level information
    topic_dict = {}

    topic_dict['title'] = get_topic_title(d)
    topic_dict['thread_id'] = get_topic_id(d)
    topic_dict['board_id'] = get_board_id(d)

    post_ids = get_post_ids(d)

    # Get post level information
    posts = []
    # With the post IDs, we can generate paths to the items we want
    for post_id in post_ids:
        #print('post_id: {0}'.format(post_id))
        # Lock ourselves to only this one post
        post_outer_html = d('#p{pid}'.format(pid=post_id)).outer_html()
        p = PyQuery(post_outer_html)
        # Parse the post
        post = parse_post(post_id, p)
        # Store the post object away
        posts.append(post)
##        if len(posts) == 200:# DEBUG
##            break# Stop at first post for debug
        continue
    #print('posts: {0!r}'.format(posts))

    topic_dict['posts'] = posts

    print('thread: {0!r}'.format(topic_dict))
    return topic_dict


# ========== SEPERATOR ========== #








#file_path = os.path.join('debug','thread_page_response.htm')
file_path = os.path.join('debug','thread_page_response.b53.t2182.start2580.htm')
file_path = os.path.join('tests','aryion.b38.t45427.htm')
#file_path = os.path.join('tests', 'phpbb.b64.t2377101.htm')
file_path = os.path.join('tests', 'aryion.b38.t44962.htm')
file_path = os.path.join('tests', 'phpbb.b64.t2103285.htm')
file_path = os.path.join('tests', 'electricalaudio.b5.t64830.htm')
file_path = os.path.join('tests', 'aryion.b53.t2182.offset2560.htm')
##file_path = os.path.join('tests', 'phpbb.b6.t362219.offset270.htm')
##file_path = os.path.join('tests', 'phpbb.b6.t2259706.offset15.htm')
##file_path = os.path.join('tests', 'aryion.viewtopic.f38.t695.htm')

with open(file_path, 'r') as f:
    page_html = f.read()



parse_topic(page_html)







def main():
    pass

if __name__ == '__main__':
    main()
