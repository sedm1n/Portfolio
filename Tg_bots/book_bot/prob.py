# # text = 'Раз. Два. Три. Четыре. Пять. Прием!'


from pprint import pprint
from book_dict import book2

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


      
# # text = 'Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит, завтра!'
# # text = '— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, в чём вопрос.'

# # print(*_get_part_text(text, 1, 15), sep='\n')

# # text = 'Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит, завтра!'

# # print(*_get_part_text(text, 0, 54), sep='\n')

# # text = 'Раз. Два. Три. Четыре. Пять. Прием!'

# # print(*_get_part_text(text, 5, 9), sep='\n')


PAGE_SIZE = 1050
book = {}
            
      
      print(book==book2)

prepare_book('book/book.txt')
      