# import time
# import gspread
# gs = gspread.service_account()

# Open a sheet from a spreadsheet in one go
# top=5
# woied =11145
# print(f'Fetching: {time.strftime("%X")}')
# wks = gs.open("User Setting").sheet1
# wks.append_row([top,woied])
# print(f'Fetched: {time.strftime("%X")}')

# wks = wks.get_all_records()
# print(wks)

# mgd-908@annular-ocean-316014.iam.gserviceaccount.com
# telebot@telegram-316116.iam.gserviceaccount.com
# telegram-bot@telegram-316116.iam.gserviceaccount.com

from pymongo import MongoClient

uri = "mongodb://searchbot:search_kankhajura@cluster0-shard-00-00.6nsgq.mongodb.net:27017,cluster0-shard-00-01.6nsgq.mongodb.net:27017,cluster0-shard-00-02.6nsgq.mongodb.net:27017/mgd?ssl=true&replicaSet=atlas-3brzwx-shard-0&authSource=admin&retryWrites=true&w=majority"
mclient = MongoClient(uri)
mydb = mclient['UserSetting']
m_pref = mydb['pref']
woeid = mydb['woeid']



class Setting():

	def __init__(self,woeid=1,country='world'):
		super(Setting, self).__init__()
# 		print('➿ check db...id is ')
		# x = Setting.fetch(user_id)
		self.woeid = woied
		self.country = country
		# self.top = 10	
		# setAttr()

	def set(self, user_id, text):
		if text.isalpha() and len(text) == 2:
			res = woeid.find_one({"CountryCode":{'$regex': f'^{str(text)}$', '$options': 'i'},"Type":"Country" })
			print(res)
		elif text.isalpha() and len(text) > 2:
			res = woeid.find_one({"Name":{'$regex': f'^{str(text)}$', '$options': 'i'},"Type":"Country" })
			print(res)
		elif text.isdigit():
			res = woeid.find_one({"WOEID":int(text)})
			print(res)
		else:
			print('else')

		if res is None:
			return False

		country = res["Country"]
		wid = res["WOEID"]
		user_id = user_id

		if m_pref.find_one({"user_id":user_id}):
			Setting.update(user_id,wid,country)
		else:
			m_pref.insert_one({"user_id":user_id,"WOEID":wid, "country":country})
			print(f'added new {user_id=}, {wid=}, {country=}')
		return True
		# if m_pref.find_one({"user_id":user_id}):
		# 	m_pref.update_one({"user_id":user_id},{"$set":{"WOEID": wid}},upsert=False)
		# 	print('updated woeid ',wid)
		# else:
		# 	m_pref.insert_one({"user_id":user_id,"WOEID":wid, "country":country})
		# 	print(f'added new {user_id=}, {wid=}, {country=}')
		# return True


	def update(user_id,wid, country):
		m_pref.update_one({"user_id":user_id},{"$set":{"WOEID": wid, "country":country}},upsert=False)
		print('updated woeid ',wid)

	def add(user_id,wid,country):
		m_pref.insert_one({"user_id":user_id,"WOEID":wid, "country":country})
		print(f'added new {user_id=}, {wid=}, {country=}')

	def fetch(self,user_id):
		x = m_pref.find_one({"user_id":user_id})
		self.woeid = x['WOEID'] if x is not None else 1 
		self.country = x['country'] if x is not None else "World"

# def populate(data):
# 	status = woeid.insert_many(data)
# 	print(status)

# use this after extrecting woied
# x = api.trends_available()
# li = []
# for i in x:
#     data = {}
#     data = {
#         'Name': i["name"],
#         'Country': i["country"],
#         'WOEID': i["woeid"],
#         'Type': i["placeType"]["name"],
#         'CountryCode': i["countryCode"]
#     }




