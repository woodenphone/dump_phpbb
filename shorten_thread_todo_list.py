#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     17/07/2016
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

# local



def main():
    """This does not care about numerical greaterthan or lessthan, only the position in the list"""
    list_path = os.path.join('threads.json')
    topic_id_to_crop_to = 0

    # Read
    with open(list_path, 'r') as f:
        data_in = json.loads(f.read())

    # Modify
    a = []
    b = []
    found_id = False
    for row in data_in:
        if found_id:
            b.append(row)
        else:
            a.append(row)
        if (row['topic_id'] == topic_id_to_crop_to):
            found_id = True
        continue

    if not found_id:# The ID wasn't there so we want everything kept
        data_out = a + b
    else:# We found the ID and want to discard those up-to and including it
        data_out = b

    # Write
    with open(list_path, 'r') as f:
        f.write(json.dumps(data_out))


    return

if __name__ == '__main__':
    main()