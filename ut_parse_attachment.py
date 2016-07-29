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
import unittest
import os
# Local
import parse_attachment


class TestAryionPid431895(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=55&t=???? split to just have the post no 431895"""
    def setUp(self):
        self.post_id = 11882
        self.html_path = os.path.join('tests', 'single_posts', 'aryion', '431895.html')# has swf attachment
        with open(self.html_path, 'r') as f:
            self.html = f.read()
        return
    def test_attachbox(self):
        abp = parse_attachment.AttachboxParser()
        attachment_dicts = abp.parse_attachbox_attachments(self.html)
        # Exactly one attachbox attachment
        self.assertEqual(len(attachment_dicts), 1)
        # Correct attributes
        self.assertEqual(attachment_dicts[0]['WIDTH'], 550)
        self.assertEqual(attachment_dicts[0]['HEIGHT'], 400)
        self.assertEqual(attachment_dicts[0]['type'], 'S_FLASH_FILE')
        self.assertEqual(attachment_dicts[0]['location'], 'attachbox')
        self.assertEqual(attachment_dicts[0]['U_VIEW_LINK'], u'./download/file.php?id=50538&amp;sid=94830efc363406eaccf0543e2ce92977&amp;view=1')
        return
    def test_inline(self):
        iap = parse_attachment.InlineattachmentParser()
        attachment_dicts = iap.parse_inline_attachments(self.html)
        # No inline attachments
        self.assertEqual(len(attachment_dicts), 0)
        return



class TestAryionPid5910(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=55&t=???? split to just have the post no 5910"""
    def setUp(self):
        self.post_id = 11882
        self.html_path = os.path.join('tests', 'single_posts', 'aryion', '5910.html')# has swf attachment
        with open(self.html_path, 'r') as f:
            self.html = f.read()
        return
    def test_attachbox(self):
        abp = parse_attachment.AttachboxParser()
        attachment_dicts = abp.parse_attachbox_attachments(self.html)
        # Exactly one attachbox attachment
        self.assertEqual(len(attachment_dicts), 1)
        # Correct attributes

        self.assertEqual(attachment_dicts[0]['real_filename'], 'folly.jpg')
        self.assertEqual(attachment_dicts[0]['COMMENT'], u'Yeah its vore...what else can I say. Partake and enjoy.')
        self.assertEqual(attachment_dicts[0]['download_count'], 1231)
        self.assertEqual(attachment_dicts[0]['FILESIZE'], '99.12')
        self.assertEqual(attachment_dicts[0]['SIZE_LANG'], 'KiB')
        self.assertEqual(attachment_dicts[0]['type'], 'S_IMAGE')
        self.assertEqual(attachment_dicts[0]['location'], 'attachbox')
        return
    def test_inline(self):
        iap = parse_attachment.InlineattachmentParser()
        attachment_dicts = iap.parse_inline_attachments(self.html)
        # No inline attachments
        self.assertEqual(len(attachment_dicts), 0)
        return





def main():
    unittest.main()

if __name__ == '__main__':
    main()