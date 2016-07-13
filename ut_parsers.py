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
        expected = {False}# TODO
        p = parsers.TopicParser()
        result = p.ParsePage(
            page_html=self.page_html,
            board_id=self.board_id,
            topic_id=self.topic_id,
            offset=self.offset
        )
        self.assertEqual(expected, result)
        return















def main():
    unittest.main()

if __name__ == '__main__':
    main()
