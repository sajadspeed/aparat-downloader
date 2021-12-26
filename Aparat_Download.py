import requests
from bs4 import BeautifulSoup
import re
import os

downloadDir = "Downloads"

if os.path.isdir(downloadDir) == False:
    os.mkdir(downloadDir)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def downloadFile(url, name):
	path = downloadDir+"/"+name
	if os.path.isfile(path) == False:
		r = requests.get(url, allow_redirects=True)
		open(path, 'wb').write(r.content)

print("Paste your Aparat links in 'Links.txt'\n")

qualites = [0, 144, 240, 360, 480, 720, 1080, 99999]

for i in range(len(qualites)):
    quality = str(qualites[i])+"p"
    if qualites[i] == 0:
        quality = "Lowest quality"
    if qualites[i] == 99999:
        quality = "Highest quality"
    print(str(i+1) + " => " + str(quality))

qualityChoose = qualites[int(input("Choose your video download quality(like 6 for 720p): "))-1]
cls()
links = [line.rstrip() for line in open('Links.txt', 'r')]

for url in links:
	if len(url) > 6:
		response = requests.get(url)
		soup = BeautifulSoup(response.content, "html.parser")

		title = soup.find("h1").text

		downloadLinks = soup.find_all("li", {"class": "menu-item-link link"})

		finalDownloadLinks = []

		for downloadLink in downloadLinks:
			finalDownloadLinks.append([int(re.findall("\d+",downloadLink.a.span.text)[0]), downloadLink.a['href']])

		if len(finalDownloadLinks) > 0:
			finalDownloadLinks.sort(key=lambda row: row[0])

			finalDownloadLink = False

			for downloadLink in finalDownloadLinks:
				if qualityChoose <= downloadLink[0]:
					finalDownloadLink = downloadLink
					break

			if finalDownloadLink == False:
				finalDownloadLink = finalDownloadLinks[-1]
			
			print("Download("+str(finalDownloadLink[0])+"p)... " + title)
			downloadFile(finalDownloadLink[1], title+".mp4")
			
		else:
			print("Failed! " + title)

print("\nDownloaded videos in '"+downloadDir+"' Directory.\n")