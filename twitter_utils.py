import tweepy

from load_config import config

auth = tweepy.OAuthHandler(config['twitter']['consumer_key'], config['twitter']['consumer_secret'])
auth.set_access_token(config['my-tokens']['access_token'], config['my-tokens']['access_token_secret'])
api = tweepy.API(auth)


def get_user_timeline(screen_name):
    statuses = api.user_timeline(screen_name=screen_name, count=config['twitter']['count'], tweet_mode="extended",
                                 exclude_replies=True)
    return statuses

import re
re.sub(r'[a-zA-Z]{id}', '/{id}', '/andre/23/abobora/43435')