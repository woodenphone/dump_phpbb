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
        self.board_id = 64
        self.topic_id = 2377101
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
        self.assertEqual(posts[0]['username'], 'mrag')
        self.assertEqual(posts[0]['userid'], '1382406')
        self.assertEqual(posts[0]['title'], 'iPhone App to post photo to forum')
        self.assertEqual(posts[0]['signature'], None)
        self.assertEqual(posts[0]['avatar_url'], None)
        self.assertEqual(posts[0]['attachments'], None)
        # Post 2
        self.assertEqual(posts[1]['username'], 'Elias')
        self.assertEqual(posts[1]['userid'], '236419')
        self.assertEqual(posts[1]['title'], 'Re: iPhone App to post photo to forum')
        self.assertEqual(posts[1]['signature'], u'<div id="sig14462731" class="signature"><!-- m --><a class="postlink" href="http://www.Front-Host.com">http://www.Front-Host.com</a><!-- m --><br/><span style="font-size: 85%; line-height: 116%;"><span style="font-style: italic">"Mystery creates wonder, and wonder is the basis of man\'s desire to understand." - Neil Armstrong</span></span><br/>|<a href="https://www.phpbb.com/extensions/installing/" class="postlink"><span style="font-size: 85%; line-height: 116%;">Installing Extensions</span></a>|<a href="https://www.phpbb.com/extensions/writing/" class="postlink"><span style="font-size: 85%; line-height: 116%;">Writing Extensions</span></a>|<a href="https://www.phpbb.com/extensions/rules-and-policies/validation-policy/" class="postlink"><span style="font-size: 85%; line-height: 116%;">Extension Validation Policy</span></a>|</div>')
        self.assertEqual(posts[1]['attachments'], None)
        # Post 3
        self.assertEqual(posts[2]['username'], 'Ger')
        self.assertEqual(posts[2]['userid'], '404045')
        self.assertEqual(posts[2]['attachments'][0]['dl_url'], u'./download/file.php?id=184656&amp;sid=ce0a2ca732b9ae14bab7da0b241b1460&amp;mode=view')
        # Post 4
        self.assertEqual(posts[3]['username'], 'mrag')
        self.assertEqual(posts[3]['userid'], '1382406')
        self.assertEqual(posts[3]['title'], 'Re: iPhone App to post photo to forum')
        self.assertEqual(posts[3]['signature'], None)
        self.assertEqual(posts[3]['avatar_url'], None)
        self.assertEqual(posts[3]['attachments'][0]['dl_url'], u'./download/file.php?id=184681&amp;sid=ce0a2ca732b9ae14bab7da0b241b1460&amp;mode=view')
        # Post 5
        self.assertEqual(posts[4]['username'], 'Ger')
        self.assertEqual(posts[4]['userid'], '404045')
        self.assertEqual(posts[4]['title'], 'Re: iPhone App to post photo to forum')
        self.assertEqual(posts[4]['attachments'], None)

        return










def main():
    unittest.main()

if __name__ == '__main__':
    main()
