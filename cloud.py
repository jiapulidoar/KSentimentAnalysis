#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from collections import Counter
import urllib
import random
import webbrowser
from konlpy.utils import pprint
from konlpy.tag import Kkma
from lxml import html
import pytagcloud # requires Korean font support
import sys
import pickle 
if sys.version_info[0] >= 3:
    urlopen = urllib.request.urlopen
else:
    urlopen = urllib.urlopen


r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())

def reading(filename):
	with open(filename, 'rb') as fp: 
		l = pickle.load(fp);
	return l[3:]; 
	


def get_tags( nouns,ntags=50, multiplier=3):
    pprint(nouns)
    count = Counter(nouns)
    return [{ 'color': color(), 'tag': n, 'size': int(40 + c/200)}\
                for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Noto Sans CJK', size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    #webbrowser.open(filename)


def nouns( pos ): 
	l = [] 
	for i in pos: 
		if (i[1][0] == 'N'):
			l.append(i[0])
	return l;
	
def readingPARSE(filename):
	with open("GENERATE/"+ filename, 'rb') as fp: 
		l = pickle.load(fp);
	return l; 
	

## Genera los archivos de POS y Frecuencia
def GenerateFiles():	
	
	###### POSITIVE
	polarPOS = readingPARSE("posPARSE")
	pnouns = nouns(polarPOS)
	
	
	tags = get_tags(pnouns)
	draw_cloud(tags, 'wordcloudPOS.png')
	
	###### NEGATIVE
	
	#generatePARSE("negPARSE",joinText(polar['neg']))
	polarNEG = readingPARSE("negPARSE")
	nnouns = nouns(polarNEG)
	tags = get_tags(nnouns)
	draw_cloud(tags, 'wordcloudNeg.png')

GenerateFiles()

