#!/usr/bin/env python

import csv
import re

import praw

INTERNATIONAL_VERSION_STRINGS = { 'int', 'intl', "int'l", "int’l", 'international' }
JAPANESE_VERSION_STRINGS = { 'jp', 'japan' }
BOTH_VERSIONS_STRINGS = { '(both)' }
OFFSET_PATTERN = re.compile('(?:UTC|GMT)\s*([+-]\d+)', re.IGNORECASE)

def tryparse(comment):
    text = comment.body

    if text == '[deleted]':
        return None

    version = offset = auto = unknown = None
    international = japanese = False

    for string in INTERNATIONAL_VERSION_STRINGS:
        if string in text.lower():
            international = True

    for string in JAPANESE_VERSION_STRINGS:
        if string in text.lower():
            japanese = True

    for string in BOTH_VERSIONS_STRINGS:
        if string in text.lower():
            international = True
            japanese = True

    if international:
        version = 'Both' if japanese else "Int'l"
    elif japanese:
        version = 'JP'

    if re.search(r'\bEST\b', text):
        offset = '-5'
    elif re.search(r'\bCST\b', text):
        offset = '-6'
    elif re.search(r'\bMST\b', text):
        offset = '-7'
    elif re.search(r'\bPST\b', text):
        offset = '-8'
    else:
        match = OFFSET_PATTERN.search(text)
        if match:
            offset = '%+d' % int(match.group(1))

    if 'auto' in text.lower():
        auto = 'yes'
    if 'manual' in text.lower():
        auto = 'no'

    if 'unknown' in text.lower():
        unknown = 'yes'

    return { 'Version': version, 'UTC Offset': offset, 'Auto': auto, 'Unknown': unknown, 'Text': text }

reddit = praw.Reddit()

# https://www.reddit.com/r/TsumTsum/comments/7a19qw/november_2017_line_id_thread/
# find a better way

submission = reddit.submission('7a19qw')

fieldNames = ['Version', 'UTC Offset', 'Auto', 'Unknown', 'Text']
with open('line-id-thread.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames = fieldNames)
    writer.writeheader()
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        data = tryparse(top_level_comment)
        if data is not None:
            writer.writerow(data)
