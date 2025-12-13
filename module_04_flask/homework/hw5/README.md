## Задача 5. Текущие процессы
### Что нужно сделать
Напишите GET-endpoint `/ps`, который принимает на вход аргументы командной строки, а возвращает результат работы команды `ps` с этими аргументами. 
Входные значения endpoint должен принимать в виде списка через аргумент `arg`.

Например, для исполнения команды `ps aux` запрос будет следующим:

`/ps?arg=a&arg=u&arg=x`
### Советы и рекомендации
- Получить аргументы списком можно следующим образом:

`args: List[str] = request.args.getlist('arg')`
- Хорошая практика — заключение потенциально небезопасного пользовательского ввода в кавычки с помощью `shlex.quote`:

```jupyterpython
>>> user_cmd = '; ./kill_the_system.sh'
>>> f"ps {user_cmd}"
ps ; ./kill_the_system.sh

>>> clean_user_cmd = shlex.quote(user_cmd)
>>> f"ps {clean_user_cmd}"
ps '; ./kill_the_system.sh'
```

В первом случае выполнится команда `ps`, а затем зловещий скрипт.<br>
Во втором же случае ничего страшного не произойдёт.
- Чтобы красиво отформатировать результат, заключите его в тег `<pre>Your result</pre>`.
### Что оценивается
- Аргументы передаются списком, а не строкой.
- Общие советы и рекомендации
- [Документация WTForms](https://wtforms.readthedocs.io/en/3.0.x/).
- Вызвать программу из Python можно с помощью модуля `subprocess` ([документация на английском языке](https://docs.python.org/3/library/subprocess.html), [документация на русском языке](https://docs-python.ru/standart-library/modul-subprocess-python/)):

```jupyterpython
>>> import shlex, subprocess
>>> command_str = f"uptime"
>>> command = shlex.split(command_str)
>>> result = subprocess.run(command, capture_output=True)
```
