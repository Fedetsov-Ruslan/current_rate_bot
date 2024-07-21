import os
import redis.asyncio as redis
import json

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.aiohttp.aiohttp import fetch_xml, parse_xml


user_private_router = Router()
redis_client = redis.from_url("redis://redis:6379/0")


@user_private_router.message(CommandStart())
async def start(message: Message):
    await message.answer('Это бот по конвертации валют')

# конвертация валют через команду 
@user_private_router.message(Command('exchange'))
async def exchange(message: Message):
   request  = message.text.split()
   if len(request) != 4:
      await message.answer('Неверное количество параметров')
   else:
      try:         
         json_data = await redis_client.get(request[1])
         if json_data:
               data1 = json.loads(json_data)
         json_data = await redis_client.get(request[2])
         if json_data:
            data2 = json.loads(json_data)
         count = request[3]
         result = float(data1['VunitRate'].replace(',', '.')) * float(count) / float(data2['VunitRate'].replace(',', '.'))
         await message.answer(f"{result} {data2['Name']}")
      except:
         await message.answer('Неверное названия валют')

# вывод данных по команде  
@user_private_router.message(Command('rates'))
async def send_rates_command(message: Message):
   keys = await redis_client.keys('*')
   json_data_list =[json.loads(await redis_client.get(key)) for key in keys]
   # Форматируем данные для отправки клиенту
   response_text = "\n".join([f"{valute['CharCode']} {valute['Value']} рублей, за {valute['Nominal']} {valute['Name']}" for valute in json_data_list if valute['CharCode'] != 'RUB'])
   await message.answer(response_text)

# вывод данных по тексту
@user_private_router.message(F.text == 'rates')
async def rates(message: Message):
   keys = await redis_client.keys('*')
   json_data_list =[json.loads(await redis_client.get(key)) for key in keys]
   # Форматируем данные для отправки клиенту
   response_text = "\n".join([f"{valute['CharCode']} {valute['Value']} рублей, за {valute['Nominal']} {valute['Name']}" for valute in json_data_list])
   await message.answer(response_text)