#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      User
#
# Created:     28/07/2016
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
import parse_attachment




class Post():
    # Post-level stuff
    def get_post_title(self):
        # Get the title of the post
    ##    post_title_path = '#p{pid} > div > div.postbody > h3 > a'.format(pid=post_id)
        post_title_path = 'div > div.postbody h3 a'
        post_title_element = self.p(post_title_path)
        post_title = post_title_element.text()
        return post_title

    def get_post_username(self):
        # Get the Username
    ##    username_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
        username_path = '.author strong'
        username_element = self.p(username_path)
        username = username_element.text()
        assert(len(username) >= 1)
        return username

    def get_post_userid(self):
        # Get the userID
    ##    userid_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
        userid_path = '.author strong'
        userid_element = self.p(userid_path)
        userid_html = userid_element.outer_html()
        if ('href' not in userid_html):
            #print('No userID for this post! p.outer_html(): {0!r}'.format(self.p.outer_html()))
            userid = None
        else:
            userid = re.search('./memberlist.php\?mode=viewprofile&amp;u=(\d+)(?:&amp;sid=\w+)?', userid_html, re.IGNORECASE|re.MULTILINE).group(1)
            assert(len(userid) >= 1)
        userid = int(userid)
        return userid

    def get_post_time(self):
        # Get the post time
    ##    post_time_path = '#p{pid} > div > div.postbody > p'.format(pid=post_id)
        post_time_path = '.author'
        post_time_element = self.p(post_time_path)
        post_time_box = post_time_element.text()
        post_time = re.search('(\w+\s\w+\s\d+,\s\d{4}\s\d+:\d+\s\w+)', post_time_box).group(1)
        assert(len(post_time) >= 5)
        return post_time

    def get_post_bodytext(self):
        # Get the post content/body/text
    ##    content_path = '#p{pid} > div > div.postbody > div'.format(pid=post_id)
    ##    content_path = 'div > div.postbody > div'
        content_path = '.content'
        content_element = self.p(content_path)
        content = content_element.outer_html()
        return content

    def get_post_avatar_url(self):
        # Get the avatar URL
    ##    avatar_path = '#profile{pid} > dt > a:nth-child(1) > img'.format(pid=post_id)
        avatar_path = '[alt="User avatar"]'
        avatar_element = self.p(avatar_path)
        if avatar_element:
            avatar_html = avatar_element.outer_html()
            # <img src="./download/file.php?avatar=5_1350103435.jpg"
            avatar_url = re.search('<img\s(?:class="avatar"\s*)?src="([^"<>]+)', avatar_html).group(1)
            return avatar_url
        else:
            return None

    def get_post_signature(self):
        # Get the signature
        signature_path = '#sig{pid}'.format(pid=self.post_id)
        signature_element = self.p(signature_path)
        signature = signature_element.outer_html()
        return signature
    # /Post-level stuff

##    def dedupe_attachments(self, acs):
##        for ac_a in acs:
##            parents = ac.parents()
##            for ac_b
##
##        return attachments

##    def parse_attachments(self):
##        """Parse attachments for one post
##        Return the extracted information as a list of dicts"""
##        # Find all the attachments in the post (if any) (There can be 0, 1 2, 3,... attachments per post)
##        # inline-attachment:    #p1053528 > div > div.postbody > div > div > dl > dt > img
##        # attachbox:            #p2404876 > div > div.postbody > dl > dd > dl > dt > a
##        # attachbox(text file): #p2467990 > div > div.postbody > dl > dd > dl > dt > a
##        # #p2404876 > div > div.postbody > dl
##    ##    attachment_path = '#p{pid} > div > div.postbody > dl > dd > dl'.format(pid=post_id)
##    ##    attachment_path = 'div > div.postbody > dl > dd > dl'
####        attachment_path = 'content .inline-attachment, .thumbnail, .file'
####        attachment_path = 'content .inline-attachment, content .thumbnail, content .file'
##        attachment_path = (
##            ".inline-attachment"+
##            ", .attachbox .thumbnail"+
##            ", inline-attachment .file .attach-image"
##        )
##        attachment_elements = self.p(attachment_path)
##        if attachment_elements:
##            # Process found elements
##            attachment_children = []
##            for ac in attachment_elements.items():# Store as list to allow dedupe
##                attachment_children.append(ac)
##
####            # Dedupe elements, none of the elements can be a subelement of another we have
####            for t in attachment_children:
####                if
####            print('TODO FIXME')
##
##            attachment_dicts = []
##            for attachment_child in attachment_children:# Parse each attachment
##                attachment_child_outer_html = attachment_child.outer_html()
##                attachment = Attachment()
##                attachment_dict = attachment.parse_attachment(attachment_child_outer_html)
##                attachment_dicts.append(attachment_dict)
##                continue
##            return attachment_dicts
##
##        else:
##            return None

    def parse_attachments(self):
        """Parse attachments for one post
        Return the extracted information as a list of dicts"""
        #attachments_parser = AttachmentsParser()
        #attachment_dicts = attachments_parser.parse_attachments(self.post_outer_html)
        attachment_dicts = []
        iap = parse_attachment.InlineattachmentParser()
        attachment_dicts += iap.parse_inline_attachments(post_html = self.post_outer_html)

        abp = parse_attachment.AttachboxParser()
        attachment_dicts += abp.parse_attachbox_attachments(post_html = self.post_outer_html)

        print('parse_attachments() attachment_dicts: {0!r}'.format(attachment_dicts))

        return attachment_dicts

    def parse_post(self, post_id, post_outer_html):
        """Parse a single post
        Return the extracted information as a dict"""
        self.post_outer_html = post_outer_html
        self.p = PyQuery(self.post_outer_html)
        self.post_id = post_id
        print('parse_post() post_id: {0!r}'.format(post_id))
        post = {}
        post['post_id'] = self.post_id
        post['time_of_retreival'] = str( time.time() )
        post['title'] = self.get_post_title()
        post['username'] = self.get_post_username()
        post['userid'] = self.get_post_userid()
        post['time'] = self.get_post_time()
        post['content'] = self.get_post_bodytext()
        post['avatar_url'] = self.get_post_avatar_url()
        post['attachments'] = self.parse_attachments()
        post['signature'] = self.get_post_signature()
        post['outer_html'] = post_outer_html# MAYBE REMOVE THIS? (Disk usage concern)
        return post



def main():
    pass

if __name__ == '__main__':
    main()
