import socket, sys, json, csv, urllib.request
import konlpy 
from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.utils import pprint 
from collections import Counter
import string, pickle

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

def importJson(f):
	with open(f) as data_file: 
		data = json.load(data_file) 
	return data
	
def exportJson(data):
	with open("DATA/geo3000.json", "w") as file:  
		json.dump(data, file)
		
def generateCredentials(): 
	credentials = {}  
	credentials['CONSUMER_KEY'] = 'W0C0F8SS7hLp5QpasoQsfU9Hd'
	credentials['CONSUMER_SECRET'] =  'bGikxlm0b2505jobYVHMt2xWBPUr7XfT86mZhUJCkWhII9fCYP'
	credentials['ACCESS_TOKEN'] = '157417608-mGVngRTiUtwy4flzdwKFPg5ldoZ1Dgkq4ScJcLcF'
	credentials['ACCESS_SECRET'] = 'hk28CE9e8elC4FOYVyfLSmWgtvApzpGe4CIo3wG77b6vV'

	# Save the credentials object to file
	with open("twitter_credentials.json", "w") as file:  
		json.dump(credentials, file)

def getGeo(TData): 
	credentials = {}  
	credentials['CONSUMER_KEY'] = 'W0C0F8SS7hLp5QpasoQsfU9Hd'
	credentials['CONSUMER_SECRET'] =  'bGikxlm0b2505jobYVHMt2xWBPUr7XfT86mZhUJCkWhII9fCYP'
	credentials['ACCESS_TOKEN'] = '157417608-mGVngRTiUtwy4flzdwKFPg5ldoZ1Dgkq4ScJcLcF'
	credentials['ACCESS_SECRET'] = 'hk28CE9e8elC4FOYVyfLSmWgtvApzpGe4CIo3wG77b6vV'

	twitter_stream = Twitter(auth=OAuth(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'], credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET']))

	geo = importJson("DATA/geo3000.json")

	index = 1
	
	j = 0
	while(TData[j]['id'] != geo[len(geo)-1]['id']):
			j += 1
	
	j+=1
	
	print(j)
	
	for k in range(j, len(TData)): 
		i = TData[k]
		
		if(i['id'] == '990227842444201984' or i['id'] == '990235323777957888' or i['id'] == '990233382930935809'):  
			continue
		
		idd= int(i['id'])
		print(idd)

		#twitter_stream.statuses.user_timeline(screen_name="jiapulidoar")
		user = twitter_stream.statuses.show(_id= idd)
		i['other'] =  {'geo': user['geo'] , 'location': user['user']['location'] , 'followers': user['user']['followers_count']} 
		
		if(len(i['other']['location']) != 0 or  i['other']['geo'] != None):
			print(i['other']['location'] + "!!" )
			geo.append(i)
		if( index%50 == 0):
			print('Guardando... ####################################################################')
			exportJson(geo)
		index += 1
		
		
		
## Hasta aqui 990268315292590082

def getAveragei( data, n , sentiment): 
	pol = {}
	Lfav =[] 
	LStat = []
	for i in data[0][sentiment]: 
		pol[i] = 0 

	npopulation = 0
	for i in range(0,n):
		npopulation += data[i]['favorites'] +1
		Lfav.append(data[i]['favorites'] +1)
		for l in pol: 
			#print(data[i][sentiment][l])
			if(l == 'pos'):
				LStat.append(data[i][sentiment][l])
			if(data[i][sentiment][l] == None):
				data[i][sentiment][l]=0

			pol[l] += data[i][sentiment][l] #* (data[i]['favorites'] + 1) 
			#print(str(pol[l]) + sentiment)
	
	print(npopulation)
	for i in pol: 
		pol[i]/=n
	return pol
		
def getAverage( TData): 
	avg = {'polarity' : {}, 'intensity':{}, 'expressive' :{}} 
	for i in avg:
		avg[i] = getAveragei(TData, len(TData), i)
		
	return avg;



TData = importJson("Target/2018-04-28.json")

geo = importJson("DATA/geo3000.json")

print(len(geo))

#getGeo(TData)

loc =[]
s = []
b = []
n = []


seoul = ["seoul","서울", "Seoul"]
busan = ["busan","부산", "Busan"]

for i in geo:
	if(len((i['other']['location'])) != 0):	 
		if ( i['other']['location'].find(seoul[0]) != -1 or i['other']['location'].find(seoul[1]) != -1  or i['other']['location'].find(seoul[2]) != -1):
			s.append(i)
		if ( i['other']['location'].find(busan[0]) != -1 or i['other']['location'].find(busan[1]) != -1  or i['other']['location'].find(busan[2]) != -1):
			b.append(i)
		if ( i['other']['location'].find("ork") != -1 or i['other']['location'].find("York") != -1 ):
			n.append(i)
		loc.append((i['other']['geo']))

print(getAverage(n))
