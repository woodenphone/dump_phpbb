#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     10/07/2016
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
from io import StringIO, BytesIO
from lxml import etree
#from bs4 import BeautifulSoup


file_path = os.path.join('debug','thread_page_response.htm')
with open(file_path, 'r') as f:
    page_html = f.read()


def main():
    pass

if __name__ == '__main__':
    main()
