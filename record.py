# this file will split the data into seperate records and then analyse these records based on our ai model
from bs4 import BeautifulSoup
import random

def split(html, source):
	soup = BeautifulSoup(html, 'html.parser')
	# temporary solution: this will need to be different based on the social media website that's the source etc etc

	posts = []

	if source == 'reddit':
		posts = soup.find_all('h3')
	if source == 'twitter':
		allPosts = soup.find_all('span')
		for post in allPosts:
			if len(post.text) > 20:
				posts.append(post)
				print(post.text)
	return posts

def analyse(html):
	# TODO: analysis
	analysis = round(random.uniform(-1, 1)) # temporary solution: random "analysis"
	return analysis

def analyseKeywords(html):
	# TODO: analysis of keywords
	return ['test', 'test2', 'test3']

def analyseEmotion(html):
	# TODO: analysis of emotion
	return 'happy'