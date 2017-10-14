import requests
import json
import argparse

def print_stock(json_response, store_id, item_id):
	# formating...
	hyphensfront = ""
	hyphenback = ""
	if len(store_id) % 2 is 0:
		hyphensfront = "--------------------"[(len(store_id))/2:]
		hyphensback = hyphensfront
	else:
		hyphensfront = "--------------------"[(len(store_id)+1)/2:]
		hyphensback = hyphensfront + "-"
	print hyphensfront + " " + store_id + " " + hyphensback

	# print stock information
	try:
		print "stock status: " + str(json_response[item_id]["stores"][0]["status"])
		print "unit available: " + str(json_response[item_id]["stores"][0]["inventory"])
	except IndexError:
		print "request timeout or invalid response from server"

URL = 'https://www.walmart.ca/ws/en/products/availability'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

client = requests.session()
# Retrieve the CSRF token first
client.get(URL)  # sets cookie
csrftoken = client.cookies['walmart.csrf']

parser = argparse.ArgumentParser(description='Checks Walmart stocks for a given product in several stores', fromfile_prefix_chars='@')
parser.add_argument('--upc', help='UPC number of item', required=True)
parser.add_argument('--sku', help='sku number of item', default='')
parser.add_argument('--item_id', help='ID number of item', default='')
parser.add_argument('--stores', help='space separated store ids from which to check stock. Ex: --stores 3007 3008', nargs='+', required=True)

args = parser.parse_args()

for store_id in args.stores:
	payload = {'stores' : '["' + store_id + '"]', 'products' : '{"'+ args.item_id +'":[{"sku":"'+ args.sku +'","upc":["' + args.upc + '"]}]}' , 'csrfToken' : csrftoken, 'origin' : 'pip'}
	r = client.post(URL, params = payload, headers = headers)
	print_stock(json.loads(r.text), store_id, args.item_id)
