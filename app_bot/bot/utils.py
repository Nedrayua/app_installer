
from aiogram import types
import json

import bot.constance as co
import datataker.datataker as dt


def inline_kb(callback: dict or list, text: str or list):
    """
    Generate inline keyboard from given data
    """
    if isinstance(callback, list):
        keyboard = types.InlineKeyboardMarkup()
        for i, j in enumerate(callback):
            json_data = json.dumps(j)
            button = types.InlineKeyboardButton(
                text=text[i],
                callback_data=json_data
            )
            keyboard.add(button)
    else:
        json_data = json.dumps(callback)
        button = types.InlineKeyboardButton(
            text=text,
            callback_data=json_data
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button)
    return keyboard

# --------------------------------------------------------------------

def return_content_args(name:str, value:str, message=None) -> str:
    """
    :name: Name for formating
    :value: value of name
    :message: if value is empty
    """
    if message:
        data = f'{name}:  {value}' if value else f'{name}:  {message}'
    else:
        data = f'{name}:  {value}' if value else ""
    return data


# --------------------------------------------------------------------

class GenMark:
    """
    class-creater for create unic tags in application
    """
    def gen_value():
        for num in range(10_000):
            yield num

    _value = gen_value()

    @classmethod
    def autoenum(cls):
        return str(next(cls._value))

# --------------------------------------------------------------------

def formated_currency_values(data:list, val:str) -> str:
    """
    Returned dict data of currency values in strin format
    """

    clean_data = [row for row in data if row[co.GET_PAIR].startswith(val + '_')]
    long_data = len(clean_data)
    sorted_data = sorted(clean_data, key=lambda row: row[co.GET_PAIR])

    message = [f'The value of the {co.CURRENCY_VALUES[val]} relative to the: \n']
    s = (len(message[0]) + 5) * '_'

    for row in sorted_data:
        relative = row[co.GET_PAIR].split('_')[1]
        part1 = f'{row.get(co.GET_BASE_CURRENCY):.8f} '.ljust(20, '>')
        part2 = f' {relative} for one {val}'.rjust(20, '>')
        message.append(s)
        message.append(part1 + part2)
    return '\n'.join(message) + f'\nTotal relative currency: {long_data}'

# -------------------------------------------------------------------

def formated_currency_value(cur_data:list, pair:str) -> str:

    clean_data = [row for row in cur_data if row.get(co.GET_PAIR) == pair].pop()
    relative, val = clean_data[co.GET_PAIR].split('_')
    part1 = f'{clean_data.get(co.GET_BASE_CURRENCY):.8f} '.ljust(20, '>')
    part2 = f' {val} for one {relative}'.rjust(20, '>')
    return part1 + part2 + '\n\n'
# --------------------------------------------------------------------

async def take_message(val:str, oto=False) -> str:
    """
    Create message for currency values
    """
    formated = formated_currency_value if oto else formated_currency_values
    cur_data = await dt.DataTaker.main_exchange_rate()
    status = cur_data.get(co.STATUS_ITEM)
    if status == co.STATUS_SUCCESS:
        print(cur_data)
        message_text = formated(cur_data.get(co.RATES_ITEM), val)
    elif status == co.STATUS_ERROR:
        message_text = co.MESSAGE_ERROR.format(cur_data[co.STATUS_ITEM], cur_data[co.ERROR_ITEM])
    else:
        message_text = co.MESSAGE_ERROR.format(co.STATUS_ERROR, co.MESSAGE_DATAIL_ERROR)

    return message_text

# --------------------------------------------------------------------


# --------------------------------------------------------------------

def generate_datas(data:dict, message_if_correct:str, tag:str, key:str) -> tuple([list, list, str]):
    """
    Generate datas, texts for buttons create and formed text_message
    """
    datas = []
    texts = []

    if data[co.STATUS_ITEM] == co.STATUS_SUCCESS:
        message_text = message_if_correct
        for currency in data.get(key):
            datas.append({'tag': tag, 'val': currency})
            texts.append(co.CURRENCY_VALUES[currency])
    elif data[co.STATUS_ITEM] == co.STATUS_ERROR:
        message_text = co.MESSAGE_ERROR.format(data[co.STATUS_ITEM], data[co.ERROR_ITEM])
    else:
        message_text = co.MESSAGE_ERROR.format(co.STATUS_ERROR, co.MESSAGE_DATAIL_ERROR)

    return datas, texts, message_text