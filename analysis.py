import requests
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas 
import matplotlib.pyplot as plot

base_url = "http://api.genius.com"
headers = {'Authorization':'Bearer tzMDdaN3NMYI5PzD56pIAyFKy_nY7bt2aWnNcXyZOID0WT3mwh1sNOxPr-ueDOC1'}

song_title = input("Enter a song title: ")
artist_name = input("Enter the song's artist: ")

def get_lyrics(song_api_path):
	song_url = base_url + song_api_path
	response = requests.get(song_url, headers=headers)
	json = response.json()
	path = json["response"]["song"]["path"]
	page_url="https://genius.com" + path
	page = requests.get(page_url)
	html = BeautifulSoup(page.text, "html.parser")
	[h.extract() for h in html('script')]
	lyrics = html.find("div", class_="lyrics").get_text()
	lyrics = lyrics.lower().replace('\n', ' ')
	lyrics = re.sub("[\[].*?[\]]", "", lyrics)
	lyrics = re.sub(r'[^\w\s\']', '', lyrics)
	return re.sub(' +', ' ', lyrics)

#makes sure there is a file to store lyrics in (out.txt)
try: 
	file=open("out.txt", 'w')
except IOError:
	file=open(fn, 'w+')

#search for song, get lyrics and store in out.txt
if __name__ == "__main__":
	search_url = base_url + "/search"
	data = {'q': song_title}
	response = requests.get(search_url, params=data, headers=headers)
	json = response.json()
	song_info = None
	for hit in json["response"]["hits"]:
		if hit["result"]["primary_artist"]["name"] == artist_name:
			song_info = hit
			break
	if song_info:
		song_api_path = song_info["result"]["api_path"]
		file.write(get_lyrics(song_api_path).replace('\n', ' '))
		file.close()
		
#determine the sentiment of the song lyrics in out.txt
	dataframe = pandas.DataFrame(columns=('song', 'positive', 'neutral', 'negative'))
	analyzer = SentimentIntensityAnalyzer()
	i=0
	pos=0
	neg=0
	neu=0
	f=open("out.txt", 'rb')
	# fix file IO
	for sentence in f.readLines():
		this_sentence = sentence.decode('utf-8')
		comp = sid.polarity_scores(this_sentence)
		comp = comp['compound']
		if comp>=0.5:
			pos+=1
		elif comp>-0.5 and comp<0.5:
			neu +=1
		else:
			neg+=1
	tot = pos + neg + neu
	pc_neg = (neg/float(tot))*100
	pc_neu = (neu/float(tot))*100
	pc_pos = (pos/float(tot))*100
	dataframe.loc[i] = (song, percent_positive, percent_neutral, percent_negative)
	dataframe.plot.bar(x='song', stacked=True)
	plt.show()