import telebot
from telebot import types 
from mod import get_class, mozg, bruho, addmin, TOKEN, channel

users = {}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Что умеет этот бот?\n \nЭтот бот создан для автоматизации приема снимков МРТ головного мозга и брюшной полости. Для корректной работы бота необходимо предоставить ему ваш номер телефона. \n \nНачать работу c ботом можно с помощью команды /start \n \nТакже вы можете перейти на канал нашей клиники по ссылке, которую бот пришлет вам после использования команды /channel \n \nЭту справку призывает команда /help")


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_num = types.KeyboardButton(text='Предоставить номер', request_contact=True)
    keyboard.add(button_num)
    bot.reply_to(message, "Здравствуйте! Чтобы нужный специалист мог с Вами связаться, пожалуйста, предоставьте свой номер телефона.\n \nСправка по боту - /help", reply_markup = keyboard)



@bot.message_handler(content_types=['contact']) 
def num(message):
    if message.contact is not None:
        userdata = str(message.contact)
        users[str(message.chat.id)]=userdata
        bot.send_message(message.chat.id, "Спасибо за доверие! Теперь нужный специалист сможет связаться с вами. Пожалуйста, отправьте фотографию МРТ мозга или брюшной полости. \n \nВнимание! Бот может принимать ТОЛЬКО ПО ОДНОЙ фотографии. Если фотографий больше, пожалуйста, присылайте их по очереди.")
    

@bot.message_handler(commands=['channel']) 
def send_channel(message): 
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Наш канал', url = channel)
    markup.add(btn)
    bot.reply_to(message, 'Рады, что вы заинтересовались нашим каналом! Перейти можно по ссылке:', reply_markup = markup)
    

@bot.message_handler(content_types=['photo'])
def ifimag(message):
    check_data = users.get[str(message.chat.id)]
    if not check_data == None:

        user_contact = users[str(message.chat.id)]

        file_info = bot.get_file(message.photo[-1].file_id)
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'images/{file_name}', 'wb') as new_file: 
            new_file.write(downloaded_file)
        
        file_path = f'images/{file_name}'
        file_class = get_class(file_path)

        if file_class == 'notsure':
            photo = open(file_path, 'rb')
            bot.reply_to(message, 'Хм! Интересный снимок. Для его обработки потребуется больше времени, чем обычно. Специалист свяжется с вами, когда все будет готово. Извините за предоставленные неудобства.')
            msg = bot.send_message(addmin, photo)
            bot.reply_to(msg, user_contact)

        elif file_class=='мозг':
            photo = open(file_path, 'rb')
            bot.reply_to(message, 'На фотографии мозг. Специалист свяжется с вами в телеграм.')
            msg = bot.send_message(mozg, photo)
            bot.reply_to(msg, user_contact)

        else:
            photo = open(file_path, 'rb')
            bot.reply_to(message, 'На фотографии брюшная полость. Специалист свяжется с вами в телеграм.')
            bot.send_photo(bruho, photo)
            bot.reply_to(msg, user_contact)
    
    else:
        bot.send_message(message.chat.id, 'Прежде чем отправлять снимки, пожалуйста, поделитесь своим номером телефона, чтобы специалист мог связаться с вами. Чтобы сделать это, активируйте команду /start')
        
bot.polling()
