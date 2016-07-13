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
import unittest
import os
# Local
import parsers


class TestAryionB38T44962(unittest.TestCase):# TODO
    def setUp(self):
        self.board_id = 38
        self.topic_id = 44962
        self.offset = 0
        self.html_path = os.path.join('tests', 'aryion.b38.t44962.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        return

    def test_thread_parse(self):
        posts = parsers.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        # Thread level
        self.assertEqual(len(posts), 20)# Should be 20 posts
        # Post 1
        self.assertEqual(posts[0]['username'], 'Lemon-scentedBiscut')
        self.assertEqual(posts[0]['userid'], '23032')
        self.assertEqual(posts[0]['title'], 'requests for biscuts')
        self.assertEqual(posts[0]['signature'], '<div id="sig2404876" class="signature"><span style="font-style: italic">Biscuts</span></div>')
        self.assertEqual(posts[0]['avatar_url'], './download/file.php?avatar=23032_1271009818.jpg')
        self.assertEqual(posts[0]['attachments'][0]['dl_url'], './download/file.php?id=147962&amp;mode=view')
        self.assertEqual(posts[0]['attachments'][0]['comment'], '')
        # Post 2
        self.assertEqual(posts[1]['username'], 'Makuta')
        self.assertEqual(posts[1]['userid'], '50406')
        self.assertEqual(posts[1]['title'], 'Re: requests for biscuts')
        self.assertEqual(posts[1]['signature'], None)
        # Post 5
        self.assertEqual(posts[4]['username'], 'Lemon-scentedBiscut')
        self.assertEqual(posts[4]['userid'], '23032')
        self.assertEqual(posts[4]['title'], 'Re: requests for biscuts')
        self.assertEqual(posts[4]['attachments'][0]['dl_url'], './download/file.php?id=147965&amp;mode=view')
        self.assertEqual(posts[4]['attachments'][0]['comment'], '')
        return




class TestPhpbbB64T2377101(unittest.TestCase):# TODO
    def setUp(self):
        self.board_id = 38
        self.topic_id = 44962
        self.offset = 0
        self.html_path = os.path.join('tests', 'phpbb.b64.t2377101.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        return

    def test_thread_parse(self):
        posts = parsers.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        # Thread level
        self.assertEqual(len(posts), 6)# Should be 20 posts
        # Post 1
        self.assertEqual(posts[0]['username'], 'Lemon-scentedBiscut')
        self.assertEqual(posts[0]['userid'], '23032')
        self.assertEqual(posts[0]['title'], 'requests for biscuts')
        self.assertEqual(posts[0]['signature'], '<div id="sig2404876" class="signature"><span style="font-style: italic">Biscuts</span></div>')
        self.assertEqual(posts[0]['avatar_url'], './download/file.php?avatar=23032_1271009818.jpg')
        self.assertEqual(posts[0]['attachments'][0]['dl_url'], './download/file.php?id=147962&amp;mode=view')
        self.assertEqual(posts[0]['attachments'][0]['comment'], '')
        # Post 2
        self.assertEqual(posts[1]['username'], 'Makuta')
        self.assertEqual(posts[1]['userid'], '50406')
        self.assertEqual(posts[1]['title'], 'Re: requests for biscuts')
        self.assertEqual(posts[1]['signature'], None)
        # Post 5
        self.assertEqual(posts[4]['username'], 'Lemon-scentedBiscut')
        self.assertEqual(posts[4]['userid'], '23032')
        self.assertEqual(posts[4]['title'], 'Re: requests for biscuts')
        self.assertEqual(posts[4]['attachments'][0]['dl_url'], './download/file.php?id=147965&amp;mode=view')
        self.assertEqual(posts[4]['attachments'][0]['comment'], '')
        return










def main():
    unittest.main()

if __name__ == '__main__':
    main()
