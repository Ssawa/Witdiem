import http.client
import hmac
import base64
import json
from pymongo import MongoClient
from hashlib import sha1
from random import random
from time import time
from urllib import parse

def oauthSignature(method, url, consumer_key, nonce, signature_method, timestamp, token, version, consumer_secret, token_secret):
	paramaters = "oauth_consumer_key=%s&oauth_nonce=%s&oauth_signature_method=%s&oauth_timestamp=%s&oauth_token=%s&oauth_version=%s&track=#witdiem" % (consumer_key, nonce, signature_method, timestamp, token, version)
	raw = method + "&" + parse.quote("https://stream.twitter.com/1.1/statuses/filter.json", safe='') + "&" + parse.quote(paramaters, safe='')
	signing_key = consumer_secret + "&" + token_secret
	hashed = hmac.new(signing_key.encode('utf-8'), raw.encode('utf-8'), sha1)
	return parse.quote(base64.b64encode(hashed.digest()).decode('utf-8'))

def twitterCall(method, url_host, url_path):
	consumer_key = "2XbFh5QMws8WhbTAOFROghIUZ"
	nonce = sha1(str(random()).encode('utf-8')).hexdigest()
	signature_method = "HMAC-SHA1"
	timestamp = str(int(time()))
	token = "2630663208-CZWWEjgNZRSG7ZNaYrVNvHxMikWytnezXAvqtpS"
	version = "1.0"
	consumer_secret = "9pioGyPnngcseWWfr90rrOjEDt5ITVkkydDS1X0LwKtv7UhB8E"
	token_secret = "MNI55rJ8YkRyYC4aQplkETZuCjtbl8RyjGEAk8FjWOvR9"
	signature = oauthSignature(method, "https://"+url_host+url_path, consumer_key, nonce, signature_method, timestamp, token, version, consumer_secret, token_secret)
	header = {"Authorization":'OAuth oauth_consumer_key="%s", oauth_nonce="%s", oauth_signature="%s", oauth_signature_method="%s", oauth_timestamp="%s", oauth_token="%s", oauth_version="%s"' % (consumer_key, nonce, signature, signature_method, timestamp, token, version)}
	conn = http.client.HTTPSConnection(url_host)
	conn.request(method, url_path, None, header)
	return conn.getresponse()

client = MongoClient()
db = client.witdiem
tweets = db.tweets

response = twitterCall("GET", "stream.twitter.com", "/1.1/statuses/filter.json?track=#witdiem")
print(response.status)
dataStream = b''
while not response.closed:
	byte = response.read(1)
	dataStream += byte
	if dataStream.endswith(b'\r\n') and dataStream.strip():
		print(dataStream.strip().decode())
		content = json.loads(dataStream.strip().decode('utf-8'))
		print(content)
		tweets.insert(content)
		dataStream = b''