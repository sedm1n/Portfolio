import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE=1050

book: dict[int, str] = {}

## Функция, возвращающая строку с текстом страницы и ее размер 
def _get_part_text(text:str, start:int, size:int)-> tuple[str, int]:
      END_ALPHA='.,!?:;'
      index_end=size
      new_str = text[start:size+start]
      if new_str[-1] in END_ALPHA and new_str[-2] in END_ALPHA:
            new_str = new_str[:-2]

      for i in range(len(new_str)-1, -1,-1):
            if new_str[i] in END_ALPHA:
                  index_end= i+1
                  break

      
      return (new_str[:index_end], index_end)


# функция формирующаяя словарь книги
def prepare_book(path:str)->None:
      with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
      start=0
      page_number = 1
      end_text = len(text)
      while start < end_text:
            line, length= _get_part_text(text, start, PAGE_SIZE)          
            book[page_number]= line.lstrip()
            start += length
            page_number+=1
      

# вызов фнукции 
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))

