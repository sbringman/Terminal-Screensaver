#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: engine.py
Author: Samuel Bringman
Date: 2025-11-12
Version: 1.0
Description: This program performs a random walk through Wikipedia links,
printing out the summary of each article it stops on.
License: MIT License

Wikipedia has a few policies for web scrappers, which are listed here:
https://wikitech.wikimedia.org/wiki/Robot_policy
Part of the policy is including contact information in the user_agent tag below.
So, it is recommended for the users of this program to include their email
in the web request below.
"""

# import required modules
import os
import helper_funcs as hf
import wikipediaapi
import datetime
import time
import logging
import requests
import argparse

# This is the argument parser, which takes command line arguments
parser = argparse.ArgumentParser(
                    prog='Wikipedia Random Walk Terminal Screensaver',
                    description='This program performs a random walk through Wikipedia links, '
                        'printing out the summary of each article it stops on.'
                    )

parser.add_argument('--start_title', 
                    default='Wikipedia:Unusual articles', 
                    help='Name of the Wikipedia article to start from')
parser.add_argument('--display_prev_walk', 
                    action='store_true', 
                    help='Instead of showing the terminal screensaver, display the '
                    'list of Wikipedia articles traversed in the previous random walk')

args = parser.parse_args()

# If only displaying the previous random walk, show that and exit
if args.display_prev_walk:
    hf.display_prev_walk()
    quit()

# Set up logging
logging.basicConfig(filename="./logs/article_path.log",
                    filemode='w')

logger = logging.getLogger()

# Set my logging to info
logger.setLevel(logging.INFO)

# Set the other loggers to warning
wikipediaapi.log.setLevel(level=wikipediaapi.logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Start logging
logger.info(f"{datetime.datetime.now()}")

# Set up the wikipedia api
wiki_wiki = wikipediaapi.Wikipedia(user_agent='Wikipedia_Screensaver_Bot/0.1 (your_email_here@email.com)',
                                    language='en')

# Have a starting page
page = wiki_wiki.page(args.start_title)
logger.info(f"{page.title}")

# Choose a random link and load the page
try: 
    page = hf.choose_page(wiki_wiki, page.title, logger)
except requests.exceptions.ConnectionError:
    print("ConnectionError: No Internet Connection detected.")
    quit()

# Upper cap of 1,000 articles
for i in range(1_000):

    # Get the terminal ready
    os.system('clear')
    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns

    # Get the ready text to print on the screen
    title = page.title
    summary = page.summary
    summary = hf.format_summary(summary, terminal_width)

    hf.print_title(title, terminal_width)
    print("", end='', flush=True)

    # Print the summary to the screen
    for j in range(len(summary)):

        print(summary[j], end='', flush=True)

        time.sleep(0.05)
    
    time.sleep(10)

    # Finished, so choose another article
    try:
        page = hf.choose_page(wiki_wiki, page.title, logger)
    except requests.exceptions.ConnectionError:
        print("ConnectionError: No Internet Connection detected.")
        quit()

    