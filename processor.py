import praw

reddit = praw.Reddit()

# https://www.reddit.com/r/TsumTsum/comments/7a19qw/november_2017_line_id_thread/
# find a better way

submission = reddit.submission('7a19qw')

for top_level_comment in submission.comments:
    print(top_level_comment.body)
    print('\n')
