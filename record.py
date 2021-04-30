# this file will split the data into seperate records and then analyse these records based on our ai model
from bs4 import BeautifulSoup
import random

def split(html):
	soup = BeautifulSoup(html, 'html.parser')
	# temporary solution: this will need to be different based on the social media website that's the source etc etc
	ps = soup.find_all('p')
	return ps

def analyse(html):
	# TODO: analysis
	analysis = random.uniform(-1, 1) # temporary solution: random "analysis"
	return analysis

def analyseKeywords(html):
	# TODO: analysis of keywords
	return ['test', 'test2', 'test3']

def analyseEmotion(html):
	# TODO: analysis of emotion
	return 'happy'