# Code Listing #7

"""

Mocking/caching data to help debugging

NOTE: The code is for illustrative purposes only and will not execute.

"""

#import config
from redis import StrictRedis
import hashlib
import json, os
import random
import string
import itertools

search_api = 'http://api.%s(site)/listings/search'

# 存在しない
def get_api_key(site):
    """ Return API key for a site """

    # Assumes the configuration is available via a config module
    return config.get_key(site)

def unique_key(address, site):
    """ Return a unique key for the given arguments """

    # hashlib.md5(X).hexdigest() を idiom として覚えること
    return hashlib.md5(''.join((address['name'],
                               address['street'],
                               address['city'],
                               site)).encode('utf-8')).hexdigest()

# こういうのは標準にある。lru_cache() を factorial() のときに習った。
def memoize(func, ttl=86400):
    """ A memory caching decorator """

    # Local redis as in-memory cache
    # これが本コードのキモなのだが
    cache = StrictRedis(host='localhost', port=6379)

    def wrapper(*args, **kwargs):

        # Construct a unique cache filename
        key = unique_key(args[0], args[1])
        # Check if its in redis
        if cached_data := cache.get(key):
            print('=>from cache<=')
            return json.loads(cached_data)

        # Else calculate and store while putting a TTL
        result = func(*args, **kwargs)
        cache.set(key, json.dumps(result), ttl)

        return result

    return wrapper

def filecache(func):
    """ A file caching decorator """

    def wrapper(*args, **kwargs):

        # Construct a unique cache key
        filename = unique_key(args[0], args[1]) + '.data'
        if os.path.isfile(filename):
            print('=>from file<=')
            # Return data from file
            return json.load(open(filename))

        # Else compute and write into file
        result = func(*args, **kwargs)
        with open(filename, 'w') as f:
            json.dump(result, f)

        return result

    return wrapper

def api_search(address, site='yellowpages.com'):
    """ API to search for a given business address
    on a site and return results """

    req_params = {}
    req_params.update({
        'key': get_api_key(site),
        'term': address['name'],
        'searchloc': '{0}, {1}, {1}'.format(address['street'],
                                            address['city'],
                                            address['state'])})
    return requests.post(search_api % locals(),
                         params=req_params)


def parse_listings(addresses, sites):
    """ Given a list of addresses, fetch their listings
    for a given set of sites, parse them """

    for site in sites:
        for address in addresses:
            listing = api_search(address, site)
            # Process the listing
            process_listing(listing, site)

def process_listings(listing, site):
    """ Process listings function """

    # Not implemented
    # Some heavy computational code
    # whose details we are not interested in
    print('Processing listings')



@memoize
def func(address, site):
    return [str(x).upper() for x in address.values()]


if __name__ == "__main__":
    address = {'city': 'Elloree', 'name': 'Sure Shine', 'country': 'US', 'longitude': -80.5720318, 'phone': '8037077781', 'state': 'SC', 'street': '5543 Old Hwy 6', 'postal_code': '29047', 'latitude': 33.5309936, 'id': '84134184-03e8-4cf6-ae32-0ed63f92b568'}
    print(func(address, 'yellowpages.com'))
