# -*-coding:utf8-*-

import requests
import bs4
import os
import os.path
import sys
import urllib
import unicodedata

address = 'http://www.lidown.com/'
code = {u'\u2022':u'·', u'\xbd':u'1/2', u'\u30fb':u'·', u'\xf6':u'o', u'\xf1':u'n', u'\u0469':u'', u'\u02a8':u'雪狮'}

directory = 'D:\\books\\Kindle'

def download(url, target):
	u = urllib2.urlopen(url)
	meta = u.info()
	file_size = int(meta.getheaders('Content-Length')[0])
	
	f = open(target, 'wb')
	
	downloaded_bytes = 0
	block_size = 1024*8
	while True:
		buffer = u.read(block_size)
		if not buffer:
			break
		
		f.write(buffer)
		downloaded_bytes += block_size
		print downloaded_bytes
	
	f.close()

def analysis(path, url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.content, 'lxml')
	for li in soup.select('ul#directory-listing li'):
		if '?dir=Book' in li.attrs.get('data-href') and '..' not in li.attrs.get('data-name'):
			name = li.attrs.get('data-name')
			temp = os.path.join(path, name)
			if not os.path.exists(temp):
				os.mkdir(temp)
			link = address + li.attrs.get('data-href')
			analysis(os.path.join(path, name), link)
		else:
			node = li.attrs.get('data-name')
			for (k,v) in  code.items():
				if k in node:
					node = node.replace(k, v)
			if not os.path.exists(os.path.join(path, node)):
				print os.path.join(path, node)
				download(address + li.attrs.get('data-href'), os.path.join(path, node))
		
analysis(directory, 'http://www.lidown.com/?dir=Book/%E7%B2%BE%E5%93%81%E4%B9%A6%E5%BA%93/Kindle%E4%BC%B4%E4%BE%A3%E7%B2%BE%E5%93%81%E4%B9%A6%E5%BA%93')
