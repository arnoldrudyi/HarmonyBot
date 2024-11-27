import datetime

from pytubefix import Search
from telebot import types


def generate_markup(videos, query, current_page, total_pages):
    markup = types.InlineKeyboardMarkup(row_width=3)
    for _ in range(len(videos)):
        markup.add(types.InlineKeyboardButton(f'{videos[_].title} - {videos[_].author} '
                                              f'[{datetime.timedelta(seconds=videos[_].length)}]',
                                              callback_data=videos[_].watch_url))
    if current_page+1 == 1:
        markup.add(types.InlineKeyboardButton("🔘", callback_data='unavailable'),
                   types.InlineKeyboardButton(f"{current_page+1}/{total_pages}", callback_data='unavailable'),
                   types.InlineKeyboardButton("▶️", callback_data=f'next_{query}_{current_page}'))
    elif len(videos) < 5:
        markup.add(types.InlineKeyboardButton("◀️", callback_data=f'previous_{query}_{current_page}'),
                   types.InlineKeyboardButton(f"{current_page+1}/{total_pages}", callback_data='unavailable'),
                   types.InlineKeyboardButton("🔘", callback_data='unavailable'))
    else:
        markup.add(types.InlineKeyboardButton("◀️", callback_data=f'previous_{query}_{current_page}'),
                   types.InlineKeyboardButton(f"{current_page+1}/{total_pages}", callback_data='unavailable'),
                   types.InlineKeyboardButton("▶️", callback_data=f'next_{query}_{current_page}'))
    return markup


def fetch_song_by_query(query):
    videos = Search(query).videos
    return generate_markup(videos[0:][:5], query, 0, int(round(len(videos)/5, 0)))


def next_page(query, current_page):
    videos = Search(query).videos
    return generate_markup(videos[(current_page+1)*5:][:5], query, current_page+1, int(round(len(videos)/5, 0)))


def previous_page(query, current_page):
    videos = Search(query).videos
    return generate_markup(videos[(current_page-1)*5:][:5], query, current_page-1, int(round(len(videos)/5, 0)))
