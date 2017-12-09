import requests
import couchdb
import time
import calendar
from HTMLParser import HTMLParser
class User(object):
	def __init__(self,ip,name,mac):
		self.ip = ip
		self.name = name
		self.mac = mac
		self.time = calendar.timegm(time.gmtime())
	def json(self):
		return {'ip':self.ip,'name':self.name,'mac':self.mac,'time':self.time}

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
				self.Users.append(User(self.CurrentUser[0],self.CurrentUser[1],self.CurrentUser[2]))
				self.CurrentUser = []
	def handle_data(self, data):
		if self.tdTagActive and data != "":
			self.CurrentUser.append( data)
	def result(self):
		return self.Users

s = requests.Session()
s.auth = ('admin', 'XXXXXXXXXXXX')
r = s.get('http://192.168.1.1/DEV_device.htm')
parser = MyHTMLParser()
parser.feed(r.text)
couch = couchdb.Server()
db = couch['brainynetwork']
for i,u in enumerate(parser.result()):
	db.save( u.json())
