import requests
import json
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tdTagActive = False
		self.Users = []
		self.CurrentUser = []
	def handle_starttag(self, tag, attrs):
		if tag == "span":
			for attr in attrs:
				if attr[1] == 'ttext':
					self.tdTagActive = True
	
	def handle_endtag(self, tag):
		if self.tdTagActive and tag == "span":
			self.tdTagActive = False
			if len(self.CurrentUser) == 3:
				self.Users.append(self.CurrentUser)
				self.CurrentUser = []
	
	def handle_data(self, data):
		if self.tdTagActive and data != "":
			self.CurrentUser.append( data)
	def result(self):
		return self.Users

s = requests.Session()
s.auth = ('admin', 'XXXXXXXXXXXXXXXXX')
r = s.get('http://192.168.1.1/DEV_device.htm')
#print r.text
parser = MyHTMLParser()
parser.feed(r.text)
print json.dumps(parser.result())


