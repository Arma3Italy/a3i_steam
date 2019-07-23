from pymongo import MongoClient
import requests as fetch
import time
import math
import re

api_key = '8E5D5A4C69D001BA20C1B71834DD0C56'
api_filter = '\\appid\\107410\\name_match\\*ita*'
regexFilters = "((^ita\\s)|(\\sita\\s)|(\\s?italia?\\s?)|(\\[ita(\/?[a-zA-Z]+)?\\]))"
api_server = 'https://api.steampowered.com/IGameServersService/GetServerList/v1/?key='+api_key+'&format=json&filter='+api_filter+'&limit=20000'
mongo_uri = 'mongodb+srv://admin:admin@arma3italy-eufgo.mongodb.net'

arma_tagsInsdex = { 
    'b': "battleEye",
    'r': "requiredversion",
    'n': "requiredbuildno",
    's': "serverstate",
    'i': "difficulty",
    'm': "equalmodpequired",
    'l': "lock",
    'v': "verifysignatures",
    'd': "dedicated",
    't': "gametype",
    'g': "language",
    'c': "longlat",
    'p': "platform",
    'h': "loadedcontenthash",
    'o': "country",
    'e': "timeleft",
    'j': "param1",
    'k': "param2",
    'f': "allowedfilepatching",
    'y': "island"
}
arma_neederTags = ['b', 'i', 'v', 't', 'o']


def filterJson(jsonObj,nameP,valueP,valueR):
	for id in jsonObj:
		if id[nameP] == valueP:
			return id[valueR]
	return 0

def parseTags(tagArray):
    tags = {'b':'null', 'i':'null', 'v':'null', 't':'null', 'o':'null'}
    for x in tagArray:
        if x != '':
            if x[0] in arma_neederTags:
                tags[x[0]] = x[1:]

    return tags

def parseServer(server):
    tags = parseTags(server['gametype'].split(',')) 

    os = 'linux'
    if server['os'] == "w": os = 'windows'

    return {
        'ip': server['addr'],
        'port': server['gameport'],
        'name': server['name'],
        'ply': server['players'],
        'maxPly': server['max_players'],
        'map': server.get('map', 'null'),
        'os': os,
        'battleEye': tags['b'],
        'difficulty': tags['i'],
        'verifysignatures': tags['v'],
        'gametype': tags['t'],
        'country': tags['o'],
        'lastUpdate': int(time.time()*1000.0)
    }

def getOnlineServers():
    res = fetch.get(api_server)
    res = res.json()
    res = res['response']['servers']
    res = list(filter(lambda x: re.search(regexFilters, x['name'], re.IGNORECASE),res))
    res = list(map(parseServer,res))

    return res

def main():
	# client = MongoClient(mongo_uri)
	# coll_users = client.test.users
	# users = list(coll_users.find())

    servers = getOnlineServers()
    
    print(servers)


main()