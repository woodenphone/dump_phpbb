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
# Libs
import requests
# Local
import process_threads




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


def save_threads(requests_session, thread_info_filepath, output_path):
    logging.debug('loading thread data from: {0}'.format(thread_info_filepath))
    with open(thread_info_filepath, 'rb') as f:
        threads = json.loads(f.read())
    logging.info('Processing threads...')
    skip_num = 59
    c = 0
    for thread in threads:
        c+= 1
        if c < skip_num:
            continue
        process_threads.process_thread(
            requests_session=requests_session,
            output_path=output_path,
            board_id=thread['board_id'],
            thread_id=thread['topic_id'],
            posts_per_page=thread['posts_per_page'],
            pages=thread['pages']
        )
        continue
    logging.info('Finished processing threads.')
    return


def main():
    # Init Requests session
    requests_session = requests.Session()
    save_threads(
        requests_session=requests_session,
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
        sys.exit(0)# Everything went fine.

    except Exception as e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)
        raise
    sys.exit(1)# Something went wrong.
