import sys

import numpy as np
import pandas as pd
import praw
from praw import Reddit

from utils.constants import POST_FIELDS


def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent)
        print("connected to reddit!")
        return reddit
    except Exception as e:
        print(e)
        sys.exit(1)

def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter: str, keywords, limit=None):
    subreddit = reddit_instance.subreddit(subreddit)
    posts = subreddit.new(limit=limit)

    post_lists = []
    keywords_lower = [keyword.lower() for keyword in keywords]  # Convert keywords to lower case for case insensitive matching

    for post in posts:
        title = post.title.lower()
        selftext = post.selftext.lower()
        # Check if any keyword is in the post's title or selftext
        if any(keyword in title or keyword in selftext for keyword in keywords_lower):
            post_dict = vars(post)
            post = {key: post_dict[key] for key in POST_FIELDS if key in post_dict}
            post_lists.append(post)

    return post_lists
    

def transform_data(post_df: pd.DataFrame):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    post_df['author'] = post_df['author'].astype(str)
    edited_mode = post_df['edited'].mode()
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]),
                                 post_df['edited'], edited_mode).astype(bool)
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    post_df['score'] = post_df['score'].astype(int)
    post_df['title'] = post_df['title'].astype(str)

    return post_df



def load_data_to_csv(data: pd.DataFrame, path: str):
    data.to_csv(path, index=False)
    
