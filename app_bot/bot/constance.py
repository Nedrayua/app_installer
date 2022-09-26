
from bot.utils import GenMark

#Greetings
GREETINGS_FIRST = 'Hello{}! Wellcome to currency bot!'
GREETINGS_AGAIN = 'Hello{}! We glad to see you again!'

# Messages

MESSAGE_ALL_RATES = 'To get all currencies relative, choice one of:'
MESSAGE_SPEND_CURRENCY = 'Choice currency to spend:'
MESSAGE_CHOICE_PAIR = 'Choice pair for traking:'
MESSAGE_ERROR = 'Status: {}. Detail: {}!'
MESSAGE_DATAIL_ERROR = 'the resource is temporarily unavailable'
MESSAGE_CHOICE_CURRENCY_OPTION = 'Choice format getting currency values.'
MESSAGE_CHANGE_OWN_INFO = 'Change your personl information.'
MESSAGE_CHOISE_SPECIFIC_CATEGORY = 'Choise category to change'
FORMATED_MESSAGE_CURRENCY = 'The value of the {} relative to the: \n'

# Tags

currency_one_to_many_tag = GenMark.autoenum()
currency_one_to_one_tag = GenMark.autoenum()
currency_list_pairs_tag = GenMark.autoenum()
currency_tag = GenMark.autoenum()
currency_list_tag = GenMark.autoenum()
action_oto_tag = GenMark.autoenum()
action_otm_tag = GenMark.autoenum()
tracking_tag = GenMark.autoenum()
settings_tag = GenMark.autoenum()
currency_detail_oto_tag = GenMark.autoenum()
currency_detail_otm_tag = GenMark.autoenum()
change_settings_tag = GenMark.autoenum()   
change_specific_settings_tag = GenMark.autoenum()

# Settings commands

change_name = GenMark.autoenum()
change_phone = GenMark.autoenum()
change_email = GenMark.autoenum()
change_city = GenMark.autoenum()
wrong_change = GenMark.autoenum()
complete_change = GenMark.autoenum()
back_to_settings = GenMark.autoenum()

SETTINGS_BUTTONS = {
    change_name: 'Change name',
    change_phone: 'Chan phone',
    change_email: 'Change email',
    change_city: 'Change city',
    back_to_settings: "Go back to change"
}

CHANGE_SETTINGS_MESSAGES = {
    change_name: "Enter Your name:",
    change_phone: 'Enter Your phone number, but no more then 13 characters:',
    change_email: 'Enter Your email',
    change_city: 'Enter the name of Your city',
    wrong_change: 'Wrong data. Try again.',
    complete_change: 'Changes is saving.'
}


MENU_LIST = [currency_tag, settings_tag]

MAIN_MENU = {
    currency_tag: 'Currency',
    settings_tag: 'Settings'
}
# Names buttons

START_TRACKING_BUTTON = 'Start tracking'
STOP_TRACKING_BUTTON = 'Stop tracking'
CURRENCY_LIST_BUTTON = 'Get currency list'
BASE_CURRENCY_LIST_BUTTON = 'Get base currency list'
SETTINGS_BUTTON = 'Settings'
ONE_TO_MANY_BUTTON = 'One currency rate to many'
ONE_TO_ONE_BUTTON = 'One to one currency rate'

# Currency

CURRENCY_VALUES = {
    'BTC': 'Bitcoin', 
    'EUR': 'Euro',
    'UAH': 'Grivna',
    'USD': 'US Dolar',
    'ETH': 'Ethereum',
    'USDT': 'Tether',
    'LTC': 'Litecoin',
    'BNB': 'Binance Coin',
    'DOGE': 'Dogecoin',
    'UACB-NOV22': 'Ukranian cryptobond',
    'USDC': 'USD Coin'
}

# commands

stop_tracking_tag = GenMark.autoenum()
start_tracking_tag = GenMark.autoenum()

# currency resource

URL = 'https://coinpay.org.ua/'

CURRENCY_LIST = "api/v1/currency"
ACTIVE_PAIR = "api/v1/pair"
EXCHANGE_RATE = "api/v1/exchange_rate"

STATUS_SUCCESS = 'success'
STATUS_ERROR = 'error'

STATUS_ITEM = 'status'
ERROR_ITEM = 'detail'
CURRENCY_ITEM = 'currencies'
PAIRS_ITEM = 'pairs'
RATES_ITEM = 'rates'

GET_PAIR = 'pair'
GET_BASE_CURRENCY = 'base_currency_price'

CURRENCY_TO_SPEND = 'currency_to_spend'
CURRENCY_TO_GET = 'currency_to_get'
PAIR_NAME = 'name'
