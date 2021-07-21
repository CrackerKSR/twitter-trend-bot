import tweepy
from tweepy import OAuthHandler

consumer_key = 'BaD753vog7rygxpLtadm6bBpe'
consumer_secret = 'fR3IlwDumht4nV3HpBWQPxV1eTmyOXfA9NRSweuxBuHwAySgw7'
access_token = '2532009798-HdjyStZf5mY6VrQKiKkKA88INjghnGkHG2qovfU'
access_secret = 'ieu9aJcxwfP6w27Y5wU1xe8zuTi2G4kP6l9NKTtNe5FRS'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

import mongo

def get_trends(wid):
	tr = api.trends_place(wid if wid is not None and wid.__class__ is int else 1) # mumbai 2295411) #Nagpur- 2282863
	t= [[i for i in t['trends']] for t in tr]
	return t

def trends2(query,user_id=None):
	
	print(f' in trends() {query=}')

	wid = mongo.get_wid(query = query)
	
	print(f'in trends() after calling get_wid() {wid=}')
	
	tr = api.trends_place(wid if wid is not None and wid.__class__ is int else 1) # mumbai 2295411) #Nagpur- 2282863
	t= [[i for i in t['trends']] for t in tr]
	# print(f'in trends()  {t=}')
	# print(t[0][0])
	# print(user_id)
	return t
# def add_f():
# 	res = api.trends_available() # mumbai 2295411) #Nagpur- 2282863
# 	res=res[1:]
# 	c = 1
# 	cmd = ''
# 	li = []
# 	for i in res:
# 		c += 1 		
# 		if 'Town' in i['placeType']['name']:
# 			cmd = f'{i["countryCode"]}.{i["name"][:3]}'
# 		elif 'Country' in i['placeType']['name']: 
# 			cmd = f'{i["countryCode"]}.{i["countryCode"]}'
# 		i['cmd'] = cmd.lower()
		
# 		li.append({
# 		"cmd":cmd.lower(),
# 		"woeid":i["woeid"],
# 		"name":i["name"],
# 		"placeType":i["placeType"]['name'],
# 		"country":i["country"],
# 		"countryCode":i["countryCode"],
# 		})
# 	return li
# add_f()