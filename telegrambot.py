import logging
import os
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext,  CallbackQueryHandler, Filters , MessageHandler
from deep_translator import GoogleTranslator

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

mydict = {}
id = ''

def start(update: Update, callback: CallbackContext):
    global mydict, id
    update.message.reply_text('welcom to translation bot')
    my_id = update.message.from_user.id
    print(str(my_id))
    mydict[str(my_id)] = []
    id = str(my_id)
    print(mydict)
    
    keyboard = [[
            InlineKeyboardButton("english", callback_data='en'),
            InlineKeyboardButton("french", callback_data='fr'),
            ],
            [InlineKeyboardButton("chinese", callback_data='zh'),
            InlineKeyboardButton("arabic", callback_data='ar'),
            ],
            [InlineKeyboardButton("russian", callback_data='ru'),
            InlineKeyboardButton("espanish", callback_data='es'),
            ],
            [InlineKeyboardButton("portuguese", callback_data='pt'),
            InlineKeyboardButton("italian", callback_data='it'),
            ],
            [InlineKeyboardButton("japanese", callback_data='ja'),
            InlineKeyboardButton("hindi", callback_data='hi'),
            ],
            [InlineKeyboardButton("persian", callback_data='fa'),]
    ]

    reply_markup =  InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose your imported language', reply_markup=reply_markup)


def target(update: Update, callback: CallbackContext):
  keyboard = [[
            InlineKeyboardButton("english", callback_data='@en'),
            InlineKeyboardButton("french", callback_data='@fr'),
            ],
            [InlineKeyboardButton("chinese", callback_data='@zh'),
            InlineKeyboardButton("arabic", callback_data='@ar'),
            ],
            [InlineKeyboardButton("russian", callback_data='@ru'),
            InlineKeyboardButton("espanish", callback_data='@es'),
            ],
            [InlineKeyboardButton("portuguese", callback_data='@pt'),
            InlineKeyboardButton("italian", callback_data='@it'),
            ],
            [InlineKeyboardButton("japanese", callback_data='@ja'),
            InlineKeyboardButton("hindi", callback_data='@hi'),
            ],
            [InlineKeyboardButton("persian", callback_data='@fa'),]
    ]

  reply_markup =  InlineKeyboardMarkup(keyboard)
  update.message.reply_text('Please choose your choosen language', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext):
    global mydict , id

    query = update.callback_query
    query.answer()

    if str(query.data).isalpha() == True:
      query.edit_message_text("Your input language selected successfully")
      update.effective_chat.send_message('enter /target to choose your target language')
      mydict[id].append(str(query.data))
      print(mydict)

    elif str(query.data)[0] == '@':
      query.edit_message_text(text=f"Your target language selected successfully")
      update.effective_chat.send_message('enter your sentence')
      mydict[id].append(str(query.data)[1:])
      print(mydict)


def translate(update:Update , callback:CallbackContext):
  global mydict, id
  print(mydict)
  text = str(update.message.text)
  to_translate = text
  translated = GoogleTranslator(source='auto', target = mydict[id][1]).translate(to_translate)
  print(translate)
  # tr = translators.google(text , from_language=mydict[id][0] , to_language= mydict[id][1])
  update.effective_chat.send_message(translated)


def main() :
    TOKEN = "1886012278:AAGnOW0j8LQ1cYck98ul2MjZQGawGuTG75g"
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    PORT = int(os.environ.get('PORT', '8443'))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("target", target))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command , translate))

    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url = 'https://translationproje.herokuapp.com/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()