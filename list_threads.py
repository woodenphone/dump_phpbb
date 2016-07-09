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
# libs
import requests
# local
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


def parse_threads_listing_page(html):
    # <a href="./viewtopic.php?f=86&amp;t=23065"
    thread_id_list = re.findall('<a\shref="./viewtopic.php\?f=\d+\&amp;t=(\d+)"', html, re.IGNORECASE | re.MULTILINE)
    logging.debug('parse_threads_listing_page() thread_id_list: {0}'.format(thread_id_list))
    return thread_id_list


def list_board_threads(requests_session, board_id, output_file_path):
    logging.info('Listing threads from board_id:{0} to output_file_path: {1}'.format(board_id, output_file_path))
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))

    thread_ids = []
    last_page_thread_ids = [None]
    for page_num in xrange(1, 500):# TODO: Increase to a few thousand after testing
        # Generate page URL
        offset = page_num*config.threads_per_page
        page_url = '{forum_base_url}/viewforum.php?f={board_id}&start={offset}'.format(
            forum_base_url=config.forum_base_url, board_id=board_id, offset=offset)

        # Load this page's threads
        thread_listing_response = fetch(
            requests_session,
            url=page_url,
            method='post',
            expect_status=200,
        )
        save_file(
            file_path = os.path.join("debug","thread_listing_response.html"),
            data = thread_listing_response.content,
            force_save = True,
            allow_fail = True
        )

        # Parse out thread IDs
        this_page_thread_ids = parse_threads_listing_page(html=thread_listing_response.content)
        thread_ids += this_page_thread_ids

        # Detect the end of the listing
        if (last_page_thread_ids == this_page_thread_ids):
            logging.info('Reached the end of the thread lisitng.')
            break
        else:
            last_page_thread_ids = this_page_thread_ids
        continue
    logging.debug('Found {0} threads.'.format(len(thread_ids)))
    # Write thread IDs to a file
    with open(output_file_path, 'w') as f:
        for thread_id in thread_ids:
            # board_id.thread_id\n
            f.write('{0}.{1}\n'.format(board_id, thread_id))

    logging.info('Listed threads from board_id:{0} to output_file_path: {1}'.format(board_id, output_file_path))
    return


def main():
    try:
        setup_logging(log_file_path=os.path.join('debug','list_threads_log.txt'))
##        # Accept CLI args
##        parser = argparse.ArgumentParser()
##        parser.add_argument('board_id', help='board_id',
##                        type=int)
##        args = parser.parse_args()
##        board_id = args.board_id
        board_id = 21

        # Init Requests session
        requests_session = requests.Session()

        # Log us in
        phpbb_login(requests_session)

        # List the threads in this subforum
        list_board_threads(
            requests_session=requests_session,
            board_id=board_id,
            output_file_path=os.path.join('debug', 'board_{0}_threads.txt'.format(board_id))
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
