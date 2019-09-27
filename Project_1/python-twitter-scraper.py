import twitter
import json
from twython import Twython, TwythonRateLimitError, TwythonAuthError
import time
import pickle
import csv
import numpy as np

players = ['KingJames', 'stephenasmith', 'RealSkipBayless', 'SHAQ', 'MagicJohnson']
social_network = dict()
id_map = dict()

credentials_path = 'credentials/twitter_credentials.json' ## Create a Creddentials folder
with open(credentials_path, "r") as file:
    cred = json.load(file)
    consumer = cred["CONSUMER_KEY"]
    consumer_secret = cred["CONSUMER_SECRET"]
    access = cred["ACCESS_KEY"]
    access_secret = cred["ACCESS_SECRET"]

def get_player_followers():
    for player in players:
        row = []
        users = api.get_followers_list(screen_name=player, count=50)
        users = users['users']
        print player
        for user in users:
            row.append([user['id']])
            map_idx(user['id'],user['name'],user['screen_name'])
        s = player + '.csv'
        with open(s,'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(row)
        csvFile.close()

def init_api():
    api = Twython(consumer, consumer_secret, access, access_secret)
    return api

def handle_rate_limit(api):
    remainder = float(api.get_lastfunction_header('x-rate-limit-reset')) - time.time()
    print "RATE LIMIT EXCEEDED - SLEEPING for {} seconds".format(remainder)
    time.sleep(remainder + 3)
    api = init_api()
    print "AWAKE\n"
    return api

def load_dicts():
    try:
        with open('social_network.pkl', 'rb') as f:
            social_network = pickle.load(f)
        with open('id_map.pkl', 'rb') as f:
            id_map = pickle.load(f)
    except:
        social_network = dict()
        id_map = dict()
    return social_network, id_map

def dump():
    with open('social_network.pkl', 'wb') as f:
        print "Size of social network is {}".format(len(social_network))
        pickle.dump(social_network, f)
    with open('id_map.pkl', 'wb') as f:
        pickle.dump(id_map, f)

def clean_network(network):
    for id in network.keys():
        if len(network[id]) == 0:
            del network[id]
    return network

def map_idx(id, name, screen_name):
    id_map[id] = {'name':name, 'screen_name':screen_name}

def make_api_call(api, id):
    try:
        users = api.get_friends_ids(id=id)
    except TwythonRateLimitError:
        api = handle_rate_limit(api)
        return make_api_call(api, id=id)
    except TwythonAuthError:
        return -1
    return users

def add_user_to_network(id, api):
    users = make_api_call(api=api, id=id)
    if users == -1:
        print "Private acct"
        social_network[id] = []
        return
    social_network[id] = users['ids']
    #print "in"
    dump()

def get_player_details(api):
    player_details = api.get_friends_list(screen_name='shreesh73895021')
    for f in player_details['users']:
        map_idx(f['id'], f['name'], f['screen_name'])
        if int(f['id']) not in social_network.keys():
            add_user_to_network(f['id'], api)
    return player_details

if __name__ == "__main__":
    api = init_api()
    social_network, id_map = load_dicts()
    # get_player_followers() ## Run this line to get 50 followers for each player in a CSV
    for player in players:
        with open(player + '.csv','r') as f:
            reader = csv.reader(f)
            users = list(reader)
        for u in users:
            if int(u[0]) not in social_network.keys():
                add_user_to_network(int(u[0]), api)
        print "{} is completed".format(player)
    # len(social_network)
    # social_network
    # len(id_map)
    # id_map.keys()
    # id_map
    player_details = get_player_details(api)
    social_network = clean_network(social_network)
    #id_map
    #make_api_call(api, type='friend', id=u['id'])
    #followers = api.get_followers_list(screen_name='MagicJohnson', count=100)
    #lol = api.get_friends_ids(screen_name='MagicJohnson')
    #type(lol['ids'][0])
    #type(social_network.values()[0][0])
    #len(followers['users'])
    #len(friends['ids'])
    #lol = api.get_friends_l(id=u['id'])
    #api.get_lastfunction_header('x-rate-limit-remaining')
    #float(api.get_lastfunction_header('x-rate-limit-reset')) - time.time()
    #print(users['users'])
    #len(social_network)
    dump()
