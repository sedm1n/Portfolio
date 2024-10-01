from cgitb import text
from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON
from services.file_handling import book


def create_bookmarks_keyboard(*args:int)-> InlineKeyboardMarkup:
      kb_builder= InlineKeyboardBuilder()

      for button in sorted(args):
            kb_builder.row(InlineKeyboardButton(
                  text=f'{button} - {book[button][:100]}',
                  callback_data=str(button)
            ))

      # Добавляем в клавиатру две кнопи редактировать и отменить
      kb_builder.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'],
                                           callback_data='edit_bookmarks'),
                  InlineKeyboardButton(text=LEXICON['cancel'],callback_data='cancel'),
                     
                   width=2  )

      return kb_builder.as_markup()

def create_edit_keyboard(*args:int)-> InlineKeyboardMarkup:
      kb_builder = InlineKeyboardBuilder()

      for button in sorted(args):
            kb_builder.row(
                  InlineKeyboardButton(text=f'{LEXICON['del']} {button} - {book[button][:100]}',
                  callback_data=f'{button}del')

            )
      # Добавляем конец кнопку отменить
      kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
      return kb_builder.as_markup()
      