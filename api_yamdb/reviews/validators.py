from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import USERNAME_SYMBOLS

SYMBOLS_ERROR = 'Недопустимые символы: {value}'
ERROR_NAME = 'Недопустимое имя пользователя {value}!'


class UserValidator:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(ERROR_NAME.format(value=ERROR_NAME))
        if not USERNAME_SYMBOLS.match(value):
            raise ValidationError(
                SYMBOLS_ERROR.format(
                    value=''.join(
                        symbol for symbol in value
                        if not USERNAME_SYMBOLS.match(symbol)
                    )
                )
            )
        return value


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'{value} год еще не наступил!',
        )
