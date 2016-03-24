import urllib
import urllib2
import string
import HTMLParser
from bs4 import BeautifulSoup
import re


def fetch_item(id):
	urlrequest = urllib2.Request('http://www.lifevc.com/item/' + id)
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	curitem_name = parser.find('h1', 'j-curitem-name')
	iname = curitem_name.text.strip()
	curitem_id = curitem_name.findNext('p', 'dt-brand').findAll('span')
	iid = re.search(r'\d+', curitem_id[1].text).group()
	curitem_price = curitem_name.findNext('p', 'price-wrap').findNext('span')
	iprice = re.search(ur'\xa5\d+', curitem_price.text).group()
	curitem_mprice = curitem_name.findNext('p', 'market-price')
	imprice = re.search(ur'\xa5\d+', curitem_mprice.text).group()

	print iname, iid, iprice, imprice

def fetch_channel(url):
	urlrequest = urllib2.Request(url)
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	channels = parser.findAll('a', {'target' : '_self'})
	for channel in channels:
		print channel.text.strip(), channel['href']

def fetch_slogan(url):
	urlrequest = urllib2.Request(url)
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	slogans = parser.findAll('h3')
	for slogan in slogans:
		print slogan.text

# fetch_item('19735')
# fetch_channel('http://www.lifevc.com')
fetch_slogan('http://www.lifevc.com')