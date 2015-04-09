import json
import urllib2
import time
import random
import multiprocessing

dictionary = {}
pages = range(2,1446)

MULTIPROCESSING = False #TODO do without blocking. Simple at first

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/4.61 [ja] (X11; I; Linux 2.6.13-33cmc1 i686)',
    'Opera/9.63 (X11; Linux x86_64; U; ru) Presto/2.1.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20100121 Firefox/3.5.6 Wyzo/3.5.6.1'
]

def safetyMeasures(wait_time):
    version = random.choice(user_agents)
    header = { 'User-Agent' : version }
    time.sleep(random.randint(0,wait_time))
    return header

def pageGetter(website,time):
    header = safetyMeasures(time)
    req = urllib2.Request(website,headers = header)
    soup = urllib2.urlopen(req).read()
    return soup

def scraper(page):
	sleep_time = random.randint(0,10)
	#oldlink = "https://reverb.com/api/listings?&page="+page+"&per_page=50"
	link = "https://reverb.com/api/listings.json?query=guitar&page="+str(page)+"&per_page=50"
	print 'waiting '+str(sleep_time)+' seconds'
	jsonDic = json.loads(pageGetter(link,sleep_time))
	print 'loading page_num: '+str(page)
	####jsonDic = json.loads(urllib2.urlopen(link).read())
	rangeLimit = len(jsonDic['listings'])
	#important information #Y-train
	# sum of info u'title': u'Gibson Les Paul Smartwood 1999 Natural'
	# u'year': u'1999'
	# u'finish': u'Natural',
	# u'make': u'Gibson',
	# u'model': u'Les Paul Smartwood'
	# u'price {u'amount': u'1250.00', u'currency': u'USD', u'symbol': u'$'}

	for index in range(0,rangeLimit):
		#for hashing 
		index_number = page+index
		dictionary[index_number] = {'data':{'x':'','y':''}}

		#establish y
		y = {}
		####TODO add try cates for missing values. must have make, model, price.
		try:
			y['year'] = jsonDic['listings'][index]['year']
		except:
			y['year'] = 0
		try:
			y['finish'] = jsonDic['listings'][index]['finish']
		except:
			y['finish'] = 0
		y['make'] = jsonDic['listings'][index]['make']
		y['model'] = jsonDic['listings'][index]['model']
		y['price'] = jsonDic['listings'][index]['price']


		#import information #X-train
		x={}
		#first 2 photos matter. are big and are of front of guitar.
		# {u'_links': {u'full': {u'href': u'https://reve.....
		photos = []
		photoRange = len(jsonDic['listings'][index]['photos'])
		for pIndex in range(0,photoRange):
			if pIndex>1:
				break
			photo = jsonDic['listings'][index]['photos'][pIndex]['_links']['full']['href']
			photos.append(photo)
		x['photos'] = photos

		#collect information
		dictionary[index_number]['data']['x'] = x
		dictionary[index_number]['data']['y'] = y
	print 'finished with page_num: '+str(page)
	print 'saving dump'
	pickle.dump(dictionary,open('reverb.p','wb'))

for i in pages:
	scraper(i)



