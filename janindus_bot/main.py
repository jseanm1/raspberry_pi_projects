#!/usr/bin/env python

import os
import sys
import json
from twython import Twython

twitterAuthPath = os.getenv("HOME")+"/auth/twitter_auth.json"

print(twitterAuthPath)

with open(twitterAuthPath) as twitterAuthFile:
	twitterAuthData = json.load(twitterAuthFile)

api = Twython(twitterAuthData['consumer_api_key'], twitterAuthData['consumer_api_secret'], twitterAuthData['access_token'], twitterAuthData['access_token_secret'])

api.update_status(status=sys.argv[1])
