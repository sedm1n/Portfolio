import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config

from handlers import other_handlers, user_handlers

from keyboards.set_menu import set_main_menu


# Инициализируем логгер
logger = logging.getLogger(__name__)



# Функция конфигурирования и запуска бота
async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')
  

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()
   
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tgbot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot=bot)
    
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    
    # Запускаем polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
