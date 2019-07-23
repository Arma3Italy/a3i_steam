from pymongo import MongoClient
import requests as fetch
import time
import math

# global variables
api_key = '8E5D5A4C69D001BA20C1B71834DD0C56'
api_gameinfo = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+api_key+'&format=json&steamid='
api_user = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+api_key+'&format=json&steamids='
mongo_uri = 'mongodb+srv://admin:admin@arma3italy-eufgo.mongodb.net'

# returns users data from steam, that are registered on mongodb
def getUsersData(users):
	users_id = []

	for user in users:
		steamid = user['steamid']
		users_id.append(steamid)

	users_ids = ','.join(users_id)
	
	res = fetch.get(api_user+users_ids)
	res = res.json()
	res = res['response']['players']

	return res

# search object(jsonObj) in an array by some name(keyP) and value(valueP) defined and returns the desire key(keyR) value
def filterJson(jsonObj,keyP,valueP,keyR):
	for id in jsonObj:
		if id[keyP] == valueP:
			return id[keyR]
	return 0

# returns the hour played on arma
def armaH(x):
	try:
		resAH = fetch.get(api_gameinfo+x)
		resAH = resAH.json()
		resAH = resAH['response']['games']

		hours = filterJson(resAH,'appid',107410,'playtime_forever')

		return math.floor(hours/60)
	except :
		return 0

# returns only needed data from steam api
def filterUsers(x):
	return {
		'steamid': x['steamid'],
		'name': x['personaname'],
		'avatar': x['avatarfull'],
		'armaHours': armaH(x['steamid']),
		'url': x['profileurl'],
		'ownedServer': [],
		'update': int(time.time()*1000.0)
	}

def main():
	# connection to the database
	client = MongoClient(mongo_uri)

	# select of the desired collection
	coll_users = client.test.users

	# getting all users of the db
	users = list(coll_users.find())

	# updating users data
	usersData = getUsersData(users)

	# parsing returned users data from steam
	newUsers = list(map(filterUsers,usersData))

	# sending updated data to db
	for usr in newUsers:
		userfilter = { 'steamid': usr['steamid'] }
		userUpdate = {
			"$set": {
					"name": usr['name'],
					"avatar": usr['avatar'],
					"armaHours": usr['armaHours'],
					"url": usr['url'],
					"ownedServer": usr['ownedServer'],
					"update": usr['update'],
				}
		}
		coll_users.update_one(userfilter,userUpdate)

		print("[UserUpdaterBot] > "+usr['name']+" updated")