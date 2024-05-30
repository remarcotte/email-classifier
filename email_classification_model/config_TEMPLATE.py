USERNAME = 'user'
PASSWORD = 'password'
SERVER = 'server'
MAILBOXES = ['INBOX', 'alt']

EXTRACT_BATCH_SIZE = 250
CLASSIFY_BATCH_SIZE = 500

LABEL_MAP = {
    'work': 0, 'personal': 1, 'ad': 2, 'financial': 3, 'spam': 4
}

LABEL_MAP2 = {
    'a': 'ad',
    'f': 'financial',
    'p': 'personal',
    's': 'spam',
    'w': 'work'
}

LABEL_MAP2_STR = 'a/f/p/s/w/. to backtrack, x to exit'
