## Hacer concordancias 
import socket, sys, json, csv, urllib.request
import konlpy 
from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.utils import pprint 
from collections import Counter
import string, pickle

import numpy as np 

twitter = Twitter()
kkma = Kkma()

def saving(filename, l):
	with open("bin/"+filename, 'wb') as fp: 
		pickle.dump(l, fp);

def verbs( pos ): 
	l = [] 
	for i in pos: 
		if (i[1][0] == 'V'):
			a = i[0] + ("다")
			#pprint(a)
			l.append((a,i[1]))
	return l;

def adverbs( pos ): 
	l = [] 
	for i in pos: 
		if (i[1][0] == 'M'):
			l.append(i)
	return l;
	
def nouns( pos ): 
	l = [] 
	for i in pos: 
		if (i[1][0] == 'N'):
			l.append(i)
	return l;

def eomi( pos ): 
	l = [] 
	for i in pos: 
		if (i[1][0] == 'E'):
			l.append(i)
	return l;

def writetxt(file, l): 
	text_file = open( 'TEXT/'+ file+'.txt', "w")
	st = '\n'.join(map(str,l))
	text_file.write(st)
	text_file.close()

def extractname(k):
	l = [] 
	for i in k: 
		l.append(i[0])
	return l;


def generateDic( csv ):
	lines = []
	for row in csv:
		lines.append(row)
	
	headers = lines[0]
	ret = {}
	for i in lines: 
		ngram = i[0] 
		ngramSplit = ngram.split(';');
		data = {}
		index = 0
		for j in headers:
			if(index > 0):
				data[j] = i[index]
			index+=1
		
		ret[ngram]=data
	return ret

def loadDic( name ): 
	dic = open(name,'r');
	polc = generateDic(csv.reader(dic)); 
	
	print(polc[0]); 


def importJson(f):
	with open(f) as data_file: 
		data = json.load(data_file) 
	return data


def normalize(text):
	return twitter.normalize(text)
	
def parseData(data):
	return kkma.pos(data,True)

def max( data ):
	m = [0,''] # [ max, name]
	
	for i in data: 
		if(data[i] == None):
			data[i] = 0
		if (data[i] >= m[0]  ):
			 m[0] = data[i]
			 m[1] = i 
			 
	#print(m)
	return m
	
## Recibe una lista de tweets y devuelve la union de todos los textos en la lista de tweets 
def joinText(data):
	s = ''
	for i in data: 
		s += i['text']
	return s 


def polarize(data):  # Separa los Tweets en 2 partes 
	newData = {'pos': [] , 'neg': [], 'neut' : [], 'none' : [], 'com' : [] }
	
	for i in data:
		m = max( i['polarity'] )
		newData[m[1]].append(i) 
	
	return newData
	
# Devuelve el promedio de los atributos de analisis del texto KOSAC
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
	
## Que hashtags usan los tweets con polaridad 
## palabra mas frecuente, negativos, positivos 


def generatePARSE(filename, data):
	l = parseData(data)
	with open("GENERATE/"+filename, 'wb') as fp: 
		pickle.dump(l, fp);

def readingPARSE(filename):
	with open("GENERATE/"+ filename, 'rb') as fp: 
		l = pickle.load(fp);
	return l; 

def count(pos): 
	c = { 'nouns' : [], 'verbs' :[] ,'adverbs':[]}
	c['nouns'] = Counter(nouns(pos)).most_common()
	c['verbs'] = Counter(verbs(pos)).most_common()
	c['adverbs'] = Counter(adverbs(pos)).most_common()
	
	return c

## Genera los archivos de POS y Frecuencia
def GenerateFiles(names):
	TData = importJson("Target/2018-04-28.json")
	
	###### ALL 

	g#eneratePARSE("allPARSE", joinText(TData))
	allPOS = readingPARSE("allPARSE")
	print(allPOS)
	allCount = count(allPOS)
	for i in allCount: 
		writetxt(names+ 'all-' + i, allCount[i])
	
	polar = polarize(TData)
	
	###### POSITIVE
	#generatePARSE("posPARSE",joinText(polar['pos']))
	polarPOS = readingPARSE("posPARSE")
	polarCount = count(polarPOS)
	for i in polarCount: 
		writetxt( names + 'Positive-' + i , polarCount[i])
	
	
	###### NEGATIVE
	
	#generatePARSE("negPARSE",joinText(polar['neg']))
	polarNEG = readingPARSE("negPARSE")
	polarCount = count(polarNEG)
	for i in polarCount: 
		writetxt( names +  'Negative-' + i , polarCount[i])


###################################

def maxfavo(TData): 
	m = 0 
	
	for i in TData: 
		k = i['favorites']
		if ( k > m):
			m = k
			
	return m

	


	
TData = importJson("Target/2018-04-28.json")

sentAvg = getAverage(TData)

print(sentAvg)
#GenerateFiles(str(len(TData))+'/')

print("################################")
polar = polarize(TData)


a = polar['neg'][0]
for i in polar['neg']: 
	if (i['polarity']['neg'] < a['polarity']['neg'] ): 
		a = i 

print(a)

print("################################")

a = polar['pos'][0]
for i in polar['pos']: 
	if (i['polarity']['pos'] <  a['polarity']['pos'] ): 
		a = i 

print(a)

print("################################")

a = polar['neut'][0]
for i in polar['neut']: 
	if (i['polarity']['neut'] <  a['polarity']['neut'] ): 
		a = i 

print(a)
