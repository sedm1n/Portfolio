import logging

from copy import deepcopy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, reply_keyboard_markup
from aiogram.filters import Command, CommandStart

from filters.filters import IsDelBookmarkCallbackData, IsDigitCalbackData
from database.database import user_db, user_dict_template

from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_ru import LEXICON
from services.file_handling import book




logger = logging.getLogger(__name__)

router = Router()

# Этот хендлер обрабатывает starт, добавляет 
# пользователя в базу если его там нет
@router.message(CommandStart())
async def process_start_command(message:Message):
      await message.answer(LEXICON[message.text])
      if message.from_user.id not in user_db:
            user_db[message.from_user.id]=deepcopy(user_dict_template)


# Этот хендлер срабатывает на комманду /help
@router.message(Command('help'))
async def process_help_command(message:Message):
      await message.answer(LEXICON[message.text])

# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command('beginning'))
async def process_beginning_command(message:Message):
      user_db[message.from_user.id]['page']=1
      text=book[ user_db[message.from_user.id]['page']]
      await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                  'backward', f"{user_db[message.from_user.id]['page']}/{len(book)}",
                  'forward'
            )
      )

# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message:Message):
      text = book[user_db[message.from_user.id]['page']]
      await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
            'backward',
            f'{user_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
      )

# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message:Message):
      if user_db[message.from_user.id]['bookmarks']:
            await message.answer(
                  text=LEXICON[message.text],
                  reply_markup=create_bookmarks_keyboard(
                        *user_db[message.from_user.id]['bookmarks']))
      else:
            await message.answer(LEXICON['no_bookmarks'])
            
                  
            

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data=='forward')
async def process_forward_press(callback:CallbackQuery):
      if user_db[callback.from_user.id]['page'] < len(book):
            user_db[callback.from_user.id]['page']+=1
            text = book[user_db[callback.from_user.id]['page']]
            await callback.message.edit_text(text=text,
                  reply_markup=create_pagination_keyboard(
                  'backward',
                  f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                  'forward'
            )
        )
      await callback.answer()



@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/','').isdigit())
async def process_page_press(callback:CallbackQuery):
      user_db[callback.from_user.id]['bookmarks'].add(
            user_db[callback.from_user.id]['page']
      )
      await callback.answer('Страница добавленв в закладку')

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCalbackData())
async def process_bookmark_press(callback:CallbackQuery):
      text = book[int(callback.data)]
      user_db[callback.from_user.id]['page']=int(callback.data)
      await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                  'backward',
                  f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                  'forward'
            )
      )

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data=='edit_bookmarks')
async def process_edit_bookmarks_press(callback:CallbackQuery):
      await callback.message.edit_text(
            text=LEXICON[callback.data],
            reply_markup=create_edit_keyboard(
                  *user_db[callback.from_user.id]['bookmarks']
            )
      )

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(F.data=='cancel')
async def process_cancel_press(callback:CallbackQuery):
            await callback.message.edit_text(text=LEXICON['cancel_text'])

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
      
    user_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *user_db[callback.from_user.id]["bookmarks"]
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])

