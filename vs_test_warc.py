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



USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
WPULL_PATH = 'wpull'



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



def run_wpull(output_path, url_list_path):

    warc_path = os.path.join(output_path, 'threads')

    db_path = os.path.join(output_path, 'thread.db')
    open(db_path, "w").close()# Create file

    wpull_log_path = os.path.join(output_path, "threads.log")
    open(wpull_log_path, "w").close()# Create file

    # Generate arguments to give to Wpull
    wpull_args = [
    WPULL_PATH,
    "--user-agent", USER_AGENT,
    "--output-file", wpull_log_path,
    "--no-robots",
    "--no-check-certificate",
    #"--load-cookies", os.path.join(os.getcwd(), 'dad_cookies.txt'),
    "--delete-after",# We only need the WARC file
    "--no-parent",
    "--database", db_path,
##    "--plugin-script", WPULL_HOOKS_SCRIPT,

    "--timeout", "60",
    "--tries", "inf",

    "--wait=2",# 2 seconds between requests seems slow enough to avoid problems
    "--random-wait",
    "--waitretry", "30",

    # https://github.com/chfoo/wpull/blob/0c20cb186d78ed4ac6ea8cd678d557e84afa3689/wpull/pipeline/item.py
    # Level ``1`` means the URL was linked from the top URL.
    # level (int): The recursive depth of this URL. A level of ``0``
    # indicates the URL was initially supplied to the program (the top URL).
    "--level", "0",#
##    "--page-requisites",#

    "--warc-file", warc_path,
    "--warc-append",
    "--warc-header", "operator: Anonarchive",
##    "--warc-header", "digiartistsdomain-img-dld-script-version: %s" % (VERSION),
##    "--warc-header", "digiartistsdomain-dld-script-sha1: %s" % (RUNNER_SHA1),# In case the version string is forgotten
##    #"--warc-header", "cyoc-dld-hooks-sha1: %s" % (WPULL_HOOKS_SHA1),
##    "--warc-header", "job_name: %s" % (job_name),

    '--input-file', url_list_path
    ]

    # Run the command
    logging.debug('wpull_args%r' % (wpull_args))
    subprocess.check_call(wpull_args)
    logging.debug('Finished running wpull')
    return


def save_threads(thread_info_filepath, output_path):
    with open(thread_info_filepath, 'rb') as jf:
        threads = json.loads(jf.read())

    # Ensure we can write to the URL list file
    url_list_path = os.path.join(output_path, 'thread.txt')

    if os.path.dirname(url_list_path) and (not os.path.exists(os.path.dirname(url_list_path))):
        os.makedirs(os.path.dirname(url_list_path))

    for thread in threads:
        logging.debug('thread: {0}'.format(thread))
        # Generate URL list file
        board_id = thread['board_id']
        thread_id = thread['topic_id']
        posts_per_page = thread['posts_per_page']
        pages = thread['pages']

        with open(url_list_path, 'a') as lf:
            for offset in range(0, pages*posts_per_page, posts_per_page):
                lf.write('https://www.phpbb.com/community/viewtopic.php?f={f}&t={t}&start={o}\n'.format(f=board_id,t=thread_id, o=offset))
                continue

    run_wpull(
        output_path=output_path,
        url_list_path=url_list_path,
    )

    return



def main():
    save_threads(
        thread_info_filepath='threads.json',
        output_path = 'warc_test'
    )
    return



if __name__ == '__main__':
    try:
        log_file_path=os.path.join('debug','vs_test_warc_log.txt')
        setup_logging(log_file_path)

        main()

        logging.info('Finished.')

    except Exception as e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)
        raise
