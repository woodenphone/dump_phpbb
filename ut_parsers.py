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


class TestAryionB38T44962(unittest.TestCase):
    """phpBB v3 https://aryion.com/forum/viewtopic.php?f=38&t=44962"""
    def setUp(self):
        self.board_id = 38
        self.topic_id = 44962
        self.offset = 0
        self.html_path = os.path.join('tests', 'aryion.b38.t44962.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.posts = parsers.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        return
    def test_thread_level(self):
        self.assertEqual(len(self.posts), 20)# Should be 20 posts
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'Lemon-scentedBiscut')# Post 1
        self.assertEqual(self.posts[1]['username'], 'Makuta')# Post 2
        self.assertEqual(self.posts[4]['username'], 'Lemon-scentedBiscut')# Post 5
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], '23032')# Post 1
        self.assertEqual(self.posts[1]['userid'], '50406')# Post 2
        self.assertEqual(self.posts[4]['userid'], '23032')# Post 5
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'requests for biscuts')# Post 1
        self.assertEqual(self.posts[1]['title'], 'Re: requests for biscuts')# Post 2
        self.assertEqual(self.posts[4]['title'], 'Re: requests for biscuts')# Post 5
        return
    def test_post_signatures(self):
        self.assertEqual(self.posts[0]['signature'], '<div id="sig2404876" class="signature"><span style="font-style: italic">Biscuts</span></div>')# Post 1
        self.assertEqual(self.posts[1]['signature'], None)# Post 2
        return
    def test_post_avatars(self):
        self.assertEqual(self.posts[0]['avatar_url'], './download/file.php?avatar=23032_1271009818.jpg')# Post 1
        return
    def test_post_attachments(self):
        self.assertEqual(self.posts[0]['attachments'][0]['dl_url'], './download/file.php?id=147962&amp;mode=view')# Post 1
        self.assertEqual(self.posts[0]['attachments'][0]['comment'], '')# Post 1
        self.assertEqual(self.posts[4]['attachments'][0]['dl_url'], './download/file.php?id=147965&amp;mode=view')# Post 5
        self.assertEqual(self.posts[4]['attachments'][0]['comment'], '')# Post 5
        return



class TestPhpbbB64T2377101(unittest.TestCase):
    """phpBB v3 https://www.phpbb.com/community/viewtopic.php?f=64&t=2377101&sid=531f6eb2847580e38563fecc8d1880b1"""
    def setUp(self):
        self.board_id = 64
        self.topic_id = 2377101
        self.offset = 0
        self.html_path = os.path.join('tests', 'phpbb.b64.t2377101.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.posts = parsers.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        return

    def test_thread_level(self):
        self.assertEqual(len(self.posts), 6)# Should be 20 posts
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], '1382406')
        self.assertEqual(self.posts[1]['userid'], '236419')
        self.assertEqual(self.posts[2]['userid'], '404045')
        self.assertEqual(self.posts[3]['userid'], '1382406')
        self.assertEqual(self.posts[4]['userid'], '404045')
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'mrag')
        self.assertEqual(self.posts[1]['username'], 'Elias')
        self.assertEqual(self.posts[2]['username'], 'Ger')
        self.assertEqual(self.posts[3]['username'], 'mrag')
        self.assertEqual(self.posts[4]['username'], 'Ger')
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'iPhone App to post photo to forum')
        self.assertEqual(self.posts[1]['title'], 'Re: iPhone App to post photo to forum')
        self.assertEqual(self.posts[3]['title'], 'Re: iPhone App to post photo to forum')
        self.assertEqual(self.posts[4]['title'], 'Re: iPhone App to post photo to forum')
        return
    def test_thread_attachments(self):
        self.assertEqual(self.posts[0]['attachments'], None)
        self.assertEqual(self.posts[1]['attachments'], None)
        self.assertEqual(self.posts[2]['attachments'][0]['dl_url'], u'./download/file.php?id=184656&amp;sid=ce0a2ca732b9ae14bab7da0b241b1460&amp;mode=view')
        self.assertEqual(self.posts[3]['attachments'][0]['dl_url'], u'./download/file.php?id=184681&amp;sid=ce0a2ca732b9ae14bab7da0b241b1460&amp;mode=view')
        self.assertEqual(self.posts[4]['attachments'], None)
        return
    def test_post_signatures(self):
        self.assertEqual(self.posts[0]['signature'], None)
        self.assertEqual(self.posts[1]['signature'], u'<div id="sig14462731" class="signature"><!-- m --><a class="postlink" href="http://www.Front-Host.com">http://www.Front-Host.com</a><!-- m --><br/><span style="font-size: 85%; line-height: 116%;"><span style="font-style: italic">"Mystery creates wonder, and wonder is the basis of man\'s desire to understand." - Neil Armstrong</span></span><br/>|<a href="https://www.phpbb.com/extensions/installing/" class="postlink"><span style="font-size: 85%; line-height: 116%;">Installing Extensions</span></a>|<a href="https://www.phpbb.com/extensions/writing/" class="postlink"><span style="font-size: 85%; line-height: 116%;">Writing Extensions</span></a>|<a href="https://www.phpbb.com/extensions/rules-and-policies/validation-policy/" class="postlink"><span style="font-size: 85%; line-height: 116%;">Extension Validation Policy</span></a>|</div>')
        self.assertEqual(self.posts[3]['signature'], None)
        return
    def test_post_avatars(self):
        self.assertEqual(self.posts[0]['avatar_url'], None)
        self.assertEqual(self.posts[3]['avatar_url'], None)
        return



##class TestCyclingforumT11644(unittest.TestCase):
##    """ phpBB v2"""
##    def setUp(self):
##        self.board_id = 1
##        self.topic_id = 11644
##        self.offset = 0
##        self.html_path = os.path.join('tests', 'cyclingforum.t11644.htm')
##        with open(self.html_path, 'r') as f:
##            self.page_html = f.read()
##        self.posts = parsers.parse_thread_page(
##            page_html=self.page_html,
##            board_id=self.board_id,
##            topic_id=self.topic_id,
##            offset=self.offset
##        )
##        return
##
##    def test_thread_level(self):
##        self.assertEqual(len(self.posts), 6)# Should be n posts
##        return
##    def test_post_userids(self):
##        self.assertEqual(self.posts[0]['userid'], '')
##        self.assertEqual(self.posts[1]['userid'], '')
##        self.assertEqual(self.posts[2]['userid'], '')
##        self.assertEqual(self.posts[3]['userid'], '')
##        self.assertEqual(self.posts[4]['userid'], '')
##        return
##    def test_post_usernames(self):
##        self.assertEqual(self.posts[0]['username'], '')
##        self.assertEqual(self.posts[1]['username'], '')
##        self.assertEqual(self.posts[2]['username'], '')
##        self.assertEqual(self.posts[3]['username'], '')
##        self.assertEqual(self.posts[4]['username'], '')
##    def test_post_titles(self):
##        self.assertEqual(self.posts[0]['title'], '')
##        self.assertEqual(self.posts[1]['title'], '')
##        self.assertEqual(self.posts[3]['title'], '')
##        self.assertEqual(self.posts[4]['title'], '')
##    def test_thread_attachments(self):
##        self.assertEqual(self.posts[0]['attachments'], None)
##        self.assertEqual(self.posts[1]['attachments'], None)



class TestElectricalaudioB5T64830(unittest.TestCase):
    """phpBB v3 http://www.electricalaudio.com/phpBB3/viewtopic.php?f=5&t=64830"""
    def setUp(self):
        self.board_id = 5
        self.topic_id = 64830
        self.offset = 0
        self.html_path = os.path.join('tests', 'electricalaudio.b5.t64830.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.posts = parsers.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        return

    def test_thread_level(self):
        self.assertEqual(len(self.posts), 20)# Should be 20 posts
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], '2072')
        self.assertEqual(self.posts[1]['userid'], '13966')
        self.assertEqual(self.posts[2]['userid'], '773')
        self.assertEqual(self.posts[3]['userid'], '80')
        self.assertEqual(self.posts[4]['userid'], '2072')
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'sleepkid')
        self.assertEqual(self.posts[1]['username'], 'Luzwei')
        self.assertEqual(self.posts[2]['username'], 'madlee')
        self.assertEqual(self.posts[3]['username'], 'honeyisfunny')
        self.assertEqual(self.posts[4]['username'], 'sleepkid')
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'Bizarre Japanese Guitars Thread')
        self.assertEqual(self.posts[1]['title'], 'Re: Bizarre Japanese Guitars Thread')
        self.assertEqual(self.posts[3]['title'], 'Re: Bizarre Japanese Guitars Thread')
        self.assertEqual(self.posts[4]['title'], 'Re: Bizarre Japanese Guitars Thread')
        return
    def test_thread_attachments(self):
        self.assertEqual(self.posts[0]['attachments'], None)
        self.assertEqual(self.posts[1]['attachments'], None)



class TestAryionB53T2182Offset2560(unittest.TestCase):
    """phpBB v3 https://aryion.com/forum/viewtopic.php?f=53&t=2182&start=2560"""
    def setUp(self):
        self.board_id = 53
        self.topic_id = 2182
        self.offset = 2560
        self.html_path = os.path.join('tests', 'aryion.b53.t2182.offset2560.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.posts = parsers.parse_thread_page(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        return

    def test_thread_level(self):
        self.assertEqual(len(self.posts), 20)# Should be 20 posts
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], '20892')
        self.assertEqual(self.posts[1]['userid'], '6155')
        self.assertEqual(self.posts[2]['userid'], '40877')
        self.assertEqual(self.posts[3]['userid'], '31799')
        self.assertEqual(self.posts[4]['userid'], '25090')
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'q921143')
        self.assertEqual(self.posts[1]['username'], 'blackskies')
        self.assertEqual(self.posts[2]['username'], 'evilsociopsych')
        self.assertEqual(self.posts[3]['username'], 'Yoshi174')
        self.assertEqual(self.posts[4]['username'], 'C-B-A')
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'Re: Giantess vore drawing thread')
        self.assertEqual(self.posts[1]['title'], 'Re: Giantess vore drawing thread')
        self.assertEqual(self.posts[3]['title'], 'Re: Giantess vore drawing thread')
        self.assertEqual(self.posts[4]['title'], 'Re: Giantess vore drawing thread')
        return
    def test_thread_attachments_alt_text(self):
        self.assertEqual(self.posts[6]['attachments'][0]['alt_text'], u'SaintxTail-314679-LizardLord0001.jpg')
        self.assertEqual(self.posts[4]['attachments'][0]['alt_text'], u'1380945683696.jpg')
        return
    def test_thread_attachments_count(self):
        self.assertEqual(self.posts[0]['attachments'], None)
        self.assertEqual(self.posts[1]['attachments'], None)
        self.assertEqual(self.posts[2]['attachments'], None)
        self.assertEqual(self.posts[3]['attachments'], None)
        self.assertEqual(len(self.posts[4]['attachments']), 1)
        self.assertEqual(self.posts[5]['attachments'], None)
        self.assertEqual(len(self.posts[6]['attachments']), 4)
        self.assertEqual(len(self.posts[7]['attachments']), 4)
        self.assertEqual(self.posts[8]['attachments'], None)
        self.assertEqual(self.posts[9]['attachments'], None)
        self.assertEqual(self.posts[10]['attachments'], None)
        self.assertEqual(self.posts[11]['attachments'], None)
        self.assertEqual(self.posts[12]['attachments'], None)
        self.assertEqual(self.posts[13]['attachments'], None)
        self.assertEqual(self.posts[14]['attachments'], None)
        self.assertEqual(len(self.posts[15]['attachments']), 10)
        self.assertEqual(len(self.posts[16]['attachments']), 16)
        self.assertEqual(len(self.posts[17]['attachments']), 14)
        self.assertEqual(len(self.posts[18]['attachments']), 9)
        self.assertEqual(self.posts[19]['attachments'], None)
        return
    def test_thread_attachments_dl_url(self):
        self.assertEqual(self.posts[4]['attachments'][0]['dl_url'], u'./download/file.php?id=144003&amp;sid=c5d626da13ef107f1162db58be359167&amp;mode=view')
        self.assertEqual(self.posts[6]['attachments'][0]['dl_url'], u'./download/file.php?id=144290&amp;sid=c5d626da13ef107f1162db58be359167&amp;mode=view')
        return
    def test_thread_attachments_title(self):
        self.assertEqual(self.posts[4]['attachments'][0]['title'], u'1380945683696.jpg (454.6 KiB) Viewed 16271 times')
        self.assertEqual(self.posts[6]['attachments'][0]['title'], u'SaintxTail-314679-LizardLord0001.jpg (636.63 KiB) Viewed 14886 times')
        return






def main():
    unittest.main()

if __name__ == '__main__':
    main()
