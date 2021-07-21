from pymongo import MongoClient

uri = "mongodb://searchbot:search_kankhajura@cluster0-shard-00-00.6nsgq.mongodb.net:27017,cluster0-shard-00-01.6nsgq.mongodb.net:27017,cluster0-shard-00-02.6nsgq.mongodb.net:27017/mgd?ssl=true&replicaSet=atlas-3brzwx-shard-0&authSource=admin&retryWrites=true&w=majority"
mclient = MongoClient(uri)
mydb = mclient['UserSetting']
m_pref = mydb['pref']
wid = mydb['wid']

import re
pattern = re.compile(r'([aA-zZ]{2}).([aA-zZ]{3})')
default = 1

def get_wid(query,user_id = None):
	# check user pref then
	findin = ''
	w = None
	cc = False

	c = query.split('.') if '.' in query else query
	# print(f'{c=}')
	if (c.__class__ is list):
		x = pattern.match(query)
		# print(x)
		try:
			c = x.group()
		except AttributeError:
			pass
			# print('attributes')
		findin = 'cmd'
	elif len(c) == 2:
		findin = 'countryCode'
		cc = True
	elif len(c) > 2:
		findin = 'name'


	reg = {"$regex": f'^{c}',"$options":'i'}
	
	if cc is True:
		w = wid.find_one({findin:reg, 'placeType':'Country'},{'woeid':1,'name':1,'country':1})
	else:
		w = wid.find_one({findin:reg},{'woeid':1,'name':1,'country':1})
	
	# print(f' 1️⃣  {w=}' )
	
	if w is not None:
		return w
	else:
		return default
	# if (len(cmd.strip()) < 1) and (w := pref_exist(user_id)):
	# 	# w = w['woeid']  
	# 	return w['WOEID']
	# else:
	# 	if any(cmd.strip()) is False:
	# 		w = wid.find_one({'cmd':"in.in"},{'woeid':1 ,'name':1})
	# 		return w['woeid']
	# 	else:
	# 		w = wid.find_one({'cmd':cmd},{'woeid':1})
	# 		if w is not None:
	# 			return w['woeid']
	# 		else:
	# 			w = wid.find_one({'cmd':"in.in"},{'woeid':1})
	# 			return w

# city = {"$regex":^mum}
# db.all_woed.find({ "$and":[countrycode:in, name:city] }

def pref_exist(user_id):
	x = m_pref.find_one(user_id)
	if x is not None:
		return x
	else:
		x = wid.find_one({"placeType":"Country", "countryCode":"IN"},{'woeid':1,'name':1,"country":1})
		# print(f'{x=}')
		return x

# x = "in.hyd"
# x = x.split(".")

# print(get_trends(user_id=123456789, query=x))
