#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     09/07/2016
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
import json
# libs
import requests
#from bs4 import BeautifulSoup
# local
import parsers
import config



def setup_logging(log_file_path,timestamp_filename=True,max_log_size=104857600):
    """Setup logging (Before running any other code)
    http://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
    """
    assert( len(log_file_path) > 1 )
    assert( type(log_file_path) == type("") )
    global logger

    # Make sure output dir(s) exists
    log_file_folder =  os.path.dirname(log_file_path)
    if log_file_folder is not None:
        if not os.path.exists(log_file_folder):
            os.makedirs(log_file_folder)

    # Add timetamp for filename if needed
    if timestamp_filename:
        # http://stackoverflow.com/questions/8472413/add-utc-time-to-filename-python
        # '2015-06-30-13.44.15'
        timestamp_string = datetime.datetime.utcnow().strftime("%Y-%m-%d %H.%M.%S%Z")
        # Full log
        base, ext = os.path.splitext(log_file_path)
        log_file_path = base+"_"+timestamp_string+ext

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 2015-07-21 18:56:23,428 - t.11028 - INFO - ln.156 - Loading page 0 of posts for u'mlpgdraws.tumblr.com'
    formatter = logging.Formatter("%(asctime)s - t.%(thread)d - %(levelname)s - ln.%(lineno)d - %(message)s")

    # File 1, log everything
    # https://docs.python.org/2/library/logging.handlers.html
    # Rollover occurs whenever the current log file is nearly maxBytes in length; if either of maxBytes or backupCount is zero, rollover never occurs.
    fh = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        # https://en.wikipedia.org/wiki/Binary_prefix
        # 104857600 100MiB
        maxBytes=max_log_size,
        backupCount=10000,# Ten thousand should be enough to crash before we reach it.
        )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.info("Logging started.")
    return logger


def save_file(file_path,data,force_save=False,allow_fail=False):
    counter = 0
    while counter <= 10:
        counter += 1

        if not force_save:
            if os.path.exists(file_path):
                logging.debug("save_file()"" File already exists! "+repr(file_path))
                return
        foldername = os.path.dirname(file_path)
        if len(foldername) != 0:
            if not os.path.exists(foldername):
                try:
                    os.makedirs(foldername)
                except WindowsError, err:
                    pass
        try:
            file = open(file_path, "wb")
            file.write(data)
            file.close()
            return
        except IOError, err:
            logging.exception(err)
            logging.error(repr(file_path))
            time.sleep(1)
            continue
    logging.warning("save_file() Too many failed write attempts! "+repr(file_path))
    if allow_fail:
        return
    else:
        logging.critical("save_file() Passing on exception")
        logging.critical(repr(file_path))
        raise


def fetch(requests_session, url, method='get', data=None, expect_status=200, headers=None):
#    headers = {'user-agent': user_agent}
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
    if headers is None:
        headers = {'user-agent': user_agent}
    elif 'user-agent' not in headers.keys():
        headers['user-agent'] = user_agent

    if headers:
        headers.update(headers)

    for try_num in range(10):
        logging.debug('Fetch %s' % (url))
        if try_num > 1:
            time.sleep(try_num*30)# Back off a bit if something goes wrong

        try:
            if method == 'get':
                response = requests_session.get(url, headers=headers, timeout=300)
            elif method == 'post':
                response = requests_session.post(url, headers=headers, data=data, timeout=300)
            else:
                raise Exception('Unknown method')
        except requests.exceptions.Timeout, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.Timeout')
            continue
        except requests.exceptions.ConnectionError, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ConnectionError')
            continue
        except requests.exceptions.ChunkedEncodingError, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ChunkedEncodingError')
            continue

        save_file(
            file_path = os.path.join("debug","fetch_last_response.txt"),
            data = response.content,
            force_save = True,
            allow_fail = True
            )
##        if response.status_code == 404:
##            logging.error("fetch() 404 for url: %s" % url)
##            time.sleep(random.uniform(0.5, 1.5))
##            raise FetchGot404(url=url, response=response)

        if response.status_code != expect_status:
            logging.error('Expected status code: %s but got status code: %s . Sleeping.' % (expect_status, response.status_code))
            time.sleep(60*try_num)
        else:
            time.sleep(random.uniform(0.5, 1.5))
            return response

    raise Exception('Giving up!')


def phpbb_login(requests_session):
    logging.info('Logging in as {0}'.format(config.username))
    login_page_url = '{0}/ucp.php?mode=login'.format(config.forum_base_url)
    # Load login page
    # Send login request
    login_response = fetch(
        requests_session,
        url=login_page_url,
        method='post',
        expect_status=200,
        headers={
            'origin': config.site_base_url,
            'pragma': 'no-cache',
            'referer': '{0}ucp.php?mode=login'.format(config.forum_base_url),
            },
        data={
            'username': config.username,
            'password': config.password,
            'autologin': 'on',
            'viewonline': 'on',
            'redirect': '',
            'login': 'login',
            }
    )
    save_file(
        file_path = os.path.join("debug","login_response.html"),
        data = login_response.content,
        force_save = True,
        allow_fail = True
    )

    # Verify login worked
    assert(config.username in login_response.content)# Our username
    assert('/ucp.php?mode=logout' in login_response.content)# Logout link
    #assert('' not in login_response.content)# Login link
    logging.info('Logged in as {0}'.format(config.username))
    return


##def parse_thread_page(html):
##    """Extract data from each post on a thread page"""
##    page_soup = BeautifulSoup.BeautifulSoup(html)
##    bs_posts = page_soup.find_all(re.compile('div id = "p\d+"'))
##    posts = []
##    for bs_post in bs_posts:
##        post_html = str(bs_post)
##        post = {
##            'time_of_retreival':str(time.time()),
##            'post_time': None,
##            'board_id': re.search('<a\ href=\"./report\.php\?f\=(\d+)', post_html).group(1),
##            'thread_id': re.search('<h2><a\shref="./viewtopic.php\?f=21&amp;t=(\d+)">([^<]+)</a></h2>', page_html, re.MULTILINE|re.IGNORECASE).group(1),
##            'thread_title': re.search('<h2><a\shref="./viewtopic.php\?f=21&amp;t=(\d+)">([^<]+)</a></h2>', page_html, re.MULTILINE|re.IGNORECASE).group(2),
##            'post_id': re.search('id="p(\d+)"', post_html).group(1),
##            'post_html': post_html,
##
##        }
##        posts.append(post)
##        continue
##    logging.debug('repr(posts): {0}'.format(repr(posts)))
##    return posts


def check_if_locked(page_1_html):
    # Try to determine if topic is locked
    locked_element = t('[class~=locked]')
    locked_search = re.search('style="background-image: url(./styles/prosilver/imageset/topic_\w+_locked.gif)', row.outer_html())
    print('locked_search: {0!r}'.format(locked_search))
    if (locked_element or locked_search):
        return True
    else:
        return False


def process_thread(requests_session, board_id, thread_id, output_path, posts_per_page, pages,
    locked=None, thread_type=None, ):
    """Load each page of a thread and parse each page"""
    logging.info('Processing thread: {0} from board: {1}'.format(thread_id, board_id))
    assert(2000 > pages > 0)# Must be at least one page, and 2000 is unexpectedly high
    assert(posts_per_page > 0)# Zero is just silly.

    thread_filepath = os.path.join(output_path, 'b{b}'.format(b=board_id), 'b{b}.t{t}.json'.format(b=board_id, t=thread_id))

    thread = {}
    # Record thread-level information
    thread['grabbing_user'] = config.username
    thread['board_id'] = board_id
    thread['thread_id'] = thread_id
    thread['posts'] = []# Filled in later on in this function
    thread['locked'] = locked# We might get this in the args
    thread['thread_type'] = thread_type# We might get this in the args

    last_page_posts = []#
    # Process the posts in the thread
    for page_number in xrange(0, 2000):# 2K pages is unexpectedly high
        offset = page_number*posts_per_page
        # Load page
        page_url = '{forum_base_url}/viewtopic.php?f={board_id}&t={thread_id}&start={offset}'.format(
            forum_base_url=config.forum_base_url, board_id=board_id, thread_id=thread_id, offset=offset)
        thread_page_response = fetch(
            requests_session,
            url=page_url,
            method='get',
            data=None,
            expect_status=200,
            headers=None
        )
        save_file(
            file_path = os.path.join('debug', 'thread_page_response.htm'),
            data = thread_page_response.content,
            force_save = True,
            allow_fail = False
        )

        # Thread-level things
        if page_number == 0:
            # Determine if thread is locked
            if check_if_locked(page_1_html=thread_page_response.content):
                thread['locked'] = True# We might get this in the args
            else:
                thread['locked'] = False# We might get this in the args
            #


        # Parse post data from page
        this_page_posts = parsers.parse_thread_page(
            page_html=thread_page_response.content,
            board_id=board_id,
            topic_id=thread_id,
            offset=offset,
        )
        #logging.debug('this_page_posts: {0}'.format(this_page_posts))
        logging.debug('len(this_page_posts): {0}'.format(len(this_page_posts)))
        thread['posts'] += this_page_posts

        # Stop at the end of the thread
        for this_page_posts in this_page_posts:# Catch duplicate post IDs
            for last_page_post in last_page_posts:
                if this_page_post['post_id'] == last_page_post['post_id']:
                    logging.info('A post on this page has the same ID as one on the last, meaning were at the end of the thread')
                    logging.debug('this_page_post: {0}, last_page_post: {1}'.format(this_page_post, last_page_post))
                    break

        if (len(this_page_posts) < config.posts_per_page):# Catch unfilled page
            logging.info('This page had less than the maxumim posts per page and so is the last page.! No more pages to process for this topic.')
            break
##        elif (page_number >= pages):# Unreliable, posts could have been added since input data was collected
##            logging.info('Expected number of pages reached, {0} of {0}'.format(page_number, pages))
##            break
        continue

    # Save data to file
    #logging.debug('thread: {0!r}'.format(thread))
    save_file(
        file_path = thread_filepath,
        data = json.dumps(thread),
        force_save = True,
        allow_fail = False
    )

    logging.info('Processed thread: {0} from board: {1}'.format(thread_id, board_id))
    return


def process_threads(thread_info_filepath, output_path):
    with open(thread_info_filepath, 'rb') as f:
        threads = json.loads(f.read())
    c = 0
    for thread in threads:
        c += 1
        if c % 100 == 0:
            logging.info('{0} threads processed'.format(c))
        process_thread(
            output_path=output_path,
            board_id=thread['board_id'],
            thread_id=thread['topic_id'],
            posts_per_page=thread['posts_per_page'],
            pages=thread['pages']
        )
        continue
    return


def main():
    try:
        setup_logging(log_file_path=os.path.join('debug','process_threads_log.txt'))
##        # Accept CLI args
##        parser = argparse.ArgumentParser()
##        parser.add_argument('list_path', help='list_path',
##                        type=int)
##        args = parser.parse_args()
##        input_file_path = args.list_path
        input_file_path = os.path.join('debug', 'threads.json')

        # Init Requests session
        requests_session = requests.Session()

        # Log us in
        phpbb_login(requests_session)

        #process_thread(requests_session=requests_session, board_id=38, thread_id=45427, output_path=config.output_path)# debug

        # Process supplied threads
        process_threads(
            requests_session=requests_session,
            input_file_path=input_file_path,
            output_path=config.output_path
        )

        sys.exit(0)# Everything went fine.

    except Exception as e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)
        raise
    sys.exit(1)# Something went wrong.

if __name__ == '__main__':
    main()
