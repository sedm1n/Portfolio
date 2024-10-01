from typing import Any
from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter

class IsDigitCalbackData(BaseFilter):
      async def __call__(self, calback:CallbackQuery) -> Any:
            return calback.data.isdigit()
      
class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()