# Email Classification Model

## Purpose

This code was developed to create a model to classify emails (e.g., work, personal, ad, finance, spam, ...).

As with other model development, the steps are covered here are:
1. Data extraction/preparation
2. Manual classification
3. Model development (optionally includes predictive classification)

## Dependencies
The code will read directly from your mailserver to export the mailbox(es) you wish to use for model training. To avoid having to work around accessing email in different accounts with different vendors and different authentication schemes, I used my mail client to export my emails and loaded them in a customer email server for this purpose. Having copped out, I can't help with issues connecting to your email server.

As implemented, the code depends on the following libraries. Should you find tune the model, additional libraries may be required.

    import json
    import joblib
    import logging
    import pandas as pd
    import random
    import imaplib
    import email
    from email.header import decode_header, make_header
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import classification_report
    from sklearn.utils import resample

## Configuration
Before running, create a config.py from config_TEMPLATE.py by setting that constants for your environment.
    USERNAME = 'mailuser'
    PASSWORD = 'mailpassword'
    SERVER = 'mailservers'
    MAILBOXES = ['gmail', 'outlook']
    
    EXTRACT_BATCH_SIZE = 250
    CLASSIFY_BATCH_SIZE = 500
    
    # Set the labels you want to use below.    
    LABEL_MAP = {
        'ad': 0,
        'financial': 1,
        'personal': 2,
        'spam': 3,
        'work': 4,
    }
    
    LABEL_MAP2 = {
        'a': 'ad',
        'f': 'financial',
        'p': 'personal',
        's': 'spam',
        'w': 'work'
    }
    
    # Below is used for terminal prompting during manual classification.
    LABEL_MAP2_STR = 'a/f/p/s/w/. to backtrack, x to exit'
## Contents
### Code
* config.py
* extractEmailsAsJson.py
* manualClassify.py
* processEmails.py
* text_cleaner.py

### Data Files
Data files will be created and read from ./data folder.
* emails.json - output of extract_email_as_json
* classified_emails.json - output of manual_classify.py
* predicted_emails.json - optional output of process_emails

### Model Files
Model files will be created and read from ./model folder.
* email_classification_model.pkl
* vectorizer.pkl

## Creating Your Model
