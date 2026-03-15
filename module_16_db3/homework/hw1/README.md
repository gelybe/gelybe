## Задача 1. Создание схемы
### Что нужно сделать
Реализуйте следующие таблицы:
  
![](../img/cinema_schema_diagram.png)

SQL-запросы для создания схемы оформите в SQL-файле или в Python-скрипте. 

Подумайте, как должны вести себя ссылки при удалении родительских записей.

В отдельном файле напишите классификацию всех типов связей между таблицами в схеме.

### Рекомендации
* [Ограничение целостности внешнего ключа](https://www.sqlitetutorial.net/sqlite-foreign-key/)
* Выполнить SQL-скрипт из файла можно так:

   ```python
   import sqlite3
   
   with open('create_schema.sql', 'r') as sql_file:
      sql_script: str = sql_file.read()
   
   with sqlite3.connect('database.db') as conn:
      cursor: sqlite3.Cursor = conn.cursor()
      cursor.executescript(sql_script)
      conn.commit()
  ```
### Что оценивается
* Диаграмма созданной схемы соответствует диаграмме из условия.
* Соблюдены ограничения целостности внешнего ключа.
* Приведена классификация всех пяти видов связей между таблицами.
