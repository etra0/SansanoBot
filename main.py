import re
import sys
import logging
from lib.constants import *
from lib.functions import *
from lib.telegram_api import *
from lib.logger import start_logging
from lib.secret_token import token
from lib.weather import Clima, interface
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
RegexHandler
from telegram import ParseMode

commands = [r"[/]?([mM]inuta)"
            + "(?: (?P<type_lunch>vegetariano|dieta|normal))?"
            + "(?: (?P<week>semana))?",
            r"[/](?P<command>start|help)",
            r"[/]?(clima)(?: (?P<today>hoy))?"
            ]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def enable_logging(func):
    def func_wrapper(bot, update, **arg):
        logging.info('%s: %s', update.message.chat.username,
                update.message.text)
        if 'groupdict' in arg:
            func(bot, update, arg['groupdict'])
        else:
            func(bot, update)
    return func_wrapper

@enable_logging
def minuta_wrapper(bot, update, groupdict):
    text = minuta(**groupdict)
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

@enable_logging
def clima_wrapper(bot, update, groupdict):
    text = get_weather(**groupdict)
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

@enable_logging
def help_wrapper(bot, update, groupdict):
    text = WELCOME_MESSAGE
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

@enable_logging
def no_command(bot, update):
    update.message.reply_text("No entiendo lo que quieres decir.")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(RegexHandler(commands[0], minuta_wrapper, pass_groupdict=True))
    dp.add_handler(RegexHandler(commands[1], help_wrapper, pass_groupdict=True))
    dp.add_handler(RegexHandler(commands[2], clima_wrapper, pass_groupdict=True))

    dp.add_handler(MessageHandler(Filters.text, no_command))

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

