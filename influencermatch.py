import json
import requests

#### (0) YouTube video to audio ####
youTubeVideoURL = 'https://www.youtube.com/watch?v=G1IewlAi7dA'

url = 'https://savedeo.p.mashape.com/download'
headers = {'X-Mashape-Key':'Dvi9NfsyjImsh1zClAADpvjQ8ffap1xPDdvjsnESER3CoqG7Sl', 'Content-Type':'application/x-www-form-urlencoded', 'Accept':'application/json'}
data = {'url':youTubeVideoURL}
r = requests.post(url, data=data, headers=headers)

jsonObject = r.json()
jsonObject['formats'][20]

#### (1) YouTube get transcripts via their API ####
youTubeVideoID = 'U1e2VNtEqm4'
youTubeAPIKey = 'AIzaSyA1krd55qk1ftK2fODlHM3iVkMwbUEfHZI'
url = 'https://www.googleapis.com/youtube/v3/captions?videoId=%s&part=snippet&key=%s' % (youTubeVideoID, youTubeAPIKey)

#youtube-dl --write-auto-sub 'https://www.youtube.com/watch?v=T77frLL_bsg'

#### (NEW) Get caption from video (0) ####
#Command line
#youtube-dl --write-sub --sub-lang "en" 'https://www.youtube.com/watch?v=T77frLL_bsg'
# Use auto-sub to grab subtitles even for videos without human transcribed subtitles - not 100% perfect but fairly good
#youtube-dl --write-auto-sub --sub-lang "en" 'https://www.youtube.com/watch?v=evcrEskuB74'
#youtube-dl --write-auto-sub --sub-lang "en" 'https://www.youtube.com/watch?v=MKlvHOgId6s'

#### (NEW 1) For file in directory... ####
#### List of files in current directory ####
import os
files = [f for f in os.listdir('.') if os.path.isfile(f)]

import re
def cleanVTT(fileInPut):
	cleanFile = fileInPut[10:len(fileInPut)-2]
	cleanFileFinal = []
	for contentPiece in cleanFile:
		# If contentPiece == '', remove #
		if contentPiece == '':
			print 'blank, remove'
		# If contentPiece begins with time element - e.g., 00: remove #
		elif (contentPiece[0].isdigit() and contentPiece[1].isdigit()):
			print 'Number, remove'
		# Otherwise remove all elements within <> tags #
		else:
			cleanFileFinal.append(re.sub('<[^>]+>', '', contentPiece))
	return cleanFileFinal
#cleanVTT(content)

#### Clean text ####
for file in files:
	if file[len(file)-len("en.vtt"):] == "en.vtt":
		with open(file) as f:
			content = f.readlines()
			# you may also want to remove whitespace characters like `\n` at the end of each line
			content = [x.strip() for x in content]



#### (2) Compare text to list of products ####
#### 1 file ####
productList = ['cheetos', 'doritos', 'coke', 'pepsi', 'naturebox']
def productsRelevantInFile(cleanFileFinal, productList):
	cleanFileWithProducts = []
	for i in range(len(cleanFileFinal)):
		cleanFileWithProducts.append([cleanFileFinal[i],[]])
		for product in products:
			if product in cleanFileFinal[i].lower():
				cleanFileWithProducts[i][1].append(product)
	return cleanFileWithProducts

cleanFileWithProducts = productsRelevantInFile(cleanFileFinal, productList)

#cleanFileWithProducts = [['cheetos you want you are going to go', ['cheetos']],...,]

#### (3) Sentiment analysis on lines with products ####
def aggregateCleanFileWithProductsForSentimentAnalysis(cleanFileWithProducts):
	text = ""
	productListInFile = []
	for item in cleanFileWithProducts:
		text += item[0].lower()
		for product in item[1]:
			if product not in productListInFile:
				productListInFile.append(product)
	productListForBlueMix = ""
	for product in productListInFile:
		productListForBlueMix += product +"|"
	return text, productListForBlueMix, productListInFile

text, targets, productListInFile = aggregateCleanFileWithProductsForSentimentAnalysis(cleanFileWithProducts)

#text = "I like cheetos"
#targets = "cheetos"
blueMixAPIKey = '926c4ea84d51ada6eb8224f4f8be4e5d144330c2'
#url = 'https://gateway-a.watsonplatform.net/calls/text/TextGetTargetedEmotion?apikey=%s' % (blueMixAPIKey)
url = 'https://gateway-a.watsonplatform.net/calls/text/TextGetTargetedSentiment?apikey=%s' % (blueMixAPIKey)
data = {'outputMode':'json', 'text':text, 'targets':targets}
r = requests.post(url, data=data)
jsonObject = r.json()
jsonObject['results']