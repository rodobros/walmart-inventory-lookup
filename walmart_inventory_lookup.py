import requests
import json
import argparse
import time
import datetime

MIN_QUERY_FREQUENCY = 5 #one query every 5 minute maximum. We don't want to start DDOSing Walmart...

def beep():
	try:
		lib_playsound = __import__("playsound")
		lib_playsound.playsound('./alarm.mp3')
	except:
		print "ERROR: please download playsound python package for alarm"

def alert_stock(json_response, item_id):
	should_alert = False
	print "Query date: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	try:
		for store_info in json_response[item_id]["stores"]:
			if store_info["inventory"] > 0:
				print "  Store #" + str(store_info["storeNumber"]) + " seems to have stock:"
				print "    stock status: " + str(store_info["status"])
				print "    unit(s) available: " + str(store_info["inventory"])
				should_alert = True
	except IndexError:
		print "request timeout or invalid response from server"
	if should_alert:
		beep()
	else:
		print "  no stock in the Walmarts selected :("


def run_inventory_lookup(stores_id, item_id, sku, upc):
	URL = 'https://www.walmart.ca/ws/en/products/availability'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}

	client = requests.session()
	client.get(URL)
	csrftoken = client.cookies['walmart.csrf']

	payload = {'stores' : '["' + '", "'.join(stores_id) + '"]', 'products' : '{"'+ item_id +'":[{"sku":"'+ sku +'","upc":["' + upc + '"]}]}' , 'csrfToken' : csrftoken, 'origin' : 'pip'}
	r = client.post(URL, params = payload, headers = headers)
	alert_stock(json.loads(r.text), item_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks Walmart stocks for a given product in several stores', fromfile_prefix_chars='@')
    parser.add_argument('--upc', help='UPC number of item', required=True)
    parser.add_argument('--sku', help='sku number of item', default='')
    parser.add_argument('--item_id', help='ID number of item', default='')
    parser.add_argument('--stores', help='space separated store ids from which to check stock. Ex: --stores 3007 3008', nargs='+', required=True)
    parser.add_argument('--repeat', type=int, help='repeats the query every X minute. Ex: --repeat 15', default=0)

    args = parser.parse_args()

    repeat = True
    while repeat:
        run_inventory_lookup(args.stores, args.item_id, args.sku, args.upc)
        time.sleep(args.repeat*60)
        if args.repeat == 0:
            repeat = False

