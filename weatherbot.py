from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from lxml import html, etree
import requests
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

METEO_URL = 'http://www.meteosuisse.admin.ch'

print ('welcome weather geneva bot')

def start(bot, update):
	update.message.reply_text('/weather, /hello')


def hello(bot, update):
	update.message.reply_text(
		'Hello {}'.format(update.message.from_user.first_name))


def hello_weather(bot, update):
	weather = find_weather()
	content = weather_html(weather)
	reply_markup = InlineKeyboardMarkup(content)
	bot.send_message(
		chat_id=update.message.chat_id,
		text='Geneve Weather',
		reply_markup=reply_markup)


def find_weather():
	page = requests.get(METEO_URL +'/home.html')
	tree = html.fromstring(page.content)
	partial_link = tree.xpath('//section[@id="weather-widget"]/@data-json-url')[0]
	link = METEO_URL + partial_link
	data = requests.get(link).json()
	return data


def weather_html(content):
	current_temp = content['data']['current']['temperature']
	data_html = [
		[
			InlineKeyboardButton("now. ", callback_data='1'),
			InlineKeyboardButton(current_temp, callback_data='1')
		]
	]
	for item in content['data']['forecasts']:
		data_html.append([
				InlineKeyboardButton(item['day'], callback_data='1'),
				InlineKeyboardButton(item['temp_low'], callback_data='1'),
				InlineKeyboardButton(item['temp_high'], callback_data='1')
			]
		)

	return data_html

updater = Updater('379027298:AAHYRO2pADoUtAe-4-XhW2y_X2FQQ8VEWrM')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('weather', hello_weather))

updater.start_polling()
updater.idle()

