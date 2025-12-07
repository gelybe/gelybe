## Задача 4. Доверяй, но проверяй
### Что нужно сделать
Каждый разработчик ещё и тестировщик: он должен уметь покрыть тестами свой код. Но бывают ситуации, когда он не успевает и просит помочь в этом деле своего товарища тестировщика. Вот и сейчас так получилось: код есть, но тестами он не покрыт. Да и, кажется, писался он впопыхах пальцем левой ноги, надо бы его проверить.

1. Покройте данный класс юнит-тестами: все методы должны быть проверены.
2. Используя написанные тесты, найдите ошибки и исправьте их.
3. Найденные ошибки и их исправления оформите в виде Markdown-файла _ERRORS.MD_.

```python

class Person:
    def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
        self.name: str = name
        self.yob: int = year_of_birth
        self.address: str = address

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return self.yob - now.year

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = self.name

    def set_address(self, address: str) -> None:
        self.address == address

    def get_address(self) -> str:
        return self.address

    def is_homeless(self) -> bool:
        '''
        returns True if address is not set, false in other case
        '''
        return address is None

```
### Советы и рекомендации
[Подсказка по Markdown-синтаксису](https://github.com/OlgaVlasova/markdown-doc/blob/master/README.md)
### Что оценивается
- Написан тест для каждого метода.
- Найдены и исправлены все ошибки.
- Ответ оформлен в виде Markdown-файла.
