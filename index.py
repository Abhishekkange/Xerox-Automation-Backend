from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API = ""
webLink = "https://celebrated-torte-184681.netlify.app/"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please upload a file using /upload.')

def upload(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    update.message.reply_text(f'Please upload a file  your PIN is {chat_id}')

def handle_document(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    document = update.message.document

    file = context.bot.get_file(document.file_id)
    file.download(f'./{chat_id}+{document.file_name}')

    context.bot.send_message(chat_id, 'File downloaded successfully.')

def handle_photo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    photo = update.message.photo[-1]

    file = context.bot.get_file(photo.file_id)
    file.download(f'./{chat_id}+{photo.file_id}.jpg')

    context.bot.send_message(chat_id, 'Image downloaded successfully.')

# Python Function to print file
import subprocess
import os
import sys
import time
import tempfile
import win32api
import win32print
    
def print_file(file_name):


    if sys.platform == 'win32':
        win32api.ShellExecute(
            0,
            "print",
            file_name,
            #
            # If this is None, the default printer will
            # be used anyway.
            #
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )
    else:
        lpr = subprocess.Popen(
            ["/usr/bin/lpr", file_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        lprout, lprerr = lpr.communicate()
        if lpr.returncode:
            sys.stdout.write(lprout)
            sys.stderr.write(lprerr)
            sys.exit(lpr.returncode)



def main() -> None:
    updater = Updater(API, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("upload", upload))
    dp.add_handler(MessageHandler(Filters.document, handle_document))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()