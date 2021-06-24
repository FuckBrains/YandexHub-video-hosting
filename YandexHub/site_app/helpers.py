# RANDOM
import random

# DATE/TIME
from datetime import datetime

# NETWORK
from urllib.request import urlopen

# JSON
import json

# UUID
import uuid 

# get random list
def random_list(x):
    random.shuffle(x)
    return x


# generate id for user, video...
def generate_id(num):
    # symbols = 'aSfzeKGhxAsBPYMECJmUwQgdcuRbXFHDkLvniytjNqpVWrTZ123456789'
    # key = ''.join(choice(symbols) for i in range(num))
    # return key
    return uuid.uuid4().hex[:int(num)].upper()


# get user IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# get info about IP
def get_ip_info(ip):
    url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    data = json.load(res)
    response = {}
    if 'country' in data:
        response['country'] = data['country']

    if 'city' in data:
        response['city'] = data['city']

    return response


# get city and country ip
def get_city_and_country_ip(request):
    ip = get_client_ip(request)
    now = datetime.now()
    date = now.strftime('%d-%m-%Y %H:%M:%S')
    ip_info = get_ip_info(ip)
    if 'country' in ip_info:
        country = ip_info['country']
    else:
        country = '???'

    if 'city' in ip_info:
        city = ip_info['city']
    else:
        city = '???'

    return f'Date: {date}\nIP: {ip}\nCountry: {country}\nCity: {city}'
