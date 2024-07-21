import redis.asyncio as redis
import xml.etree.ElementTree as ElementTree

import json


from aiohttp import ClientSession


redis_client = redis.from_url("redis://redis:6379/0")

async def fetch_xml():
    url = "https://cbr.ru/scripts/XML_daily.asp"
    async with ClientSession() as session:
        async with session.get(url) as response:
            xmlstr = await response.read()
            return xmlstr

async def update_redis_data():
    while True:
        xmlstr = await fetch_xml()
        
        root = ElementTree.XML(xmlstr) 
        currency_data_dict = {}
             
        for valute in root.findall('Valute'):
            currency_data = {
                'ID': valute.get('ID'),
                'NumCode': valute.find('NumCode').text,
                'CharCode': valute.find('CharCode').text,
                'Nominal': valute.find('Nominal').text,
                'Name': valute.find('Name').text,
                'Value': valute.find('Value').text,
                'VunitRate': valute.find('VunitRate').text,
            }
            json_data = json.dumps(currency_data)
            currency_data_dict[currency_data['CharCode']] = json_data
            await redis_client.mset(currency_data_dict)
        rus_current = {
            'ID': '1',
            'NumCode': '1',
            'CharCode': 'RUB',
            'Nominal': '1',
            'Name': 'Росийскийских рублей',
            'Value': '1',
            'VunitRate': '1,0',
        }
        json_data = json.dumps(rus_current)
        await redis_client.set(rus_current['CharCode'], json_data)
        return 

def parse_xml(xmlstr):
    root = ElementTree.XML(xmlstr)
    currencies = []

    for valute in root.findall('Valute'):
        currency_data = {
            'ID': valute.get('ID'),
            'NumCode': valute.find('NumCode').text,
            'CharCode': valute.find('CharCode').text,
            'Nominal': valute.find('Nominal').text,
            'Name': valute.find('Name').text,
            'Value': valute.find('Value').text,
            'VunitRate': valute.find('VunitRate').text,
        }
        currencies.append(currency_data)

    return currencies


