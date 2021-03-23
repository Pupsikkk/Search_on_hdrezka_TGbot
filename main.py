from bs4 import BeautifulSoup
import requests
import telebot

TOKEN = '1790960120:AAHIHyMbVqOuIvu36Pm4VDTKGPXfdOR32W8'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, '     Просто введите название фильма/сериала который ищете\n'
                                      '     По ссылках(названиях) можете перейти прямо на сайт')

@bot.message_handler(content_types=['text'])
def search(message):
    base = 'https://rezka.ag/search/?do=search&subaction=search&q='
    req = message.text
    html = requests.get(base + req).content
    soup = BeautifulSoup(html, 'lxml')
    final_res = []
    for index, note in enumerate(soup.find_all('div', class_='b-content__inline_item')):
        if index == 3:
            break
        else:
            final_res.append({'name': soup.find_all('div', class_='b-content__inline_item')[index]
                             .find('div', class_='b-content__inline_item-link').find('a').text,
                              'some_inf': soup.find_all('div', class_='b-content__inline_item')[index]
                             .find('div', class_='b-content__inline_item-link')
                             .find('div').text,
                              'img_link': soup.find_all('div', class_='b-content__inline_item')[index]
                             .find('div', class_='b-content__inline_item-cover')
                             .find('img').get('src'),
                              'link': soup.find_all('div', class_='b-content__inline_item')[index]
                             .find('div', class_='b-content__inline_item-cover')
                             .find('a').get('href')})
    if final_res:
        for note in final_res:
            inf = list(note.values())
            bot.send_photo(message.chat.id, inf[2], f'<b><a href="{inf[3]}">{inf[0]}</a></b>\n{inf[1]}'.format(message.from_user, bot.get_me()),
                           parse_mode='html')
        if len(soup.find_all('div', class_='b-content__inline_item')) > 3:
            bot.send_message(message.chat.id, f'<b><a href="{base+req}">БОЛЬШЕ РЕЗУЛЬТАТОВ ЗДЕСЬ</a></b>'.format(message.from_user, bot.get_me()),
                            parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Ничего не найдено')

bot.polling(none_stop=True)
