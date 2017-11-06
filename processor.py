#!/usr/bin/env python

import csv

import praw

INTERNATIONAL_VERSION_STRINGS = { 'int', 'intl', "int'l", "int’l", 'international' }
JAPANESE_VERSION_STRINGS = { 'jp' }

def tryparse(comment):
    text = comment.body

    if text == '[deleted]':
        return None

    version = timeZone = None
    international = japanese = False

    for string in INTERNATIONAL_VERSION_STRINGS:
        if string in text.lower():
            international = True

    for string in JAPANESE_VERSION_STRINGS:
        if string in text.lower():
            japanese = True

    if international:
        version = 'Both' if japanese else "Int'l"
    elif japanese:
        version = 'JP'

    return { 'Version': version, 'Time Zone': timeZone, 'Text': text }

reddit = praw.Reddit()

# https://www.reddit.com/r/TsumTsum/comments/7a19qw/november_2017_line_id_thread/
# find a better way

submission = reddit.submission('7a19qw')

fieldNames = ['Version', 'Time Zone', 'Text']
with open('line-id-thread.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames = fieldNames)
    writer.writeheader()
    for top_level_comment in submission.comments:
        data = tryparse(top_level_comment)
        if data is not None:
            writer.writerow(data)
