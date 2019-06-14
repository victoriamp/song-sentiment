import requests
from bs4 import BeautifulSoup

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
	lyrics.replace('\n', ' ')
	return lyrics

try: 
	file=open("out.txt", 'w')
except IOError:
	file=open(fn, 'w+')

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