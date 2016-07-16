#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     14/07/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# stdlib
import logging
import logging.handlers
import subprocess
import time
import datetime
import hashlib
import os
import random
import shutil
import argparse
import json



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



def process_thread(requests_session, board_id, thread_id, output_path):
    """Load each page of a thread and parse each page"""
    logging.info('Processing thread: {0} from board: {1}'.format(thread_id, board_id))

    thread_filepath = os.path.join(output_path, 'b{b}'.format(b=board_id), 'b{b}.t{t}.json'.format(b=board_id, t=thread_id))

    thread = {}
    # Record thread-level information
    thread['grabbing_user'] = config.username
    thread['board_id'] = board_id
    thread['thread_id'] = thread_id
    thread['posts'] = []# Filled in later on in this function

    # Process the posts in the thread
    for page_number in xrange(0, 2000):# 2K pages is unexpectedly high
        offset = page_number*config.posts_per_page
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
        if (len(this_page_posts) < config.posts_per_page):
##            logging.error('!DEBUG BREAK!')
            logging.info('This page had less than the maxumim posts per page and so is the last page.! No more pages to process for this topic.')
            break
        else:
            continue

    # Save data to file
    logging.debug('thread: {0!r}'.format(thread))
    save_file(
        file_path = thread_filepath,
        data = json.dumps(thread),
        force_save = True,
        allow_fail = False
    )

    logging.info('Processed thread: {0} from board: {1}'.format(thread_id, board_id))
    return

def save_threads(thread_info_filepath, output_path):
    with open(thread_info_filepath, 'rb') as f:
        threads = json.loads(f.read())
    for thread in threads:
        save_thread(
            output_path=output_path,
            board_id=thread['board_id'],
            thread_id=thread['topic_id'],
            posts_per_page=thread['posts_per_page'],
            pages=thread['pages']
        )
        continue
    return



def main():
    save_threads(
        thread_info_filepath='threads.json',
        output_path = 'json_test'
    )
    return



if __name__ == '__main__':
    try:
        log_file_path=os.path.join('debug','vs_test_json_log.txt')
        setup_logging(log_file_path)

        main()

        logging.info('Finished.')

    except Exception as e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)
        raise
