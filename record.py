# this file will split the data into seperate records and then analyse these records based on our ai model
from bs4 import BeautifulSoup
from gensim.summarization import keywords
import re

def split(html, source):
	soup = BeautifulSoup(html, 'html.parser')

	posts = []

	if source == 'reddit':
		for h3 in soup.find_all('h3'):
			posts.append(h3.text)
	if source == 'twitter':
		allPosts = soup.find_all('span')
		for post in allPosts:
			if len(post.text) > 20:
				posts.append(post.text)
	if source == 'facebook': # TODO
		# for div in soup.find_all("script"):
		# 	div.decompose()
		for span in soup.find_all('span'):
			if len(span.text) > 35:
				if 'Advertentievoorkeuren' in span.text or 'Gesponsord' in span.text:
					span.decompose()
				else:
					posts.append(span.text)

	# print(posts)
	# filter out duplicates
	posts = list(dict.fromkeys(posts))

	return posts

def analyse(text):
	# load the list of words 
	# (English found here: https://finnaarupnielsen.wordpress.com/2011/03/16/afinn-a-new-word-list-for-sentiment-analysis/
	#  Dutch translated by me)
	afinn = dict()
	for line in open("AFINN-111.txt"):
		afinn[line.split('\t')[0]] = line.split('\t')[1]
	# do the analysis
	analysis = 0
	textWithoutPunctuation = re.sub(r'[^\w\s]', '', text)
	for word in textWithoutPunctuation.split():
		if word.lower() in afinn:
			value = afinn[word.lower()]
			analysis = int(analysis) + int(value)
	# collapse the number into 1, 0 or -1
	sentiment = 0
	print(textWithoutPunctuation, analysis)
	if analysis > 1:
		sentiment = 1
	if analysis < -1:
		sentiment = -1
	return sentiment

def analyseKeywords(text):
	meaninglessWords = ['met', 'uit', 'heeft', 'meer', 'tot', 'een', 'van', 'of', 'dit', 'dat', 'de', 'het', 'en', 'immers', 'omdat', 'daarom', 'omdat', 'namelijk', 'daardoor', 'doordat', 'ten', 'vervolgens', 'hierna', 'echter', 'maar', 'enerzijds', 'anderzijds', 'toch', 'omdat', 'want', 'hierdoor', 'aangezien', 'bijvoorbeeld', 'ter', 'kortom']
	temporaryResult = keywords(text).split('\n')
	result = []
	for word in temporaryResult:
		if word not in meaninglessWords:
			result.append(word)
	return result

def analyseEmotion(text):
	# TODO: analysis of emotion
	return 'happy'
