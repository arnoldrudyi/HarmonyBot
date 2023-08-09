import os
from json import load
import re

import telebot

from downloader.utils.logger_cogs import logger
from downloader.database.connect import SessionLocal
from downloader.models.account import Account
from downloader.models.audio import Audio
from downloader.core.youtube_downloader import fetch_audio_info
from downloader.core.soundcloud_downloader import fetch_soundcloud_audio
from downloader.core.services_downloader import fetch_youtube_link
from downloader.core.search_engine import fetch_song_by_query, next_page, previous_page


session = SessionLocal()
bot = telebot.TeleBot(os.getenv('TOKEN'))

with open('messages.json', 'r', encoding='utf-8-sig') as file:
    messages_dict: list = load(file)


def send_audio(audio_dict, origin_message, loading_message):
    bot.send_chat_action(origin_message.chat.id, 'upload_document')
    if audio_dict is not None:
        if 'title' in audio_dict:
            try:
                bot.delete_message(origin_message.chat.id, loading_message.id)
                audio_message = bot.send_audio(origin_message.chat.id, title=audio_dict['title'], performer=audio_dict['author'],
                                               duration=audio_dict['length'], thumbnail=audio_dict['thumbnail'],
                                               audio=audio_dict['audio'], reply_to_message_id=origin_message.id,
                                               parse_mode='html')
                session.add(Audio(url=audio_dict['video_id'], unique_id=audio_message.json['audio']['file_id']))
                session.commit()
            except telebot.apihelper.ApiTelegramException:
                account = session.query(Account).filter(Account.chatid == origin_message.chat.id).first()
                bot.send_message(origin_message.chat.id, messages_dict[0][f'tooBig_{account.language}'],
                                 parse_mode='html',
                                 reply_to_message_id=origin_message.id)
        else:
            try:
                bot.delete_message(origin_message.chat.id, loading_message.id)
                bot.send_audio(origin_message.chat.id, audio=audio_dict['unique_id'], reply_to_message_id=origin_message.id,
                               parse_mode='html')
            except telebot.apihelper.ApiTelegramException:
                account = session.query(Account).filter(Account.chatid == origin_message.chat.id).first()
                bot.send_message(origin_message.chat.id, messages_dict[0][f'tooBig_{account.language}'],
                                 parse_mode='html',
                                 reply_to_message_id=origin_message.id)
    else:
        account = session.query(Account).filter(Account.chatid == origin_message.chat.id).first()
        bot.delete_message(origin_message.chat.id, loading_message.id)
        bot.send_message(origin_message.chat.id, messages_dict[0][f'error_{account.language}'], parse_mode='html',
                         reply_to_message_id=origin_message.id)


@bot.message_handler(commands=['start'])
def start(message):
    if session.query(Account).filter(Account.chatid == message.chat.id).first() is None:
        languages = telebot.types.InlineKeyboardMarkup(row_width=2)
        english = telebot.types.InlineKeyboardButton(text='English 🇬🇧', callback_data='set_english')
        ukrainian = telebot.types.InlineKeyboardButton(text='Українська 🇺🇦', callback_data='set_ukrainian')
        languages.add(english, ukrainian)
        bot.send_message(message.chat.id, f'Hello, <b>{message.from_user.first_name}</b>!\n\n'
                                          f'Please, choose your preferred language from the list below:',
                         parse_mode='html', reply_markup=languages)
    else:
        account = session.query(Account).filter(Account.chatid == message.chat.id).first()
        bot.send_message(message.chat.id, messages_dict[0][f'start_{account.language}'], parse_mode='html')


@bot.message_handler(content_types=['text'])
def handle_url(message):
    youtube_pattern = re.search('youtube.com', message.text)
    youtube_mobile_pattern = re.search('youtu.be', message.text)
    soundcloud_pattern = re.search('soundcloud.com', message.text)
    spotify_pattern = re.search('open.spotify.com', message.text)
    youtube_music_pattern = re.search('music.youtube.com', message.text)

    if (youtube_pattern or youtube_mobile_pattern) and youtube_music_pattern is None:
        loading_message = bot.send_message(message.chat.id, '⏳', reply_to_message_id=message.id)
        audio_dict = fetch_audio_info(message.text)
        send_audio(audio_dict, message, loading_message)

    elif soundcloud_pattern:
        loading_message = bot.send_message(message.chat.id, '⏳', reply_to_message_id=message.id)
        link = fetch_youtube_link(message.text)
        if link is not None:
            audio_dict = fetch_audio_info(link)
            send_audio(audio_dict, message, loading_message)
        else:
            account = session.query(Account).filter(Account.chatid == message.chat.id).first()
            video_id = fetch_soundcloud_audio(message.text)
            bot.send_message(message.chat.id, messages_dict[0][f'another_song_{account.language}'], parse_mode='html', reply_to_message_id=message.id)
            audio_dict = fetch_audio_info(f'https://www.youtube.com/watch?v={video_id}')
            send_audio(audio_dict, message, loading_message)

    elif youtube_music_pattern or spotify_pattern:
        loading_message = bot.send_message(message.chat.id, '⏳', reply_to_message_id=message.id)
        link = fetch_youtube_link(message.text)
        if link is not None:
            audio_dict = fetch_audio_info(link)
            send_audio(audio_dict, message, loading_message)
        else:
            account = session.query(Account).filter(Account.chatid == message.chat.id).first()
            bot.delete_message(message.chat.id, loading_message.id)
            bot.send_message(message.chat.id, messages_dict[0][f'unsupported_{account.language}'], parse_mode='html',
                             reply_to_message_id=message.id)

    else:
        markup = fetch_song_by_query(message.text)
        account = session.query(Account).filter(Account.chatid == message.chat.id).first()
        bot.send_message(message.chat.id,
                         f"{messages_dict[0][f'found_{account.language}']} <code>{message.text}</code>:",
                         reply_markup=markup, reply_to_message_id=message.id, parse_mode='html')

@bot.callback_query_handler(lambda call: True)
def handle(call):
    if call.data == 'set_english':
        if session.query(Account).filter(Account.chatid == call.message.chat.id).first():
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, '❌ This account is <b>already registered</b>.', parse_mode='html')
        else:
            session.add(Account(chatid=call.message.chat.id, username=call.json['from']['username'],
                                is_admin=False, language='us'))
            session.commit()
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, messages_dict[0][f'start_us'], parse_mode='html')

    if call.data == 'set_ukrainian':
        if session.query(Account).filter(Account.chatid == call.message.chat.id).first():
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, '❌ Цей акаунт <b>вже зареєстровано</b>.', parse_mode='html')
        else:
            session.add(Account(chatid=call.message.chat.id, username=call.json['from']['username'],
                                is_admin=False, language='ua'))
            session.commit()
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, messages_dict[0][f'start_ua'], parse_mode='html')

    if call.data.startswith('next'):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⏳',
                              reply_markup=None)
        query, page = call.data.split('_')[1], call.data.split('_')[2]
        markup = next_page(query, int(page))
        account = session.query(Account).filter(Account.chatid == call.message.chat.id).first()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"{messages_dict[0][f'found_{account.language}']} <code>{query}</code>:",
                              reply_markup=markup, parse_mode='html')

    if call.data.startswith('previous'):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⏳',
                              reply_markup=None)
        query, page = call.data.split('_')[1], call.data.split('_')[2]
        markup = previous_page(query, int(page))
        account = session.query(Account).filter(Account.chatid == call.message.chat.id).first()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"{messages_dict[0][f'found_{account.language}']} <code>{query}</code>:",
                              reply_markup=markup, parse_mode='html')

    if call.data.startswith('https://youtube.com'):
        loading_message = bot.send_message(call.message.chat.id, '⏳')
        audio_dict = fetch_audio_info(call.data)
        send_audio(audio_dict, call.message, loading_message)


if __name__ == '__main__':
    logger.success(f'Bot @{bot.get_me().username} started!')
    bot.polling(none_stop=True)
