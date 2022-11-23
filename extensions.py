import requests
import json
from config import *

class ConversionException(Exception):
    pass

class ExchangeMaker:
    @staticmethod
    def get_price(target: str, base: str, amount: str):
        if target == base:
            raise ConversionException(f'Невозможно перевести, так как введены одинаковые названия валют {base}.')

        try:
            target_ticker = keys[target]
        except KeyError:
            raise ConversionException(f'Не удалось обработать введенную валюту {target}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать введенную валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать введенное количество {amount}')

        request = requests.get(f'https://v6.exchangerate-api.com/v6/bc707e8c44ea94453d11304a/pair/{target_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(request.content)['conversion_result']

        return total_base