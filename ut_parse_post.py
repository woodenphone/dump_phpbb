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
import parse_post





class TestAryionPid5910(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=??&t=???? split to just have the post no 5910"""
    def setUp(self):
        self.post_id = 11882
        self.html_path = os.path.join('tests', 'single_posts', 'aryion', '5910.html')# has swf attachment
        with open(self.html_path, 'r') as f:
            self.html = f.read()
        self.pp = parse_post.Post()
        self.post = self.pp.parse_post(self.post_id, self.html)
        print('self.post: {0!r}'.format(self.post))
        return

    def test_post(self):
        # Correct attributes
        self.assertEqual(self.post['post_id'], 11882)
        self.assertEqual(self.post['title'], 'My attempt at vore.')
        self.assertEqual(self.post['username'], 'ress_q_puma')
        self.assertEqual(self.post['userid'], 958)
        self.assertEqual(self.post['time'], u'Fri Feb 10, 2006 10:48 pm')
        self.assertEqual(self.post['content'], u'<div class="content">Um...yeah...here it is. My first attempt at vore. Lemme know whatcha think. Huzzah.</div>')
        self.assertEqual(self.post['avatar_url'], None)
        self.assertEqual(len(self.post['attachments']), 1)
        self.assertEqual(self.post['attachments'][0]['COMMENT'], u'Yeah its vore...what else can I say. Partake and enjoy.')
        self.assertEqual(self.post['attachments'][0]['U_INLINE_LINK'], u'./download/file.php?id=630&amp;sid=9a7595219b9215d9c273b8c13457343b')
        self.assertEqual(self.post['attachments'][0]['SIZE_LANG'], u'KiB')
        self.assertEqual(self.post['attachments'][0]['FILESIZE'], u'99.12')
        self.assertEqual(self.post['attachments'][0]['DOWNLOAD_NAME'], u'folly.jpg')
        self.assertEqual(self.post['attachments'][0]['L_DOWNLOAD_COUNT'], 1231)
        self.assertEqual(self.post['attachments'][0]['type'], 'S_IMAGE')
        self.assertEqual(self.post['attachments'][0]['location'], 'attachbox')
        self.assertEqual(self.post['signature'], None)
        self.assertEqual(self.post['outer_html'], self.html)
        return



class TestAryionPid2404879(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=??&t=???? split to just have the post no 2404879"""
    def setUp(self):
        self.post_id = 2404879
        self.html_path = os.path.join('tests', 'single_posts', 'aryion', '2404879.html')# has swf attachment
        with open(self.html_path, 'r') as f:
            self.html = f.read()
        self.pp = parse_post.Post()
        self.post = self.pp.parse_post(self.post_id, self.html)
        print('self.post: {0!r}'.format(self.post))
        return

    def test_post(self):
        # Correct attributes
        self.assertEqual(self.post['post_id'], 2404879)
        self.assertEqual(self.post['title'], 'Re: requests for biscuts')
        self.assertEqual(self.post['username'], 'Aleksandrova')
        self.assertEqual(self.post['userid'], 60700)
        self.assertEqual(self.post['time'], u'Sun Dec 20, 2015 4:50 pm')
        self.assertEqual(self.post['content'], u'<div class="content"><!-- m --><a class="postlink" href="http://www.furaffinity.net/view/14386621/">http://www.furaffinity.net/view/14386621/</a><!-- m --> If I\'m not too big. Whatever you\'d like, just as long as she\'s the pred!</div>')
        self.assertEqual(self.post['avatar_url'], u'./download/file.php?avatar=60700_1419348820.jpg')
        self.assertEqual(len(self.post['attachments']), 0)
        self.assertEqual(self.post['signature'], None)
        self.assertEqual(self.post['outer_html'], self.html)
        return



class TestAryionPid2493048(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=??&t=???? split to just have the post no 2493048"""
    def setUp(self):
        self.post_id = 2493048
        self.html_path = os.path.join('tests', 'single_posts', 'aryion', '2493048.html')# has swf attachment
        with open(self.html_path, 'r') as f:
            self.html = f.read()
        self.pp = parse_post.Post()
        self.post = self.pp.parse_post(self.post_id, self.html)
        print('self.post: {0!r}'.format(self.post))
        return

    def test_post(self):
        # Correct attributes
        self.assertEqual(self.post['post_id'], 2493048)
        self.assertEqual(self.post['title'], 'Re: Rastus Stuff')
        self.assertEqual(self.post['username'], 'Erastus')
        self.assertEqual(self.post['userid'], 69773)
        self.assertEqual(self.post['time'], u'Wed Jun 29, 2016 2:21 pm')
        self.assertEqual(self.post['content'], u'<div class="content">something quick and simple i scribbled at work one day~  the "vore" aspect is up in the air, but meh it counts</div>')
        self.assertEqual(self.post['avatar_url'], u'./download/file.php?avatar=69773_1451382641.png')
        self.assertEqual(self.post['signature'], None)
        self.assertEqual(self.post['outer_html'], self.html)
        # Attachments
        self.assertEqual(len(self.post['attachments']), 1)
        self.assertEqual(self.post['attachments'][0]['COMMENT'], None)
        self.assertEqual(self.post['attachments'][0]['U_DOWNLOAD_LINK'], u'./download/file.php?id=158308')
        self.assertEqual(self.post['attachments'][0]['SIZE_LANG'], u'KiB')
        self.assertEqual(self.post['attachments'][0]['FILESIZE'], u'15.75')
        self.assertEqual(self.post['attachments'][0]['DOWNLOAD_NAME'], u'notepad6.docx')
        self.assertEqual(self.post['attachments'][0]['L_DOWNLOAD_COUNT'], 48)
        self.assertEqual(self.post['attachments'][0]['type'], 'S_FILE')
        self.assertEqual(self.post['attachments'][0]['location'], 'attachbox')
        return


class TestAryionPid470081(unittest.TestCase):
    """phpBB v3
    https://aryion.com/forum/viewtopic.php?f=??&t=???? split to just have the post no 470081"""
    def setUp(self):
        self.post_id = 470081
        self.html_path = os.path.join('tests', 'single_posts', 'aryion', '470081.html')# has swf attachment
        with open(self.html_path, 'r') as f:
            self.html = f.read()
        self.pp = parse_post.Post()
        self.post = self.pp.parse_post(self.post_id, self.html)
        print('self.post: {0!r}'.format(self.post))
        return

    def test_post(self):
        # Correct attributes
        self.assertEqual(self.post['post_id'], 470081)
        self.assertEqual(self.post['title'], 'First-person perspective (caution: explicit)')
        self.assertEqual(self.post['username'], 'dreamweevil')
        self.assertEqual(self.post['userid'], 8531)
        self.assertEqual(self.post['time'], u'Tue Jul 14, 2009 4:22 pm')
        #self.assertEqual(self.post['content'], '')
        self.assertEqual(self.post['avatar_url'], None)
        self.assertEqual(len(self.post['attachments']), 1)
        self.assertEqual(self.post['signature'], None)
        self.assertEqual(self.post['outer_html'], self.html)
        return









def main():
    unittest.main()

if __name__ == '__main__':
    main()