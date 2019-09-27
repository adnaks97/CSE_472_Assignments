import tweepy
import json

with open('twitter_credentials.json', "r") as file:
    cred = json.load(file)
    consumer = cred["CONSUMER_KEY"]
    consumer_secret = cred["CONSUMER_SECRET"]
    access = cred["ACCESS_KEY"]
    access_secret = cred["ACCESS_SECRET"]

auth = tweepy.OAuthHandler(consumer, consumer_secret)
auth.set_access_token(access, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=True)
user = api.get_user('skoct_13')
user.followers_count

followers = []
for user in tweepy.Cursor(api.followers, screen_name='imVkohli').items(50): # Set items for number of followers
    print user.name, user.screen_name
i=0
for friend in tweepy.Cursor(api.friends, screen_name='KingJames').items(150):
    print friend.screen_name
    i+=1
print i

len(friend.followers())
kohli = api.get_user('imVkohli')
kohli.friends_count

type(user) == type(friend)
s = api.get_user('KingJames')
len(s.followers())
len(s.friends())
len(user.friends())
for guy in user.followers():
    print guy.name

help(friend.friends)
for f in friend.friends():
    print f.screen_name

for friend in (user):
    print friend.name

import pickle
def load_dicts():
    with open('social_network.pkl', 'rb') as f:
        social_network = pickle.load(f)
    with open('id_map.pkl', 'rb') as f:
        id_map = pickle.load(f)
    return social_network, id_map

social_network, idx = load_dicts()

len(social_network)
len(idx)
social_network
social_network
