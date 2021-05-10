# this file will split the data into seperate records and then analyse these records based on our ai model
from bs4 import BeautifulSoup
import random

def split(html, source):
	soup = BeautifulSoup(html, 'html.parser')

	posts = []

	if source == 'reddit':
		posts = soup.find_all('h3')
	if source == 'twitter':
		allPosts = soup.find_all('span')
		for post in allPosts:
			if len(post.text) > 20:
				posts.append(post)
	if source == 'facebook': # TODO
		print(html)
		
	return posts

def analyse(html):
	# load the list of words 
	# (English found here: https://finnaarupnielsen.wordpress.com/2011/03/16/afinn-a-new-word-list-for-sentiment-analysis/
	#  Dutch translated by me)
	afinn = dict()
	for line in open("AFINN-111.txt"):
		afinn[line.split('\t')[0]] = line.split('\t')[1]
	text = html.get_text()
	# do the analysis
	analysis = 0
	for word in text.split(' '):
		if word.lower() in afinn:
			value = afinn[word.lower()]
			analysis = int(analysis) + int(value)
	# collapse the number into 1, 0 or -1
	sentiment = 0
	print(text, analysis)
	if analysis > 1:
		sentiment = 1
	if analysis < -1:
		sentiment = -1
	return sentiment

def analyseKeywords(html):
	# TODO: analysis of keywords
	return ['test', 'test2', 'test3']

def analyseEmotion(html):
	# TODO: analysis of emotion
	return 'happy'