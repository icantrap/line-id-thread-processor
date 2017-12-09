# LINE ID Thread Processor

This script scours the monthly LINE ID thread on [/r/TsumTsum](https://www.reddit.com/r/TsumTsum) via Reddit API and create a CSV file.

It was created with Python 3.

## Setup

1. Clone this repo.

2. Register an [script](https://www.reddit.com/prefs/apps) w/ Reddit.

3. Create a file __praw.ini__ with the appropriate values from the app creation, including changing the username in the `user_agent` property.

  ```
  [DEFAULT]
  client_id=abcde-12345678
  client_secret=mklkfmalikjocvomewp
  user_agent=praw:processor.py:v0.1:by /u/username
  ```

4. Install __pipenv__.

  ```bash
  $ pip3 install --user pipenv
  ```

5. Install dependencies

  ```bash
  $ pipenv install
  ```

## Execution

You need to find the id for the thread you want to process. The URL of the the November 2017 thread is

`https://www.reddit.com/r/TsumTsum/comments/7a19qw/november_2017_line_id_thread/`

The id is `7a19qw`.

Run

```bash
$ pipenv run ./processor.py 7a19qw
```

The file __line-id-thread.csv__ will be created. If the file already exists, then it will be overwritten.
