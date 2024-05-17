import telebot
from telebot import *
from prozhito_def_files import plot_all_graphs
import io
import matplotlib.pyplot as plt

TOKEN='6742100930:AAFWmK2R_8StqyA3QmHZpsQFwG4kwbwDam8'
bot = telebot.TeleBot(TOKEN)

instruction_file=open('source/instruction.pdf', 'rb')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    change_mode(message)
   

def change_mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔍 Найти")
    btn2 = types.KeyboardButton("🛈 Инструкция")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, f'Чем могу помочь?', reply_markup=markup)
    bot.register_next_step_handler(message, mode_router)
    
    
def mode_router(message):
    if message.text == '🔍 Найти':
        search(message)
        
    elif message.text == '🛈 Инструкция':
        bot.send_document(message.chat.id, instruction_file)    
        change_mode(message)
        
    else:
        bot.send_message(message.chat.id, 'Неверный ввод. Выберите один из вариантов(кнопок).')
        change_mode(message)


def search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, 'Отправьте мне id автора', reply_markup=markup)
    bot.register_next_step_handler(message, step_1)
    
def step_1(message):
    if message.text == '🔙 Назад':
        change_mode(message)
            
    else:
        if message.text.isdigit():
            try:
                bot.send_message(message.chat.id, 'Ищу')
                
                fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 14))
                
                fig, messages = plot_all_graphs(fig , axs, message.text)
                
                if fig == None and messages ==None:
                    bot.send_message(message.chat.id, 'Нет такого id')
                    search(message)
                    return None
                    
                # Сохранение изображения в поток байтов
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)

                for text in messages:
                    bot.send_message(message.chat.id, text)
                    
                # Отправка изображения
                bot.send_photo(message.chat.id, buf)

                # Закрытие изображения
                plt.clf()
                plt.close('all')
                
            except Exception as e:
                    print(e)
                    bot.send_message(message.chat.id, 'Непредвиденная ошибка')
                    search(message)
        
        else:
            bot.send_message(message.chat.id, 'Нужно ввести число')
            bot.register_next_step_handler(message, step_1)
        
bot.infinity_polling()
