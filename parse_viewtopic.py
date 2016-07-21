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






##class AttachmentParser():
##    """
##    https://github.com/phpbb/phpbb/blob/3.1.x/phpBB/styles/prosilver/template/attachment.html
##    """
##    def parse_attachment(self, attachment_html):
##        """Parse one attachment
##        Return the extracted information as a dict"""
##        self.attachment_html = attachment_html
##        self.a = PyQuery(attachment_html)
##        #print('attachment_html: {0!r}'.format(attachment_html))
##
##        attachment = {}
##        attachment['class'] = self.get_attachment_class()
##        attachment['dl_url'] = self.get_attachment_dl_url()
##        attachment['comment'] = self.get_attachment_comment()
##        attachment['title'] = self.get_attachment_title()
##        attachment['alt_text'] = self.get_attachment_alt_text()
##
##        return attachment




class AttachboxParser():
    """Parse attachbox style attachments"""
    # TODO Write code for inline attachments
    def find_attachbox_attachments(self):
        """Must not include ANY inline attachments"""
        pass


class InlineattachmentParser():
    """Parse inline attachments, generated from BBcode"""
    # TODO: Move code to here
    def find_inline_attachments(self):
        """Must not include ANY attachbox attachments"""
        pass
    def parse_inline_attachments(self, post_html):
        self.post_html = post_html
        attachment_dicts = []
        inline_attachments = self.find_inline_attachments()
        for inline_attachment in inline_attachments:
            pass
            #attachment_dicts += TODO
        return attachment_dicts



class AttachmentsParser():
    """
    Parse attachments from one post.
    Return a list of dicts for attachments in the post.
    When possible variable names reflect values used by PhpBB.
    This is a class because of problems encountered using just functions.
        (I assume it's some kind of object persistence problem, maybe garbage collection killed the objects passed into functions after they returned?)
    Much of this code is based on the information in this template file:
        https://github.com/phpbb/phpbb/blob/3.1.x/phpBB/styles/prosilver/template/attachment.html
    Python regex likes whitespace to be '\s' instead of some variant of ' '.
    """
    def parse_s_thumbnails(self):
        #<!-- IF _file.S_THUMBNAIL -->
        ts = self.p('.thumbnail')
        print('S_THUMBNAIL: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')
        return attachment_dicts

    def parse_s_image(self):
        #<!-- IF _file.S_IMAGE -->
        ts = self.p('.file .attach-image')
        print('S_IMAGE: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_IMAGE'}
            print('cont: {0!r}'.format(cont))
            snip = cont.parent().outer_html()
            print('snip: {0!r}'.format(snip))

            # <dt class="attach-image"><img src="{_file.U_INLINE_LINK}" class="postimage" alt="{_file.DOWNLOAD_NAME}"
            il_dn_search = re.search('<dt\sclass="attach-image"><img src="([^"]+)"(?:\sclass="postimage")?\salt="([^"]+)"', snip)
            attachment['U_INLINE_LINK'] = il_dn_search.group(1)
            attachment['DOWNLOAD_NAME'] = il_dn_search.group(2)

            # <!-- IF _file.COMMENT --><dd><em>{_file.COMMENT}</em></dd><!-- ENDIF -->
            comment_search = re.search('<dd><em>(.+)</em></dd>', snip)
            if comment_search:
                 comment = comment_search.group(1)
            else: comment = None
            attachment['COMMENT'] = comment

            # dd>{_file.DOWNLOAD_NAME} ({_file.FILESIZE} {_file.SIZE_LANG}) {_file.L_DOWNLOAD_COUNT}</dd>
            dn_fs_sl_dc_search = re.search('<dd>([^"]+)\s(([^"]+)\s([^"]+))\s([^"]+)</dd>', snip)
            attachment['DOWNLOAD_NAME'] = il_dn_search.group(1)
            attachment['FILESIZE'] = il_dn_search.group(2)
            attachment['SIZE_LANG'] = il_dn_search.group(3)
            attachment['L_DOWNLOAD_COUNT'] = il_dn_search.group(4)
            attachment_dicts.append(attachment)
        return attachment_dicts

    def parse_s_file(self):
        #<!-- IF _file.S_FILE -->
        ts = self.p('.file .postlink')
        print('S_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')
        return attachment_dicts

    def parse_s_wm_file(self):
        #<!-- IF _file.S_WM_FILE -->
        ts = self.p('object[id*=wmstream]')
        print('S_WM_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')
        return attachment_dicts

    def parse_s_flash_file(self):
        #<!-- ELSEIF _file.S_FLASH_FILE -->
        ts = self.p('.inline-attachment > object embed[type*=shockwave-flash], .attachbox > dt > object embed[type*=shockwave-flash]')
        print('parse_s_flash_file() ts: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_FLASH_FILE'}
            print('parse_s_flash_file() cont: {0!r}'.format(cont))
            snip = cont.parent().parent().outer_html()# div[class=inline-attachment] > ? > object > embed
            print('parse_s_flash_file() snip: {0!r}'.format(snip))

            # <embed src="{_file.U_VIEW_LINK}" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" width="{_file.WIDTH}" height="{_file.HEIGHT}" play="true" loop="true" quality="high" allowscriptaccess="never" allownetworking="internal"></embed>
            vl_w_h_search = re.search('<embed src="([^"]+)"\stype="application/x-shockwave-flash"\spluginspage="(?:[^"]+)"\swidth="([^"]+)"\sheight="([^"]+)"', snip)
            attachment['U_VIEW_LINK'] = vl_w_h_search.group(1)
            attachment['WIDTH'] = vl_w_h_search.group(2)
            attachment['HEIGHT'] = vl_w_h_search.group(3)


            print('parse_s_flash_file() attachment: {0!r}'.format(attachment))
            attachment_dicts.append(attachment)
        return attachment_dicts

    def parse_s_quicktime_file(self):
        #<!-- ELSEIF _file.S_QUICKTIME_FILE -->
        ts = self.p('object[id*=qtstream]')
        print('S_QUICKTIME_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')
        return attachment_dicts

    def parse_s_rm_file(self):
        #<!-- ELSEIF _file.S_RM_FILE -->
        ts = self.p('object[id*=rmstream]')
        print('S_RM_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')
        return attachment_dicts


    def parse_attachments(self, post_html):
        self.post_html = post_html
        self.p = PyQuery(self.post_html)

        attachment_dicts = []
        #attachment_dicts += self.parse_s_thumbnails()
        attachment_dicts += self.parse_s_image()
        #attachment_dicts += self.parse_s_file()
        #attachment_dicts += self.parse_s_wm_file()
        attachment_dicts += self.parse_s_flash_file()
        #attachment_dicts += self.parse_s_quicktime_file()
        #attachment_dicts += self.parse_s_rm_file()

        print('parse_attachments() attachment_dicts: {0!r}'.format(attachment_dicts))
        return attachment_dicts




### Attachment-level stuff
##class Attachment():
##    def get_attachment_class(self):
##        # Record the type/class of attachment
##        if self.a.has_class('thumbnail'):
##            attachment_class='thumbnail'
##        elif self.a.has_class('inline-attachment'):
##            attachment_class='inline-attachment'
##        elif self.a.has_class('file'):
##            attachment_class='file'
##        else:
##            raise Exception('Unexpected attachment class.')
##        return attachment_class
##
##
##    def get_attachment_dl_url(self):
##        # Find the url of this attachment
##        if (
##            ('href' not in self.attachment_child_outer_html) and
##            ('src' not in self.attachment_child_outer_html) and
##            ('[<div.inline-attachment>]' == repr(self.a))
##            ):
##            print('No download URL for this attachment!')
##            attachment_dl_url = None# This can happen sometimes in quotes
##        else:
##            attachment_dl_url = re.search('"(./download/file\.php\?id=\d+(?:&amp;mode=view|&amp;sid=\w+)*)"', self.attachment_child_outer_html).group(1)
##        return attachment_dl_url
##
##
##    def get_attachment_comment(self):
##        # Find the comment for this attachment, if there is a comment for it
##        attachment_comment = self.a.text()
##        #print('attachment_comment: {0!r}'.format(attachment_comment))
##        return attachment_comment
##
##
##    def get_attachment_title(self):
##        # Attachment title
##        if 'title="' in self.attachment_child_outer_html:# Some don't have this
##            attachment_title = re.search('title="([^"]*)"', self.attachment_child_outer_html).group(1)
##        else:
##            attachment_title = None
##        return attachment_title
##
##
##    def get_attachment_alt_text(self):
##        # Find the alt text for the attachment, if there is one
##        if 'alt="' in self.attachment_child_outer_html:# Some don't have this
##            attachment_alt_text = re.search('alt="([^"]*)"', self.attachment_child_outer_html).group(1)
##        else:
##            attachment_alt_text = None
##        return attachment_alt_text
##    # /Attachment-level stuff
##
##
##    def parse_attachment(self, attachment_child_outer_html):
##        """Parse one attachment
##        Return the extracted information as a dict"""
##        self.attachment_child_outer_html = attachment_child_outer_html
##        self.a = PyQuery(attachment_child_outer_html)
##        #print('attachment_child_outer_html: {0!r}'.format(attachment_child_outer_html))
##
##        attachment = {}
##        attachment['class'] = self.get_attachment_class()
##        attachment['dl_url'] = self.get_attachment_dl_url()
##        attachment['comment'] = self.get_attachment_comment()
##        attachment['title'] = self.get_attachment_title()
##        attachment['alt_text'] = self.get_attachment_alt_text()
##
##        return attachment





# ========== SEPERATOR ========== #

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
        attachments_parser = AttachmentsParser()
        attachment_dicts = attachments_parser.parse_attachments(self.post_outer_html)
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
        return post


# ========== SEPERATOR ========== #

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
            post = Post()
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


# ========== SEPERATOR ========== #



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
    file_path = os.path.join('tests', 'aryion.viewtopic.f55.t11882.offset30.htm')# has swf attachment
    file_path = os.path.join('tests', 'aryion.viewtopic.f79.t17592.htm')# has swf attachment



    with open(file_path, 'r') as f:
        page_html = f.read()


    topic = Topic()
    result = topic.parse_topic(page_html)
    print('result: {0!r}'.format(result))