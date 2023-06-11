from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^(?!me)[\w.@+-]+\z'
    message = ('Введенное имя использовать запрещено. Выберите другое.')
    flags = 0
