#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: Tests for parse_viewtopic.py
#
# Author:      User
#
# Created:     21/07/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# stdlib
import unittest
import os
# Local
import parse_viewtopic


class TestViewtopicAryionB38T44962(unittest.TestCase):
    """phpBB v3 https://aryion.com/forum/viewtopic.php?f=38&t=44962"""
    def setUp(self):
        self.board_id = 55
        self.topic_id = 11882
        self.offset = 30
        self.html_path = os.path.join('tests', 'aryion.viewtopic.f55.t11882.offset30.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.posts = parse_viewtopic.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        return
    def test_thread_level(self):
        self.assertEqual(len(self.posts), 15)# Should be 20 posts
        return
    def test_swf_attachment(self):
        self.assertEqual(self.posts[0]['attachments'][0]['type'], 'S_FLASH_FILE')
        self.assertEqual(self.posts[0]['attachments'][0]['U_VIEW_LINK'], u'./download/file.php?id=48726&amp;sid=df8fb41c844e053cfd42dc310606983f&amp;view=1')
        self.assertEqual(self.posts[0]['attachments'][0]['WIDTH'], '160')
        self.assertEqual(self.posts[0]['attachments'][0]['HEIGHT'], '120')
        return



def main():
    unittest.main()

if __name__ == '__main__':
    main()
