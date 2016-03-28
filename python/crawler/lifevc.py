# -*- coding: utf-8 -*-

import urllib
import urllib2
import string
import HTMLParser
from bs4 import BeautifulSoup
import re
import xlwt
import json
from tqdm import tqdm


def fetch_item(id, output):
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

def fetch_channel(url, output):
	urlrequest = urllib2.Request(url)
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	channels = parser.findAll('a', {'target' : '_self'})
	for channel in channels:
		print channel.text.strip(), channel['href']

def fetch_slogan(url, output):
	urlrequest = urllib2.Request(url)
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	itemlist = parser.find('ul', 'FeaturedItemList').findAll('li', '')
	for item in itemlist:
		name = item.findNext('a')['title']
		uid =  re.search(r'\d+', item.findNext('a')['href']).group()
		churl = item.find('a', 'linkCat')['href']
		ch = churl[churl.rfind('/') + 1 : ].split('-')[0]
		subch = churl[churl.rfind('/') + 1 : ].split('-')[1]
		price = item.find('b', 'countPrice').text
		slogan = item.find('h3').text
		comment = re.search(r'\d+', item.find('span', 'recentSale').text.strip()).group()
		if not uid in output:
			subdict = {}
			subdict['name'] = name
			subdict['channel'] = ch
			subdict['subchannel'] = subch
			subdict['slogan'] = slogan
			subdict['price'] = price
			subdict['comment'] = comment
			output[uid] = subdict

def fetch_app_api(url, output):
	chlist = [2859, 2860, 2861, 2862, 2863, 2864, 2865, 2866]
	for ch in tqdm(chlist):
		jData = json.loads(urllib2.urlopen(urllib2.Request(url + str(ch))).read())
		cats = jData['InnerData']['Categories']
		for cat in cats:
			for item in cat['Items']:
				uid = item['ItemInfoId']
				if not uid in output:
					subdict = {}
					subdict['name'] = item['Name']
					subdict['channel'] = ch
					subdict['category'] = cat['Title'] + '-' + str(cat['ItemIndexId'])
					subdict['slogan'] = item['Appeal']
					subdict['price'] = item['SalePrice']
					subdict['comment'] = item['CommentCount']
					output[uid] = subdict

def main():
	vdict = {}
	wb = xlwt.Workbook()
	ws = wb.add_sheet('LifeVC Products')

	# fetch_item('19735')
	# fetch_channel('http://www.lifevc.com')
	# fetch_slogan('http://www.lifevc.com/Exh/Topic/SelectedNProducts', vdict)
	fetch_app_api('http://app.lifevc.com/1.0/v_ios_4.0.1_28/categories/Category?itemindexid=', vdict)

	i = 1
	for key in vdict:
		ws.write(i, 0, key)
		ws.write(i, 1, vdict[key]['name'])
		ws.write(i, 2, vdict[key]['slogan'])
		ws.write(i, 3, vdict[key]['price'])
		ws.write(i, 4, vdict[key]['channel'])
		ws.write(i, 5, vdict[key]['category'])
		ws.write(i, 6, vdict[key]['comment'])
		i += 1
	print len(vdict)
	wb.save('livevc.xls')

if __name__ == '__main__':
	main()
