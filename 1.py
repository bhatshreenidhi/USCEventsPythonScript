from lxml import html
import requests
import bs4
from USCCinemaEvents import USCCinemaEvents

#This is the main url
rootUrl = 'http://cinema.usc.edu'

#Stores the events
eventList = []

#Get the response from the main URL
response = requests.get(rootUrl + "/events/")
#Use the library to get the HTML String
document = bs4.BeautifulSoup(response.text)


#<ul class = "eventListing">
	#<li>
	#	<a ---- class = "eventImg">
	#		<img src="">
	#	</a>
	#	<a>
	#	</a>
	#	</li>
	#<li></li>
	#</ul>

ulValues = document.find('ul',{"class":"eventListing"})


# Loop through the first Hyperlink to find out the ImageLink and the description page link
aValues = ulValues.findAll('a',{"class":"eventImg"})
eventCount = 0
for img in aValues:
	cinemaEvent = USCCinemaEvents("","","","",rootUrl + img.find('img').get('src'),"","","","",rootUrl + img.get('href'),"",img.get('href').split('=')[1])
	eventList.append(cinemaEvent)

#Find all the anchor tags in UL
ulValues = document.find('ul',{"class":"eventListing"})
aValues = ulValues.findAll('a')

# This loop scrapes through TITLE<SUMMARY<DATETIME<LOCATION from the page

for event in eventList:
	val = (aValues[eventCount+1].get_text().split('\n'))
	lineCount = 0
	eventCount = eventCount + 2
	for i in val:
		lineCount = lineCount + 1
		if(lineCount==3):
			event.title = i.strip()
		if(lineCount == 4) :
			event.dateTime = i.strip()
		if(lineCount == 5) :
			event.location = i.strip()
		if(lineCount == 7 ):
			event.summary = i.strip()
			lineCount = 0
#Go to the Details page and scrape through other information
for event in eventList:
	
	#Get the response from the details page URL
	response = requests.get(event.USCDetailPage)
	#Use the library to get the HTML String
	document = bs4.BeautifulSoup(response.text)

	#Youtube link
	videoUrl = document.findAll('iframe')
	if(videoUrl):
		event.videoUrl = videoUrl[0].get('src')[2:]
		event.eventType = 'movie'

	#Detail Page Image Link
	division = document.find('div',{'class':'imgLeft width200'})
	if(division):
		event.detailImgUrl = division.find('img').get('src')

	#Reservation Website link
	division = document.find('p',{'class':'reservation'})
	if(division):
		event.reservationUrl = rootUrl + division.find('a').get('href')

	#print event.title	



