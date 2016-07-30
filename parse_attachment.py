#-------------------------------------------------------------------------------
# Name:        module1
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




class AttachboxParser():
    """Parse attachbox style attachments"""
    def parse_s_thumbnails(self):
        #<!-- IF _file.S_THUMBNAIL -->
        ts = self.p('.attachbox .thumbnail')
        #print('S_THUMBNAIL: {0!r}'.format(ts))
##        if ts:
##            raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_THUMBNAIL', 'location':'attachbox'}
            #print('cont: {0!r}'.format(cont))
            snip = cont.outer_html()
            #print('snip: {0!r}'.format(snip))

            # {_file.U_DOWNLOAD_LINK}, {_file.THUMB_IMAGE}, {_file.DOWNLOAD_NAME}
            # dt><a href="{_file.U_DOWNLOAD_LINK}"><img src="{_file.THUMB_IMAGE}" class="postimage" alt="{_file.DOWNLOAD_NAME}"
##            dllink_thumbimg_dlname_search = re.search('<dt><a href="([^"]+)"><img src="([^"]+)" class="postimage" alt="([^"]+)"\s', snip)
            dllink_thumbimg_dlname_search = re.search('<dt><a href="([^"]+)"><img src="([^"]+)" (?:class="postimage"\s)?alt="([^"]+)"\s', snip)
            attachment['U_DOWNLOAD_LINK'] = dllink_thumbimg_dlname_search.group(1)
            attachment['THUMB_IMAGE'] = dllink_thumbimg_dlname_search.group(2)
            attachment['DOWNLOAD_NAME'] = dllink_thumbimg_dlname_search.group(3)

            #({_file.FILESIZE} {_file.SIZE_LANG}) {_file.L_DOWNLOAD_COUNT}" /></a></dt>
            filesize_sizelang_dlcount_search = re.search('\(([\d.]+)\s(\w{1,5})\)\sViewed\s(\d+)\stimes"/></a></dt>', snip)
            attachment['FILESIZE'] = dllink_thumbimg_dlname_search.group(1)
            attachment['SIZE_LANG'] = dllink_thumbimg_dlname_search.group(2)
            attachment['L_DOWNLOAD_COUNT'] = dllink_thumbimg_dlname_search.group(3)

            # <!-- IF _file.COMMENT --><dd> {_file.COMMENT}</dd><!-- ENDIF -->
            # {_file.COMMENT}
            if '<dd>' not in snip:
                attachment['COMMENT'] = None
            else:
                comment_search = re.search('<dd>\s(.+)</dd>', snip)
                attachment['COMMENT'] = comment_search.group(1)

            #assert(False)# WIP
            attachment_dicts.append(attachment)
            continue


        return attachment_dicts

    def parse_s_image(self):
        #<!-- IF _file.S_IMAGE -->
        ts = self.p('.attachbox .file .attach-image')
        #print('S_IMAGE: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_IMAGE', 'location':'attachbox'}
            #print('cont: {0!r}'.format(cont))
            snip = cont.parent().outer_html()
            #print('snip: {0!r}'.format(snip))

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
            dn_fs_sl_dc_search = re.search('<dd>([^<>]+)\s\(([\d\.]+)\s(\w+)\)\sViewed\s(\d+)\stimes</dd>', snip)
            attachment['DOWNLOAD_NAME'] = dn_fs_sl_dc_search.group(1)# ex 'foo.jpg'
            attachment['FILESIZE'] = dn_fs_sl_dc_search.group(2)# ex '123'
            attachment['SIZE_LANG'] = dn_fs_sl_dc_search.group(3)# ex 'kb'
            attachment['L_DOWNLOAD_COUNT'] = int(dn_fs_sl_dc_search.group(4))# ex 987
            attachment_dicts.append(attachment)
            continue
        return attachment_dicts

    def parse_s_file(self):
        #<!-- IF _file.S_FILE -->
        ts = self.p('.attachbox .file .postlink')
        if not ts:
            return []
        #print('S_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_FILE', 'location':'attachbox'}
            #print('parse_s_file() cont: {0!r}'.format(cont))
            snip = ts.parent().parent().outer_html()# <dl class="file"> ... </dl>
            #print('parse_s_file() snip: {0!r}'.format(snip))
            # {_file.UPLOAD_ICON}, {_file.U_DOWNLOAD_LINK}, {_file.DOWNLOAD_NAME}
            # <dt><!-- IF _file.UPLOAD_ICON -->{_file.UPLOAD_ICON} <!-- ENDIF --><a class="postlink" href="{_file.U_DOWNLOAD_LINK}">{_file.DOWNLOAD_NAME}</a></dt>
            icon_dllink_dlname_search = re.search('<dt>(.+)?<a class="postlink" href="([^"]+)">(.+)</a>', snip)
            if icon_dllink_dlname_search.group(1):
                attachment['UPLOAD_ICON'] = icon_dllink_dlname_search.group(1)
            else:
                attachment['UPLOAD_ICON'] = None
            attachment['U_DOWNLOAD_LINK'] = icon_dllink_dlname_search.group(2)
            attachment['DOWNLOAD_NAME'] = icon_dllink_dlname_search.group(3)

            # {_file.COMMENT}
            if '<em>' not in snip:
                attachment['COMMENT'] = None
            else:
                # <!-- IF _file.COMMENT --><dd><em>{_file.COMMENT}</em></dd><!-- ENDIF -->
                comment_search = re.search('<em>([^<]+)</em>', snip)
                attachment['COMMENT'] = None

            # {_file.FILESIZE}, {_file.SIZE_LANG}, {_file.L_DOWNLOAD_COUNT}
            # <dd>({_file.FILESIZE} {_file.SIZE_LANG}) {_file.L_DOWNLOAD_COUNT}</dd>
            filesize_sizelang_dlcount_search = re.search('<dd>\(([\d.]+)\s(\w+)\)\sDownloaded\s(\d+)\stimes</dd>', snip)
            attachment['FILESIZE'] = filesize_sizelang_dlcount_search.group(1)
            attachment['SIZE_LANG'] = filesize_sizelang_dlcount_search.group(2)
            attachment['L_DOWNLOAD_COUNT'] = int(filesize_sizelang_dlcount_search.group(3))
            attachment_dicts.append(attachment)
            continue
        return attachment_dicts

    def parse_s_wm_file(self):
        #<!-- IF _file.S_WM_FILE -->
        ts = self.p('.attachbox object[id*=wmstream]')
        if not ts:
            return []
        print('S_WM_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_s_flash_file(self):
        #<!-- ELSEIF _file.S_FLASH_FILE -->
        ts = self.p('.attachbox  object embed[type*=shockwave-flash]')
        if not ts:
            return []
        #print('parse_s_flash_file() ts: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_FLASH_FILE', 'location':'attachbox'}
            #print('parse_s_flash_file() cont: {0!r}'.format(cont))
            snip = cont.parent().parent().outer_html()# div[class=inline-attachment] > ? > object > embed
            #print('parse_s_flash_file() snip: {0!r}'.format(snip))

            # <embed src="{_file.U_VIEW_LINK}" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" width="{_file.WIDTH}" height="{_file.HEIGHT}" play="true" loop="true" quality="high" allowscriptaccess="never" allownetworking="internal"></embed>
            vl_w_h_search = re.search('<embed src="([^"]+)"\stype="application/x-shockwave-flash"\spluginspage="(?:[^"]+)"\swidth="([^"]+)"\sheight="([^"]+)"', snip)
            attachment['U_VIEW_LINK'] = vl_w_h_search.group(1)
            attachment['WIDTH'] = int(vl_w_h_search.group(2))
            attachment['HEIGHT'] = int(vl_w_h_search.group(3))


            #print('parse_s_flash_file() attachment: {0!r}'.format(attachment))
            attachment_dicts.append(attachment)
        return attachment_dicts

    def parse_s_quicktime_file(self):
        #<!-- ELSEIF _file.S_QUICKTIME_FILE -->
        ts = self.p('.attachbox object[id*=qtstream]')
        if not ts:
            return []
        print('S_QUICKTIME_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_s_rm_file(self):
        #<!-- ELSEIF _file.S_RM_FILE -->
        ts = self.p('.attachbox object[id*=rmstream]')
        if not ts:
            return []
        print('S_RM_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_attachbox_attachments(self, post_html):
        """Must not include ANY inline attachments"""
        if 'attachbox' not in post_html:
            return []
        self.post_html = post_html
        self.p = PyQuery(self.post_html)

        attachment_dicts = []
        attachment_dicts += self.parse_s_thumbnails()
        attachment_dicts += self.parse_s_image()
        attachment_dicts += self.parse_s_file()
        attachment_dicts += self.parse_s_wm_file()
        attachment_dicts += self.parse_s_flash_file()
        attachment_dicts += self.parse_s_quicktime_file()
        attachment_dicts += self.parse_s_rm_file()

        #print('parse_attachbox_attachments() attachment_dicts: {0!r}'.format(attachment_dicts))
        return attachment_dicts



class InlineattachmentParser():
    """Parse inline attachments, generated from BBcode"""
    def parse_s_thumbnails(self):
        #<!-- IF _file.S_THUMBNAIL -->
        ts = self.p('.inline-attachment .thumbnail')
        if not ts:
            return []
        #print('S_THUMBNAIL: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_THUMBNAIL', 'location':'attachbox'}
            #print('cont: {0!r}'.format(cont))
            snip = cont.outer_html()
            #print('snip: {0!r}'.format(snip))

            # {_file.U_DOWNLOAD_LINK}, {_file.THUMB_IMAGE}, {_file.DOWNLOAD_NAME}
            # <dt><a href="{_file.U_DOWNLOAD_LINK}"><img src="{_file.THUMB_IMAGE}" alt="{_file.DOWNLOAD_NAME}" title=...
            dllink_thumbimg_dlname_search = re.search('<dt><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"\stitle', snip)
            attachment['U_DOWNLOAD_LINK'] = dllink_thumbimg_dlname_search.group(1)
            attachment['THUMB_IMAGE'] = dllink_thumbimg_dlname_search.group(2)
            attachment['DOWNLOAD_NAME'] = dllink_thumbimg_dlname_search.group(3)

            #({_file.FILESIZE} {_file.SIZE_LANG}) {_file.L_DOWNLOAD_COUNT}" /></a></dt>
            filesize_sizelang_dlcount_search = re.search('\(([\d.]+)\s(\w{1,5})\)\sViewed\s(\d+)\stimes"/></a></dt>', snip)
            attachment['FILESIZE'] = dllink_thumbimg_dlname_search.group(1)
            attachment['SIZE_LANG'] = dllink_thumbimg_dlname_search.group(2)
            attachment['L_DOWNLOAD_COUNT'] = dllink_thumbimg_dlname_search.group(3)

            # <!-- IF _file.COMMENT --><dd> {_file.COMMENT}</dd><!-- ENDIF -->
            # {_file.COMMENT}
            if '<dd>' not in snip:
                attachment['COMMENT'] = None
            else:
                comment_search = re.search('<dd>\s(.+)</dd>', snip)
                attachment['COMMENT'] = comment_search.group(1)

            #assert(False)# WIP
            attachment_dicts.append(attachment)
            continue
        return attachment_dicts

    def parse_s_image(self):
        #<!-- IF _file.S_IMAGE -->
        ts = self.p('.inline-attachment .file .attach-image')
        #print('S_IMAGE: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_IMAGE', 'location':'inline-attachment'}
            #print('cont: {0!r}'.format(cont))
            snip = cont.parent().outer_html()
            #print('snip: {0!r}'.format(snip))

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

            # <dd>{_file.DOWNLOAD_NAME} ({_file.FILESIZE} {_file.SIZE_LANG}) {_file.L_DOWNLOAD_COUNT}</dd>
            dn_fs_sl_dc_search = re.search('<dd>([^<>]+)\s\(([\d\.]+)\s(\w+)\)\sViewed\s(\d+)\stimes</dd>', snip)
            attachment['DOWNLOAD_NAME'] = dn_fs_sl_dc_search.group(1)# ex 'foo.jpg'
            attachment['FILESIZE'] = dn_fs_sl_dc_search.group(2)# ex '123'
            attachment['SIZE_LANG'] = dn_fs_sl_dc_search.group(3)# ex 'kb'
            attachment['L_DOWNLOAD_COUNT'] = int(dn_fs_sl_dc_search.group(4))# ex 987
            attachment_dicts.append(attachment)
        return attachment_dicts

    def parse_s_file(self):
        #<!-- IF _file.S_FILE -->
        ts = self.p('.inline-attachment .file .postlink')
        if not ts:
            return []
        print('S_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_s_wm_file(self):
        #<!-- IF _file.S_WM_FILE -->
        ts = self.p('.inline-attachment object[id*=wmstream]')
        if not ts:
            return []
        print('S_WM_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_s_flash_file(self):
        #<!-- ELSEIF _file.S_FLASH_FILE -->
        ts = self.p('.inline-attachment  object embed[type*=shockwave-flash]')
        #print('parse_s_flash_file() ts: {0!r}'.format(ts))
        attachment_dicts = []
        for cont in ts.items():
            attachment = {'type': 'S_FLASH_FILE', 'location':'inline-attachment'}
            #print('parse_s_flash_file() cont: {0!r}'.format(cont))
            snip = cont.parent().parent().outer_html()# div[class=inline-attachment] > ? > object > embed
            #print('parse_s_flash_file() snip: {0!r}'.format(snip))

            # <embed src="{_file.U_VIEW_LINK}" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" width="{_file.WIDTH}" height="{_file.HEIGHT}" play="true" loop="true" quality="high" allowscriptaccess="never" allownetworking="internal"></embed>
            vl_w_h_search = re.search('<embed src="([^"]+)"\stype="application/x-shockwave-flash"\spluginspage="(?:[^"]+)"\swidth="([^"]+)"\sheight="([^"]+)"', snip)
            attachment['U_VIEW_LINK'] = vl_w_h_search.group(1)
            attachment['WIDTH'] = int(vl_w_h_search.group(2))
            attachment['HEIGHT'] = int(vl_w_h_search.group(3))

            #<a href="[^"]+">([^<]+)</a> \[ ([\d\.]+)\s(\w{1,5}) \| Viewed (\d+) times \]</p>
            dlname_filesize_sizelang_dlcount_search = re.search('<a href="[^"]+">([^<]+)</a> \[ ([\d\.]+)\s(\w{1,5}) \| Viewed (\d+) times \]</p>', snip)
            attachment['DOWNLOAD_NAME'] = dlname_filesize_sizelang_dlcount_search.group(1)
            attachment['FILESIZE'] = dlname_filesize_sizelang_dlcount_search.group(2)
            attachment['SIZE_LANG'] = dlname_filesize_sizelang_dlcount_search.group(3)
            attachment['L_DOWNLOAD_COUNT'] = int(dlname_filesize_sizelang_dlcount_search.group(4))



            #print('parse_s_flash_file() attachment: {0!r}'.format(attachment))
            attachment_dicts.append(attachment)
        return attachment_dicts

    def parse_s_quicktime_file(self):
        #<!-- ELSEIF _file.S_QUICKTIME_FILE -->
        ts = self.p('.inline-attachment object[id*=qtstream]')
        if not ts:
            return []
        print('S_QUICKTIME_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_s_rm_file(self):
        #<!-- ELSEIF _file.S_RM_FILE -->
        ts = self.p('.inline-attachment object[id*=rmstream]')
        if not ts:
            return []
        print('S_RM_FILE: {0!r}'.format(ts))
        attachment_dicts = []
        raise Exception('NotImplimentedYet')# Add these when a test case is discovered
        return attachment_dicts

    def parse_inline_attachments(self, post_html):
        """Must not include ANY attachbox attachments"""
        if 'inline-attachment' not in post_html:
            return []
        self.post_html = post_html
        self.p = PyQuery(self.post_html)

        attachment_dicts = []
        attachment_dicts += self.parse_s_thumbnails()
        attachment_dicts += self.parse_s_image()
        attachment_dicts += self.parse_s_file()
        attachment_dicts += self.parse_s_wm_file()
        attachment_dicts += self.parse_s_flash_file()
        attachment_dicts += self.parse_s_quicktime_file()
        attachment_dicts += self.parse_s_rm_file()

        #print('parse_inline_attachments() attachment_dicts: {0!r}'.format(attachment_dicts))
        return attachment_dicts



##class AttachmentsParser():
##    """
##    Parse attachments from one post.
##    Return a list of dicts for attachments in the post.
##    When possible variable names reflect values used by PhpBB.
##    This is a class because of problems encountered using just functions.
##        (I assume it's some kind of object persistence problem, maybe garbage collection killed the objects passed into functions after they returned?)
##    Much of this code is based on the information in this template file:
##        https://github.com/phpbb/phpbb/blob/3.1.x/phpBB/styles/prosilver/template/attachment.html
##    Python regex likes whitespace to be '\s' instead of some variant of ' '.
##    """
##    def parse_s_thumbnails(self):
##        #<!-- IF _file.S_THUMBNAIL -->
##        ts = self.p('.thumbnail')
##        print('S_THUMBNAIL: {0!r}'.format(ts))
##        attachment_dicts = []
##        raise Exception('NotImplimentedYet')
##        return attachment_dicts
##
##    def parse_s_image(self):
##        #<!-- IF _file.S_IMAGE -->
##        ts = self.p('.file .attach-image')
##        print('S_IMAGE: {0!r}'.format(ts))
##        attachment_dicts = []
##        for cont in ts.items():
##            attachment = {'type': 'S_IMAGE'}
##            print('cont: {0!r}'.format(cont))
##            snip = cont.parent().outer_html()
##            print('snip: {0!r}'.format(snip))
##
##            # <dt class="attach-image"><img src="{_file.U_INLINE_LINK}" class="postimage" alt="{_file.DOWNLOAD_NAME}"
##            il_dn_search = re.search('<dt\sclass="attach-image"><img src="([^"]+)"(?:\sclass="postimage")?\salt="([^"]+)"', snip)
##            attachment['U_INLINE_LINK'] = il_dn_search.group(1)
##            attachment['DOWNLOAD_NAME'] = il_dn_search.group(2)
##
##            # <!-- IF _file.COMMENT --><dd><em>{_file.COMMENT}</em></dd><!-- ENDIF -->
##            comment_search = re.search('<dd><em>(.+)</em></dd>', snip)
##            if comment_search:
##                 comment = comment_search.group(1)
##            else: comment = None
##            attachment['COMMENT'] = comment
##
##            # dd>{_file.DOWNLOAD_NAME} ({_file.FILESIZE} {_file.SIZE_LANG}) {_file.L_DOWNLOAD_COUNT}</dd>
##            dn_fs_sl_dc_search = re.search('<dd>([^"]+)\s(([^"]+)\s([^"]+))\s([^"]+)</dd>', snip)
##            attachment['DOWNLOAD_NAME'] = il_dn_search.group(1)
##            attachment['FILESIZE'] = il_dn_search.group(2)
##            attachment['SIZE_LANG'] = il_dn_search.group(3)
##            attachment['L_DOWNLOAD_COUNT'] = il_dn_search.group(4)
##            attachment_dicts.append(attachment)
##        return attachment_dicts
##
##    def parse_s_file(self):
##        #<!-- IF _file.S_FILE -->
##        ts = self.p('.file .postlink')
##        print('S_FILE: {0!r}'.format(ts))
##        attachment_dicts = []
##        raise Exception('NotImplimentedYet')
##        return attachment_dicts
##
##    def parse_s_wm_file(self):
##        #<!-- IF _file.S_WM_FILE -->
##        ts = self.p('object[id*=wmstream]')
##        print('S_WM_FILE: {0!r}'.format(ts))
##        attachment_dicts = []
##        raise Exception('NotImplimentedYet')
##        return attachment_dicts
##
##    def parse_s_flash_file(self):
##        #<!-- ELSEIF _file.S_FLASH_FILE -->
##        ts = self.p('.inline-attachment > object embed[type*=shockwave-flash], .attachbox > dt > object embed[type*=shockwave-flash]')
##        print('parse_s_flash_file() ts: {0!r}'.format(ts))
##        attachment_dicts = []
##        for cont in ts.items():
##            attachment = {'type': 'S_FLASH_FILE'}
##            print('parse_s_flash_file() cont: {0!r}'.format(cont))
##            snip = cont.parent().parent().outer_html()# div[class=inline-attachment] > ? > object > embed
##            print('parse_s_flash_file() snip: {0!r}'.format(snip))
##
##            # <embed src="{_file.U_VIEW_LINK}" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" width="{_file.WIDTH}" height="{_file.HEIGHT}" play="true" loop="true" quality="high" allowscriptaccess="never" allownetworking="internal"></embed>
##            vl_w_h_search = re.search('<embed src="([^"]+)"\stype="application/x-shockwave-flash"\spluginspage="(?:[^"]+)"\swidth="([^"]+)"\sheight="([^"]+)"', snip)
##            attachment['U_VIEW_LINK'] = vl_w_h_search.group(1)
##            attachment['WIDTH'] = vl_w_h_search.group(2)
##            attachment['HEIGHT'] = vl_w_h_search.group(3)
##
##
##            print('parse_s_flash_file() attachment: {0!r}'.format(attachment))
##            attachment_dicts.append(attachment)
##        return attachment_dicts
##
##    def parse_s_quicktime_file(self):
##        #<!-- ELSEIF _file.S_QUICKTIME_FILE -->
##        ts = self.p('object[id*=qtstream]')
##        print('S_QUICKTIME_FILE: {0!r}'.format(ts))
##        attachment_dicts = []
##        raise Exception('NotImplimentedYet')
##        return attachment_dicts
##
##    def parse_s_rm_file(self):
##        #<!-- ELSEIF _file.S_RM_FILE -->
##        ts = self.p('object[id*=rmstream]')
##        print('S_RM_FILE: {0!r}'.format(ts))
##        attachment_dicts = []
##        raise Exception('NotImplimentedYet')
##        return attachment_dicts
##
##
##    def parse_attachments(self, post_html):
##        self.post_html = post_html
##        self.p = PyQuery(self.post_html)
##
##        attachment_dicts = []
##        #attachment_dicts += self.parse_s_thumbnails()
##        attachment_dicts += self.parse_s_image()
##        #attachment_dicts += self.parse_s_file()
##        #attachment_dicts += self.parse_s_wm_file()
##        attachment_dicts += self.parse_s_flash_file()
##        #attachment_dicts += self.parse_s_quicktime_file()
##        #attachment_dicts += self.parse_s_rm_file()
##
##        print('parse_attachments() attachment_dicts: {0!r}'.format(attachment_dicts))
##        return attachment_dicts




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







def main():
    pass


if __name__ == '__main__':
    post_id = 2493048
##    html_path = os.path.join('tests', 'single_posts', 'aryion', '2493048.html')# has swf attachment
    html_path = os.path.join('tests', 'single_posts', 'aryion', '470081.html')# has swf attachment
##    html_path = os.path.join('tests', 'phpbb.b64.t2377101.htm') # parse_s_thumbnails
##    html_path = os.path.join('tests', 'aryion.b53.t2182.offset2560.htm')

    with open(html_path, 'r') as f:
            html = f.read()

    attachment_dicts = []
    iap = InlineattachmentParser()
    attachment_dicts += iap.parse_inline_attachments(post_html = html)

    abp = AttachboxParser()
    attachment_dicts += abp.parse_attachbox_attachments(post_html = html)

    print('parse_attachments() attachment_dicts: {0!r}'.format(attachment_dicts))
    main()
