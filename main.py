import requests
import json
from datetime import datetime, timedelta, date
import time
from matplotlib import pyplot as plt
import telebot

token = "token"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'Hello! I can:\n' +  
        'Show latest exchange for CURrency: type /lst. \n'
        'Exchange one currency to another: type /exchange .\n' 
        'Show historic exchange for 2 currencies last 7 days: type /history. \n'
        'I am case and syntax sensitive. So type exactly as command first response suggests. \n'
        'There is no help, only /start. So if you need a reminder - let us start anew.'
)

url_spec = 'https://api.exchangeratesapi.io/latest?base=' #Specified URL for exchange

@bot.message_handler(commands=["lst"])
def lst_command(message):
    currency = bot.reply_to(message, "Type currency ABV. Example: USD")
    bot.register_next_step_handler(currency, process_lst)

def process_lst(message): #Receiving user input
    currency = message.text
    lst_dict = load_data(url_spec+str(currency)) #Load exc.rates as a dict
    for currencies, rates in lst_dict.items(): #Iterating for outer dictionary
        for value in rates: #Iterating in inner dictionary
            try: #Ignoring last part of outer dictionary received by API request
                currency_value = value + ":" + str(round(rates[value], 2))
                bot.send_message(message.chat.id, currency_value) #Returns two rows: currency and rate, rounded.
            except TypeError:
                pass
    return lst_dict

def load_data(url): #Loads data provided by specified url
    return json.loads(requests.get(url).text)

@bot.message_handler(commands=["exchange"])
def exchange_command(message):
    exchange_data = bot.reply_to(message, "Type: [base currency ABV], [exchange currency ABV], [amount]. Example: USD, CAD, 200")
    bot.register_next_step_handler(exchange_data, process_exchange)

def process_exchange(message): #Receiving user input
    exchange = message.text
    try: #Catching exceptions
        currency_from = exchange[0:3] #Extracting required arguments from user input
        currency_to = exchange[5:8]
        amount = float(exchange[10:])
        url = 'https://api.exchangeratesapi.io/latest?base='+str(currency_from) #Changes base currency accordingly
        exchange_dict = load_data(url)
        exchange_rate = round((exchange_dict["rates"][currency_to]), 2)
        bot.send_message (message.chat.id, exchange_rate * amount) #Returns currency exchanged, two decimals.
    except: 
        bot.send_message (message.chat.id, "Your input doesn't meet required parameters. Try again and right.")


@bot.message_handler(commands=["history"])
def history_command(message):
    history_data = bot.reply_to(message, "Type [base currency ABV], [comparing currency ABV]. Example: PLN, GBP")
    bot.register_next_step_handler(history_data, process_history)

def process_history(message): #Receiving user input
    try: #Catching exceptions
        history = message.text
        currency_from = history[0:3] #Extracting required arguments from user input
        exchange_currency = history[5:8]
    except:
        bot.send_message (message.chat.id, "Your input doesn't meet required parameters. Try again and right.")
    #Creating necessary datetime objects
    today_obj = date.today()
    week_ago_obj = today_obj - timedelta(days=8)

    #Converting objects to string with required mask
    today_str = today_obj.strftime("%Y-%m-%d")
    week_ago_str = week_ago_obj.strftime("%Y-%m-%d")

    #Creating an URL for request
    url = "https://api.exchangeratesapi.io/history?start_at="+week_ago_str+"&end_at="+today_str+"&base="+currency_from+"&symbols="+currency_to
    history_info = load_data(url) #Request
    history_days = history_info["rates"].keys() #Receiving days
    history_exchange = history_info["rates"].values() #Receiving exchange for days

    #Preparing data for matplotlib
    chart_days = []
    for day in history_days:
        chart_days.append(day) 

    chart_exchange = []
    for exchange in history_exchange:
        chart_exchange.append(exchange)
    chart_exchange_num = [num[exchange_currency] for num in chart_exchange]
    chart_exchange_num_round = []
    for num in chart_exchange_num:
        chart_exchange_num_round.append(round(num, 2))
    #Creating a graph
    try: #If data exists
        plt.plot(chart_days, chart_exchange_num_round)
        plt.xlabel("Exchange dates range")
        plt.ylabel("Exchange rates range")
        plt.title(currency_from + " to " + exchange_currency + " from " + week_ago_str + " to " + today_str)
        plt.savefig("graph.png")
        plt.clf()
        graph = open('graph.png', 'rb')
        bot.send_photo(message.chat.id, graph)
    except: #If no data provided
        bot.send_message (message.chat.id, "Requested data wasn't available.")

bot.polling(none_stop=True, interval=0)