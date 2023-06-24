from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    """Валидация запрещающая выбрать имя пользователя 'me'."""

    regex = r'^(?!me)[\w.@+-]'
    message = ('Введенное имя использовать запрещено. Выберите другое.')
    flags = 0
