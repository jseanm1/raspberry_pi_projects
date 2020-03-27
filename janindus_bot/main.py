#!/usr/bin/env python

import os
import sys
import json
from twython import Twython
import requests

def getHpbData():
	hpbEndpoint = 'https://www.hpb.health.gov.lk/api/get-current-statistical'

	hpbResponse = requests.get(url = hpbEndpoint)

	return hpbResponse.json()

def genHpbLocalTweet(hpbData):
	line1 = '#COVID19 SL Update ' + str(hpbData['data']['update_date_time']) + '\n'
	line2 = str(hpbData['data']['local_new_cases']) + ' new cases\n'
	line3 = str(hpbData['data']['local_total_cases']) + ' total cases\n'
	line4 = str(hpbData['data']['local_total_number_of_individuals_in_hospitals']) + ' in hospital\n'
	line5 = str(hpbData['data']['local_recovered']) + ' recovered\n'
	line6 = str(hpbData['data']['local_deaths']) + ' deaths\n'
	line7 = "Source : HPB API"

	return line1 + line2 + line3 + line4 + line5 + line6 + line7


def genHpbGlobalTweet(hpbData):
	line1 = '#COVID19 Global Update ' + str(hpbData['data']['update_date_time']) + '\n'
	line2 = str(hpbData['data']['global_new_cases']) + ' new cases\n'
	line3 = str(hpbData['data']['global_total_cases']) + ' total cases\n'
	line4 = str(hpbData['data']['global_recovered']) + ' recovered\n'
	line5 = str(hpbData['data']['global_deaths']) + ' deaths\n'
	line6 = "Source : HPB API"

	return line1 + line2 + line3 + line4 + line5 + line6

def sendTweet(tweet):
	twitterAuthPath = os.getenv('HOME')+'/auth/twitter_auth.json'

	with open(twitterAuthPath) as twitterAuthFile:		
		twitterAuthData = json.load(twitterAuthFile)

	api = Twython(twitterAuthData['consumer_api_key'], twitterAuthData['consumer_api_secret'], twitterAuthData['access_token'], twitterAuthData['access_token_secret'])

	print(tweet)
	print(len(tweet))
	api.update_status(status=tweet)

hpbData = getHpbData()

hpbLocalTweet = genHpbLocalTweet(hpbData)
hpbGlobalTweet = genHpbGlobalTweet(hpbData)

sendTweet(hpbLocalTweet)
sendTweet(hpbGlobalTweet)
