"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


# Функциональный валидатор
def number_length(min_num: int, max_num: int):
    def _number_length(form: FlaskForm, field: Field):
        _phone: int = field.data
        if _phone < min_num or _phone > max_num:
            message = f'Phone must be between {min_num} and {max_num}'
            raise ValidationError(message)
    return _number_length


# Класс-валидатор
class NumberLength:
    def __init__(self, min_num=-1, max_num=-1, message: Optional[str] = None):
        self.min_num = min_num
        self.max_num = max_num
        self.message = message

    def __call__(self, form, field):
        data = str(field.data)
        if data.isdigit():
            if self.min != -1 and len(data) < self.min:
                raise ValidationError(f'Number must be at least {self.min} digits long.')
            if self.max != -1 and len(data) > self.max:
                raise ValidationError(f'Number must be at most {self.max} digits long.')
        else:
            raise ValidationError('Number must contain only digits.')