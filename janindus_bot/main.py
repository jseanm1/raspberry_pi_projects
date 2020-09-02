#!/usr/bin/env python

import os
import sys
import json
from twython import Twython
import requests
from PIL import Image, ImageDraw, ImageFont

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

def genImage(tweet, fname):
	W = 1000
	H = 800
	fsize = 32

	img = Image.new('RGB', (W,H), color=(51,51,51))

	fnt = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf', fsize)

	d = ImageDraw.Draw(img)

	w,h = d.textsize(tweet, font=fnt)
	d.text(((W-w)/2, (H-h)/2), tweet, align='center', font=fnt, fill=(240,250,0))

	img.save(fname)

def sendTweet(tweet, fname):
	twitterAuthPath = os.getenv('HOME')+'/auth/twitter_auth.json'

	with open(twitterAuthPath) as twitterAuthFile:		
		twitterAuthData = json.load(twitterAuthFile)

	api = Twython(twitterAuthData['consumer_api_key'], twitterAuthData['consumer_api_secret'], twitterAuthData['access_token'], twitterAuthData['access_token_secret'])

	img = open(fname, 'rb')
	res = api.upload_media(media=img)

	print(tweet)
	print(len(tweet))
	#api.update_status(status=tweet)
	api.update_status(status=tweet, media_ids=[res['media_id']])

hpbData = getHpbData()

hpbLocalTweet = genHpbLocalTweet(hpbData)
hpbGlobalTweet = genHpbGlobalTweet(hpbData)

genImage(hpbLocalTweet, 'local.jpg')
genImage(hpbGlobalTweet, 'global.jpg')

sendTweet(hpbLocalTweet, 'local.jpg')
sendTweet(hpbGlobalTweet, 'global.jpg')
