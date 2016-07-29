#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: tests for parsers.py
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
import parse_viewtopic

class TestViewtopicAryionB38T44962(unittest.TestCase):
    """phpBB v3 https://aryion.com/forum/viewtopic.php?f=38&t=44962"""
    def setUp(self):
        self.board_id = 38
        self.topic_id = 44962
        self.offset = 0
        self.html_path = os.path.join('tests', 'aryion.b38.t44962.htm')
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



class TestViewtopicPhpbbB64T2377101(unittest.TestCase):
    """phpBB v3 https://www.phpbb.com/community/viewtopic.php?f=64&t=2377101&sid=531f6eb2847580e38563fecc8d1880b1"""
    def setUp(self):
        self.board_id = 64
        self.topic_id = 2377101
        self.offset = 0
        self.html_path = os.path.join('tests', 'phpbb.b64.t2377101.htm')
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
        self.assertEqual(len(self.posts), 6)# Should be 20 posts
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 1382406)
        self.assertEqual(self.posts[1]['userid'], 236419)
        self.assertEqual(self.posts[2]['userid'], 404045)
        self.assertEqual(self.posts[3]['userid'], 1382406)
        self.assertEqual(self.posts[4]['userid'], 404045)
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
##        self.posts = parse_viewtopic.parse_thread_page(
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



class TestViewtopicElectricalaudioB5T64830(unittest.TestCase):
    """phpBB v3 http://www.electricalaudio.com/phpBB3/viewtopic.php?f=5&t=64830"""
    def setUp(self):
        self.board_id = 5
        self.topic_id = 64830
        self.offset = 0
        self.html_path = os.path.join('tests', 'electricalaudio.b5.t64830.htm')
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
        self.assertEqual(len(self.posts), 20)# Should be 20 posts
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 2072)
        self.assertEqual(self.posts[1]['userid'], 13966)
        self.assertEqual(self.posts[2]['userid'], 773)
        self.assertEqual(self.posts[3]['userid'], 80)
        self.assertEqual(self.posts[4]['userid'], 2072)
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
        self.assertEqual(self.posts[0]['attachments'], [])
        self.assertEqual(self.posts[1]['attachments'], [])



class TestViewtopicAryionB53T2182Offset2560(unittest.TestCase):
    """phpBB v3 https://aryion.com/forum/viewtopic.php?f=53&t=2182&start=2560"""
    def setUp(self):
        self.board_id = 53
        self.topic_id = 2182
        self.offset = 2560
        self.html_path = os.path.join('tests', 'aryion.b53.t2182.offset2560.htm')
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
        self.assertEqual(len(self.posts), 20)# Should be 20 posts
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 20892)
        self.assertEqual(self.posts[1]['userid'], 6155)
        self.assertEqual(self.posts[2]['userid'], 40877)
        self.assertEqual(self.posts[3]['userid'], 31799)
        self.assertEqual(self.posts[4]['userid'], 25090)
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
        self.assertEqual(self.posts[6]['attachments'][0]['DOWNLOAD_NAME'], u'SaintxTail-314679-LizardLord0001.jpg')
        self.assertEqual(self.posts[4]['attachments'][0]['DOWNLOAD_NAME'], u'1380945683696.jpg')
        return
    def test_thread_attachments_count(self):
        self.assertEqual(self.posts[0]['attachments'], [])
        self.assertEqual(self.posts[1]['attachments'], [])
        self.assertEqual(self.posts[2]['attachments'], [])
        self.assertEqual(self.posts[3]['attachments'], [])
        self.assertEqual(len(self.posts[4]['attachments']), 1)
        self.assertEqual(self.posts[5]['attachments'], None)
        self.assertEqual(len(self.posts[6]['attachments']), 4)
        self.assertEqual(len(self.posts[7]['attachments']), 4)
        self.assertEqual(self.posts[8]['attachments'], [])
        self.assertEqual(self.posts[9]['attachments'], [])
        self.assertEqual(self.posts[10]['attachments'], [])
        self.assertEqual(self.posts[11]['attachments'], [])
        self.assertEqual(self.posts[12]['attachments'], [])
        self.assertEqual(self.posts[13]['attachments'], [])
        self.assertEqual(self.posts[14]['attachments'], [])
        self.assertEqual(len(self.posts[15]['attachments']), 10)
        self.assertEqual(len(self.posts[16]['attachments']), 16)
        self.assertEqual(len(self.posts[17]['attachments']), 7)
        self.assertEqual(len(self.posts[18]['attachments']), 8)
        self.assertEqual(self.posts[19]['attachments'], [])
        return
    def test_thread_attachments_dl_url(self):
        self.assertEqual(self.posts[4]['attachments'][0]['dl_url'], u'./download/file.php?id=144003&amp;sid=c5d626da13ef107f1162db58be359167&amp;mode=view')
        self.assertEqual(self.posts[6]['attachments'][0]['dl_url'], u'./download/file.php?id=144290&amp;sid=c5d626da13ef107f1162db58be359167&amp;mode=view')
        return
    def test_thread_attachments_title(self):
        self.assertEqual(self.posts[4]['attachments'][0]['title'], u'1380945683696.jpg (454.6 KiB) Viewed 16271 times')
        self.assertEqual(self.posts[6]['attachments'][0]['title'], u'SaintxTail-314679-LizardLord0001.jpg (636.63 KiB) Viewed 14886 times')
        return
    def test_attachment_class(self):
        self.assertEqual(self.posts[4]['attachments'][0]['class'], 'thumbnail')

        self.assertEqual(self.posts[6]['attachments'][0]['class'], 'thumbnail')
        self.assertEqual(self.posts[6]['attachments'][1]['class'], 'thumbnail')
        self.assertEqual(self.posts[6]['attachments'][2]['class'], 'thumbnail')
        self.assertEqual(self.posts[6]['attachments'][3]['class'], 'thumbnail')

        self.assertEqual(self.posts[17]['attachments'][0]['class'], 'inline-attachment')#https://aryion.com/forum/viewtopic.php?f=53&t=2182&start=2560#p2427846
        self.assertEqual(self.posts[17]['attachments'][1]['class'], 'inline-attachment')
        self.assertEqual(self.posts[17]['attachments'][2]['class'], 'inline-attachment')
        self.assertEqual(self.posts[17]['attachments'][3]['class'], 'inline-attachment')
        self.assertEqual(self.posts[17]['attachments'][4]['class'], 'inline-attachment')
        self.assertEqual(self.posts[17]['attachments'][5]['class'], 'inline-attachment')
        self.assertEqual(self.posts[17]['attachments'][6]['class'], 'inline-attachment')
        self.assertEqual(self.posts[17]['attachments'][7]['class'], 'inline-attachment')

        self.assertEqual(self.posts[18]['attachments'][0]['class'], 'thumbnail')
        self.assertEqual(self.posts[18]['attachments'][1]['class'], 'thumbnail')
        self.assertEqual(self.posts[18]['attachments'][2]['class'], 'thumbnail')
        self.assertEqual(self.posts[18]['attachments'][3]['class'], 'file')
        self.assertEqual(self.posts[18]['attachments'][4]['class'], 'thumbnail')
        self.assertEqual(self.posts[18]['attachments'][5]['class'], 'thumbnail')
        self.assertEqual(self.posts[18]['attachments'][6]['class'], 'thumbnail')
        self.assertEqual(self.posts[18]['attachments'][7]['class'], 'thumbnail')
        return



class TestViewtopicPhpbbB6T362219ffset270(unittest.TestCase):
    """phpBB v3 """
    def setUp(self):
        self.board_id = 6
        self.topic_id = 362219
        self.offset = 270
        self.html_path = os.path.join('tests', 'phpbb.b6.t362219.offset270.htm')
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
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 874305)
        self.assertEqual(self.posts[1]['userid'], 956185)
        self.assertEqual(self.posts[2]['userid'], 329351)
        self.assertEqual(self.posts[3]['userid'], 882465)
        self.assertEqual(self.posts[7]['userid'], None)# No user ID for this post
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'koimaster')
        self.assertEqual(self.posts[1]['username'], '4Teach')
        self.assertEqual(self.posts[2]['username'], 'vamsy')
        self.assertEqual(self.posts[3]['username'], 'Snorlaxative')
        self.assertEqual(self.posts[4]['username'], 'DeepUnderground')
        self.assertEqual(self.posts[7]['username'], 'scottlpool2003')# No user ID for this post
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'Re: The hardest question of all... how do you get new users?')
        self.assertEqual(self.posts[1]['title'], 'Re: The hardest question of all... how do you get new users?')
        self.assertEqual(self.posts[3]['title'], 'Re: The hardest question of all... how do you get new users?')
        self.assertEqual(self.posts[4]['title'], 'Re: The hardest question of all... how do you get new users?')
        return
    def test_thread_attachments_alt_text(self):
##        self.assertEqual(self.posts[6]['attachments'][0]['alt_text'], u'SaintxTail-314679-LizardLord0001.jpg')
##        self.assertEqual(self.posts[4]['attachments'][0]['alt_text'], u'1380945683696.jpg')
        return
    def test_thread_attachments_count(self):
        self.assertEqual(self.posts[0]['attachments'], [])
        self.assertEqual(self.posts[1]['attachments'], [])
        self.assertEqual(self.posts[2]['attachments'], [])
        self.assertEqual(self.posts[3]['attachments'], [])
        return
    def test_thread_attachments_dl_url(self):
##        self.assertEqual(self.posts[4]['attachments'][0]['dl_url'], u'./download/file.php?id=144003&amp;sid=c5d626da13ef107f1162db58be359167&amp;mode=view')
##        self.assertEqual(self.posts[6]['attachments'][0]['dl_url'], u'./download/file.php?id=144290&amp;sid=c5d626da13ef107f1162db58be359167&amp;mode=view')
        return
    def test_thread_attachments_title(self):
##        self.assertEqual(self.posts[4]['attachments'][0]['title'], u'1380945683696.jpg (454.6 KiB) Viewed 16271 times')
##        self.assertEqual(self.posts[6]['attachments'][0]['title'], u'SaintxTail-314679-LizardLord0001.jpg (636.63 KiB) Viewed 14886 times')
        return




class TestViewtopicPhpbbB6T2259706ffset15(unittest.TestCase):
    """phpBB v3
    https://www.phpbb.com/community/viewtopic.php?f=6&t=2259706&start=15
    Has an attachment class without any file/link/image"""
    def setUp(self):
        self.board_id = 6
        self.topic_id = 2259706
        self.offset = 15
        self.html_path = os.path.join('tests', 'phpbb.b6.t2259706.offset15.htm')
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
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 182473)
        self.assertEqual(self.posts[11]['userid'], 1136425)
        self.assertEqual(self.posts[13]['userid'], 1136425)
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'Lumpy Burgertushie')
        self.assertEqual(self.posts[11]['username'], 'Danielx64')
        self.assertEqual(self.posts[13]['username'], 'Danielx64')
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'Re: Speedtest')
        self.assertEqual(self.posts[11]['title'], 'Re: Speedtest')
        self.assertEqual(self.posts[13]['title'], 'Re: Speedtest')
        return
    def test_thread_attachments_alt_text(self):
        self.assertEqual(self.posts[11]['attachments'][0]['DOWNLOAD_NAME'], None)# Attachment is strange in this post
        self.assertEqual(self.posts[13]['attachments'][0]['DOWNLOAD_NAME'], u'3775542717.png')
        return
    def test_thread_attachments_count(self):
        print("self.posts[13]['attachments']: {0!r}".format(self.posts[13]['attachments']))
        self.assertEqual(self.posts[0]['attachments'], [])
        self.assertEqual(self.posts[1]['attachments'], [])
        self.assertEqual(self.posts[2]['attachments'], [])
        self.assertEqual(self.posts[3]['attachments'], [])
        self.assertEqual(len(self.posts[11]['attachments']), 1)# Attachment is strange in this post
        self.assertEqual(len(self.posts[13]['attachments']), 3)
        return
    def test_thread_attachments_dl_url(self):
        self.assertEqual(self.posts[11]['attachments'][0]['dl_url'], None)# Attachment is strange in this post
        self.assertEqual(self.posts[13]['attachments'][0]['dl_url'], u'./download/file.php?id=159886&amp;sid=5f585129d9f3e20dde9a82ebe4facd8d')
        return
    def test_thread_attachments_title(self):
        self.assertEqual(self.posts[11]['attachments'][0]['title'], None)# Attachment is strange in this post
        self.assertEqual(self.posts[13]['attachments'][0]['title'], None)
        return




class TestListingPphbbB64(unittest.TestCase):
    """phpBB v3
    https://www.phpbb.com/community/viewforum.php?f=64
    Normal viewforum page"""
    def setUp(self):
        self.board_id = 6
        self.posts_per_page = 15
        self.html_path = os.path.join('tests', 'phpbb.b64.listing.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.topics = parsers.parse_threads_listing_page(
            html=self.page_html,
            board_id=self.board_id,
            posts_per_page=self.posts_per_page
        )
        return

    def test_number_of_threads_found(self):
        self.assertEqual(len(self.topics), 26)
    def test_locked_detection(self):
        self.assertEqual(self.topics[0]['locked'], True)
        self.assertEqual(self.topics[1]['locked'], False)
        self.assertEqual(self.topics[2]['locked'], False)
        self.assertEqual(self.topics[3]['locked'], False)
        self.assertEqual(self.topics[4]['locked'], False)
        self.assertEqual(self.topics[25]['locked'], False)
        return
    def test_announcement_detection(self):
        self.assertEqual(self.topics[0]['thread_type'], 'announce')
        self.assertEqual(self.topics[1]['thread_type'], 'sticky')
        self.assertEqual(self.topics[2]['thread_type'], 'sticky')
        self.assertEqual(self.topics[3]['thread_type'], 'sticky')
        self.assertEqual(self.topics[4]['thread_type'], 'normal')
        self.assertEqual(self.topics[5]['thread_type'], 'normal')
        self.assertEqual(self.topics[25]['thread_type'], 'normal')
        return
    def test_topic_id_detection(self):
        #print('topics: {0!r}'.format(self.topics))
        self.assertEqual(self.topics[0]['topic_id'], 558789)
        self.assertEqual(self.topics[1]['topic_id'], 10385)
        self.assertEqual(self.topics[2]['topic_id'], 2103285)
        self.assertEqual(self.topics[3]['topic_id'], 1237515)
        self.assertEqual(self.topics[4]['topic_id'], 2379711)
        self.assertEqual(self.topics[25]['topic_id'], 2376576)



class TestListingAryionB21(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewforum.php?f=21
    Normal viewforum page"""
    def setUp(self):
        self.board_id = 6
        self.posts_per_page = 20
        self.html_path = os.path.join('tests', 'aryion.viewforum.f21.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.topics = parsers.parse_threads_listing_page(
            html=self.page_html,
            board_id=self.board_id,
            posts_per_page=self.posts_per_page
        )
        return

    def test_number_of_threads_found(self):
        self.assertEqual(len(self.topics), 50)
    def test_locked_detection(self):
        self.assertEqual(self.topics[0]['locked'], False)
        self.assertEqual(self.topics[1]['locked'], False)
        self.assertEqual(self.topics[2]['locked'], True)
        self.assertEqual(self.topics[3]['locked'], True)
        self.assertEqual(self.topics[4]['locked'], True)
        self.assertEqual(self.topics[25]['locked'], False)
        self.assertEqual(self.topics[49]['locked'], False)
        return
    def test_announcement_detection(self):
        self.assertEqual(self.topics[0]['thread_type'], 'sticky')
        self.assertEqual(self.topics[1]['thread_type'], 'sticky')
        self.assertEqual(self.topics[2]['thread_type'], 'normal')
        self.assertEqual(self.topics[3]['thread_type'], 'normal')
        self.assertEqual(self.topics[4]['thread_type'], 'normal')
        self.assertEqual(self.topics[5]['thread_type'], 'normal')
        self.assertEqual(self.topics[25]['thread_type'], 'normal')
        self.assertEqual(self.topics[49]['thread_type'], 'normal')
        return
    def test_topic_id_detection(self):
        self.assertEqual(self.topics[0]['topic_id'], 12751)
        self.assertEqual(self.topics[1]['topic_id'], 27754)
        self.assertEqual(self.topics[2]['topic_id'], 47207)
        self.assertEqual(self.topics[3]['topic_id'], 47200)
        self.assertEqual(self.topics[4]['topic_id'], 47150)
        self.assertEqual(self.topics[49]['topic_id'], 44870)
        return



class TestListingElectricalaudioB5(unittest.TestCase):
    """phpBB v3
    http://www.electricalaudio.com/phpBB3/viewforum.php?f=5
    Normal viewforum page"""
    def setUp(self):
        self.board_id = 6
        self.posts_per_page = 20
        self.html_path = os.path.join('tests', 'electricalaudio.f5.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.topics = parsers.parse_threads_listing_page(
            html=self.page_html,
            board_id=self.board_id,
            posts_per_page=self.posts_per_page
        )
        return

    def test_number_of_threads_found(self):
        self.assertEqual(len(self.topics), 51)
    def test_locked_detection(self):
        self.assertEqual(self.topics[0]['locked'], False)
        self.assertEqual(self.topics[1]['locked'], False)
        self.assertEqual(self.topics[2]['locked'], False)
        self.assertEqual(self.topics[3]['locked'], False)
        self.assertEqual(self.topics[4]['locked'], False)
        self.assertEqual(self.topics[25]['locked'], False)
        self.assertEqual(self.topics[50]['locked'], False)
        return
    def test_announcement_detection(self):
        self.assertEqual(self.topics[0]['thread_type'], 'announce')
        self.assertEqual(self.topics[1]['thread_type'], 'sticky')
        self.assertEqual(self.topics[2]['thread_type'], 'sticky')
        self.assertEqual(self.topics[3]['thread_type'], 'sticky')
        self.assertEqual(self.topics[4]['thread_type'], 'normal')
        self.assertEqual(self.topics[5]['thread_type'], 'normal')
        self.assertEqual(self.topics[25]['thread_type'], 'normal')
        self.assertEqual(self.topics[50]['thread_type'], 'normal')
        return
    def test_topic_id_detection(self):
        #print('topics: {0!r}'.format(self.topics))
        self.assertEqual(self.topics[0]['topic_id'], 63483)
        self.assertEqual(self.topics[1]['topic_id'], 491)
        self.assertEqual(self.topics[2]['topic_id'], 55031)
        self.assertEqual(self.topics[3]['topic_id'], 34722)
        self.assertEqual(self.topics[4]['topic_id'], 51141)
        self.assertEqual(self.topics[50]['topic_id'], 67172)
        return



class TestListingChichlidforumB4(unittest.TestCase):
    """phpBB v3
    http://www.cichlid-forum.com/phpbb/viewforum.php?f=4&sid=3
    Normal viewforum page"""
    def setUp(self):
        self.board_id = 4
        self.posts_per_page = 20
        self.html_path = os.path.join('tests', 'cichlid-forum.viewforum.f4.htm')
        with open(self.html_path, 'r') as f:
            self.page_html = f.read()
        self.topics = parsers.parse_threads_listing_page(
            html=self.page_html,
            board_id=self.board_id,
            posts_per_page=self.posts_per_page
        )
        return

    def test_number_of_threads_found(self):
        self.assertEqual(len(self.topics), 53)
    def test_locked_detection(self):
        self.assertEqual(self.topics[0]['locked'], True)
        self.assertEqual(self.topics[1]['locked'], True)
        self.assertEqual(self.topics[2]['locked'], True)
        self.assertEqual(self.topics[3]['locked'], True)
        self.assertEqual(self.topics[4]['locked'], False)
        self.assertEqual(self.topics[25]['locked'], False)
        self.assertEqual(self.topics[50]['locked'], False)
        self.assertEqual(self.topics[52]['locked'], False)
        return
    def test_announcement_detection(self):
        self.assertEqual(self.topics[0]['thread_type'], 'global-announce')
        self.assertEqual(self.topics[1]['thread_type'], 'announce')
        self.assertEqual(self.topics[2]['thread_type'], 'announce')
        self.assertEqual(self.topics[3]['thread_type'], 'sticky')
        self.assertEqual(self.topics[4]['thread_type'], 'normal')
        self.assertEqual(self.topics[5]['thread_type'], 'normal')
        self.assertEqual(self.topics[25]['thread_type'], 'normal')
        self.assertEqual(self.topics[50]['thread_type'], 'normal')
        self.assertEqual(self.topics[52]['thread_type'], 'normal')
        return
    def test_topic_id_detection(self):
        #print('topics: {0!r}'.format(self.topics))
        self.assertEqual(self.topics[0]['topic_id'], 307234)
        self.assertEqual(self.topics[1]['topic_id'], 255444)
        self.assertEqual(self.topics[2]['topic_id'], 125185)
        self.assertEqual(self.topics[3]['topic_id'], 239823)
        self.assertEqual(self.topics[4]['topic_id'], 391585)
        self.assertEqual(self.topics[50]['topic_id'], 389066)
        self.assertEqual(self.topics[52]['topic_id'], 388033)
        return



class TestViewtopicChichlidforumf4t246181(unittest.TestCase):
    """phpBB v3
    http://www.cichlid-forum.com/phpbb/viewtopic.php?f=4&t=246181
    Normal viewtopic page"""
    def setUp(self):
        self.board_id = 4
        self.topic_id = 246181
        self.offset = 0
        self.html_path = os.path.join('tests', 'cichlid-forum.viewtopic.f4.t246181.htm')
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
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 75869)
        self.assertEqual(self.posts[1]['userid'], 68437)
        self.assertEqual(self.posts[2]['userid'], 75869)
        self.assertEqual(self.posts[3]['userid'], 68437)
        self.assertEqual(self.posts[14]['userid'], 75869)
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'orau22')
        self.assertEqual(self.posts[1]['username'], 'jd lover')
        self.assertEqual(self.posts[2]['username'], 'orau22')
        self.assertEqual(self.posts[3]['username'], 'jd lover')
        self.assertEqual(self.posts[14]['username'], 'orau22')
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'Tank Cycling w/ Dr. Tim\'s One and Only')
        self.assertEqual(self.posts[1]['title'], "Re: Tank Cycling w/ Dr. Tim's One and Only")
        self.assertEqual(self.posts[3]['title'], "Re: Tank Cycling w/ Dr. Tim's One and Only")
        self.assertEqual(self.posts[14]['title'], "Re: Tank Cycling w/ Dr. Tim's One and Only")
        return
    def test_thread_attachments_count(self):
        self.assertEqual(self.posts[0]['attachments'], [])
        self.assertEqual(self.posts[1]['attachments'], [])
        self.assertEqual(self.posts[2]['attachments'], [])
        self.assertEqual(self.posts[14]['attachments'], [])
        return



class TestViewtopicAryionB38T695(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=38&t=695
    Really old, 2005"""
    def setUp(self):
        self.board_id = 38
        self.topic_id = 695
        self.offset = 0
        self.html_path = os.path.join('tests', 'aryion.viewtopic.f38.t695.htm')
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
        self.assertEqual(len(self.posts), 6)
        return
    def test_post_userids(self):
        self.assertEqual(self.posts[0]['userid'], 958)
        self.assertEqual(self.posts[1]['userid'], 3)
        self.assertEqual(self.posts[2]['userid'], 823)
        return
    def test_post_usernames(self):
        self.assertEqual(self.posts[0]['username'], 'ress_q_puma')
        self.assertEqual(self.posts[1]['username'], 'Eka')
        self.assertEqual(self.posts[2]['username'], 'Ai_ga_Kowai')
        return
    def test_post_titles(self):
        self.assertEqual(self.posts[0]['title'], 'My attempt at vore.')
        self.assertEqual(self.posts[1]['title'], '')
        self.assertEqual(self.posts[2]['title'], '')
        return
    def test_thread_attachments_alt_text(self):
        self.assertEqual(self.posts[0]['attachments'][0]['DOWNLOAD_NAME'], u'folly.jpg')
        return
    def test_thread_attachments_count(self):
        #print('attachment: {0!r}'.format(self.posts[0]['attachments']))
        self.assertEqual(len(self.posts[0]['attachments']), 1)
        self.assertEqual(self.posts[1]['attachments'], [])
        self.assertEqual(self.posts[2]['attachments'], [])
        self.assertEqual(self.posts[3]['attachments'], [])
        return
    def test_thread_attachments_dl_url(self):
        self.assertEqual(self.posts[0]['attachments'][0]['dl_url'], './download/file.php?id=630&amp;sid=9a7595219b9215d9c273b8c13457343b')
        return
## I don't know what this one is for anymore
##    def test_thread_attachments_title(self):
##        print('test_thread_attachments_title() self.posts: {0!r}'.format(self.posts))
##        self.assertEqual(self.posts[0]['attachments'][0]['title'], None)
##        return



class TestViewtopicAryionB38T44962(unittest.TestCase):
    """phpBB v3
    http://aryion.com/forum/viewtopic.php?f=55&t=11882&start=30"""
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
        self.assertEqual(len(self.posts), 15)
        return
    def test_thread_attachments_alt_text(self):
        self.assertEqual(self.posts[0]['attachments'][0]['DOWNLOAD_NAME'], u'folly.jpg')
        return
    def test_thread_attachments_count(self):
        #print('attachment: {0!r}'.format(self.posts[0]['attachments']))
        self.assertEqual(len(self.posts[0]['attachments']), 1)
        self.assertEqual(self.posts[1]['attachments'], None)
        self.assertEqual(self.posts[2]['attachments'], None)
        self.assertEqual(self.posts[3]['attachments'], None)
        return
    def test_thread_attachments_dl_url(self):
        self.assertEqual(self.posts[0]['attachments'][0]['dl_url'], './download/file.php?id=630&amp;sid=9a7595219b9215d9c273b8c13457343b')
        return
    def test_thread_attachments_title(self):
        self.assertEqual(self.posts[0]['attachments'][0]['title'], None)
        return





def main():
    unittest.main()

if __name__ == '__main__':
    main()
