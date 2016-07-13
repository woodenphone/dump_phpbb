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
# libs
from pyquery import PyQuery





class TopicParser():# TODO
    """Parser for threads"""
    def __init__(self, board_id, topic_id):
        self.topic = {}
        return

    def ParsePage(self, page_html, offset):
        return {}

    def GetThreadObj(self):
        return self.topic

class PostParser():# TODO
    """Parser for posts"""
    user_id = None

    def __init__(self, topic_page_html, post_id):
        self.topic_page_html = topic_page_html
        self.post_id = post_id
        # Parse the post
        self.post_userid = self.find_userid()
        return


    def find_userid(self):
        userid_path = '#p{pid} > div > div.postbody > p > strong > a'.format(pid=post_id)
        userid_element = d(userid_path)
        userid_html = userid_element.outer_html()
        userid = re.search('memberlist.php\?mode=viewprofile&amp;u=(\d+)', userid_html).group(1)
        return userid





def main():
    pass

if __name__ == '__main__':
    main()
