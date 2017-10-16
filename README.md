# walmart-inventory-lookup
## Description
Little python command-line tool to check a given product stock in some walmart stores.

## Installation
* Install python if it is not already on your system.
* Install requests package (http://docs.python-requests.org/en/master/user/install/#install)
* Install playsound package (https://pypi.python.org/pypi/playsound/1.2.1)
* Make sure alarm.mp3 is in the same directory as walmart_inventory_lookup

## Usage
walmart_inventory_lookup.py [-h] --upc UPC [--sku SKU] [--item_id ITEM_ID] --stores STORES [STORES ...] [--repeat MINUTE]


arguments:
* -h, --help :            show this help message and exit
* --upc UPC :             UPC number of item
* --sku SKU :             sku number of item
* --item_id ITEM_ID :     ID number of item
* --stores STORES [STORES ...] : Space separated store ids from which to check stock. Ex: --stores 3007 3008. Also accepts files, each stores ids in the file should be on a separate line.
* --repeat MINUTE : repeat the query every MINUTE minute

## Examples
* SNES mini classic inventory lookup
  * python walmart_inventory_lookup.py --sku 6000197536050 --item_id 6000197536049 --upc 4549659075 --stores 3008 5777 1208
* SNES mini classic inventory lookup using a file
  * python walmart_inventory_lookup.py --sku 6000197536050 --item_id 6000197536049 --upc 4549659075 --stores @stores.txt
* SNES mini classic inventory lookup which will be repeated every 10 minutes
  * python walmart_inventory_lookup.py --sku 6000197536050 --item_id 6000197536049 --upc 4549659075 --stores @stores.txt --repeat 10
