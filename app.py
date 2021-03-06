import logging
import API_KEYS

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from alpha_vantage.cryptocurrencies import CryptoCurrencies 
from alpha_vantage.foreignexchange import ForeignExchange


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#print(logger)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('/start : Greeting message\n /price : to get latest price of crypto\n /help : get all working comands of geekfluxcrypto bot\n /news : Coming soon')

def news(update, context):
    """Send a message when the command /news is issued."""
    update.message.reply_text('COMING SOON hehe ')


def price(update, context):
    """Send a message when the command /PRICE is issued."""
    CUR_NAME = update.message.text
    CUR_NAME = CUR_NAME.replace(" " , "")
    CUR_NAME = CUR_NAME.split("/price")[1]
    print(CUR_NAME)
    if(len(CUR_NAME) > 5 ):
        update.message.reply_text("are you fucking kiding me ?")
    else:
        cc = ForeignExchange(key=API_KEYS.URL_API_KEY , output_format="json")
        Currency , _ = cc.get_currency_exchange_rate(from_currency=CUR_NAME,to_currency='INR')
        Data = str( 
        str(Currency["1. From_Currency Code"]) + " INR : " + str( Currency["5. Exchange Rate"]))
        update.message.reply_text(Data)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/start : Greeting message\n /price : to get latest price of crypto\n /help : get all working comands of geekfluxcrypto bot\n /news : commign soon')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text + " kya bsdk?")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_KEYS.API_KEY , use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("news", news))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()