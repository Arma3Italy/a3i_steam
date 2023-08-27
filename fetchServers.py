# from pymongo import MongoClient
import requests
import time
import math
import re

api_key = 'DB5703735A7F619DCA70D93000B9ABC4'
api_filter = '%5Cappid%5C107410%5Cname_match%5C*ita*' # search for all the servers with "ita" in the name
regex_filters = [ # regex filters are case insensitive: ita = ITA = Ita = itA
  "(^ita\\s)", # exemple: "ita superserver"
  "(\\sita\\s)", # exemple: "super ita server"
  "(\\s?italia\\s?)", # exemple: "super italia server" or "superitaliaserver"
  "(\[ita(\/[a-zA-Z]+)*\])", # exemple: "[ita]" or "[ita/eng]" or "[ita/eng/ger]"
]
api_server = 'https://api.steampowered.com/IGameServersService/GetServerList/v1/?key='+api_key+'&format=json&filter='+api_filter+'&limit=20000'
mongo_uri = 'mongodb+srv://admin:admin@arma3italy-eufgo.mongodb.net'
arma_tags = { 
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
arma_needer_tags = ['b', 'i', 'v', 't', 'o']

def filter_with_regex(filters, server_name):
  regex_string = '|'.join(filters)
  return re.search(regex_string, server_name, re.IGNORECASE)

def filter_json(jsonObj,nameP,valueP,valueR):
	for id in jsonObj:
		if id[nameP] == valueP:
			return id[valueR]
	return 0

def parse_tags(tagArray):
  tags = {'b':'null', 'i':'null', 'v':'null', 't':'null', 'o':'null'}
  for x in tagArray:
    if x != '':
      if x[0] in arma_needer_tags:
        tags[x[0]] = x[1:]

  return tags

def parse_server(server):
  tags = parse_tags(server['gametype'].split(',')) 

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

def get_online_servers():
  try:
    res = requests.get(api_server)
    res = res.json()
    res = res['response']['servers']
    res = list(filter(lambda x: filter_with_regex(regex_filters, x['name']), res))
    res = list(map(parse_server, res))
    return res
  except:
    print("[a3i_steam] > Error while fetching servers from steam")

def main():
  # client = MongoClient(mongo_uri)
  # coll_servers = client.test.servers
  # servers = list(coll_servers.find())

  # coll_servers.remove({})

  new_servers = get_online_servers()

  for server in new_servers:
    print(server['name'])
    # coll_servers.insert_one(server)
    # print("[AddedServer] > "+server['name']+" added")

main()