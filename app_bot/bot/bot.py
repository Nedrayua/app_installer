
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from mongoengine.errors import NotUniqueError, ValidationError
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware


import bot.constance as co
from bot.utils import inline_kb, generate_datas, take_message
from models.models import User
from states.states import FormAnswer
from datataker import datataker as dt
from bot.config import BOT_TOKEN

CHECK_TRACKING = {}

# об'єкт бота
bot = Bot(BOT_TOKEN)
# appointment memory storage
storage = MemoryStorage()
# Диспечер для бота
dp = Dispatcher(bot, storage=storage)
# liging
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# -------------------------------------------------------------------------------------------
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Create template of replay keyboard
        - Personal data
        - Currency
        - ...
    """

    name = f', {message.from_user.first_name}' if getattr(message.from_user, 'first_name') else '!'
    try:
        User.objects.create(
            telegram_id=message.chat.id,
            username=getattr(message.from_user, 'username', None),
            first_name=getattr(message.from_user, 'first_name', None)
        )
    except NotUniqueError:
        greetings = co.GREETINGS_AGAIN.format(name)
    else:
        greetings = co.GREETINGS_FIRST .format(name)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(b) for b in co.MAIN_MENU.values()]
    kb.add(*buttons)

    await message.answer(text=greetings, reply_markup=kb)

# -------------------------------------------------------------------------------------
# Currency category


@dp.message_handler(lambda m: co.MAIN_MENU[co.currency_tag] == m.text)
async def cmd_start(message: types.Message):
    """
    Redirect to currency category
    """
    data = [
        {'tag': co.currency_one_to_one_tag},
        {'tag': co.currency_one_to_many_tag}]
    text = [co.ONE_TO_ONE_BUTTON, co.ONE_TO_MANY_BUTTON]

    keyboard = inline_kb(data, text)
    await message.answer('Choice:', reply_markup=keyboard)


@dp.message_handler(commands=co.MAIN_MENU[co.settings_tag])
async def cmd_start(message: types.Message):
    """
    Redirect to settings
    """
    data = {
        'tag': co.settings_tag
    }
    text = co.SETTINGS_BUTTON
    keyboard = inline_kb(data, text)
    await message.answer('Choice:', reply_markup=keyboard)


# ============================================================================
# Currency sector
# ----------------------------------------------------------------------------
# One to one


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.currency_one_to_one_tag)
async def currency_list_oto(call:types.CallbackQuery):
    """
    Give a list with awaliable currencies for one to one value
    """
    data = await dt.DataTaker.main_currency_list()
    
    datas, texts, message_text = generate_datas(
        data=data,
        message_if_correct=co.MESSAGE_SPEND_CURRENCY,
        tag=co.currency_list_pairs_tag,
        key=co.CURRENCY_ITEM
    )
    keyboard = inline_kb(datas,texts)

    await bot.edit_message_text(
        text=message_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard
        )


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.currency_list_pairs_tag)
async def get_awaliable_pairs(call:types.CallbackQuery):
    """
    Getting avaliable pairs with the selected one above
    """
    val = json.loads(call.data)['val']
    data = await dt.DataTaker.main_active_pair()


    datas = []
    texts = []

    for row in data.get(co.PAIRS_ITEM):
        if row.get(co.CURRENCY_TO_SPEND) == val:
            datas.append({'tag': co.currency_detail_oto_tag, 'val': val, 'pair': row.get(co.PAIR_NAME)})
            texts.append('{0}/{1}: how mach {1} for {0}'.format(row.get(co.CURRENCY_TO_GET), val))
    keyboard = inline_kb(datas,texts)
    message_text = co.MESSAGE_CHOICE_PAIR
    await bot.edit_message_text(
        text=message_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard
        )

@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.currency_detail_oto_tag)
async def get_awaliable_pairs(call:types.CallbackQuery):
    """
    
    """
    call_dict = json.loads(call.data)

    if call_dict.get('comm') == co.stop_tracking_tag:
        CHECK_TRACKING.update({call.from_user.id: co.stop_tracking_tag})
    else:
        CHECK_TRACKING.update({call.from_user.id: co.start_tracking_tag})

    pair = call_dict['pair']
    
    button_data_list = [
        {
        'tag': co.action_oto_tag,
        'pair': pair,
        'comm': co.start_tracking_tag
    }, 
        {
        'tag': co.currency_one_to_one_tag
    }]
    button_text_list = [co.START_TRACKING_BUTTON, co.BASE_CURRENCY_LIST_BUTTON]    
    kb = inline_kb(button_data_list, button_text_list)
    message_text = await take_message(val=pair, oto=True)

    await bot.edit_message_text(
        text=message_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.action_oto_tag)
async def val_tracking(call: types.CallbackQuery):
    """
    Tracking currency with interval? that they in the settings. Default = 1.5 seconds
    """
    call_dict = json.loads(call.data)

    CHECK_TRACKING.update({call.from_user.id: co.start_tracking_tag})

    pair = call_dict['pair']

    button_data_list = [
        {
        'tag': co.currency_detail_oto_tag,
        'pair': pair,
        'comm': co.stop_tracking_tag
    }, 
        {
        'tag': co.currency_one_to_one_tag
    }]
    button_text_list = [co.STOP_TRACKING_BUTTON, co.BASE_CURRENCY_LIST_BUTTON]
    
    kb = inline_kb(button_data_list, button_text_list)
    num = 20
    for n in range(num):

            if CHECK_TRACKING[call.from_user.id] == co.stop_tracking_tag:
                break
            await asyncio.sleep(1.5)
            
            message_text = await take_message(val=pair, oto=True) + f'\nNumber of check {(num - 1) - n}\n'
            
            await bot.edit_message_text(
                text=message_text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=kb
                )

    CHECK_TRACKING.update({call.from_user.id: co.stop_tracking_tag})



# ----------------------------------------------------------------------------
# One to meny

@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.currency_one_to_many_tag)
async def currency_list_otm(call: types.CallbackQuery):
    """
    Give a list with available currencies for one to many
    """
    data = await dt.DataTaker.main_currency_list()
    
    datas, texts, message_text = generate_datas(
        data=data,
        tag=co.currency_detail_otm_tag,
        message_if_correct=co.MESSAGE_ALL_RATES,
        key=co.CURRENCY_ITEM
        )
    keyboard = inline_kb(callback=datas, text=texts)
    
    await bot.edit_message_text(
        text=message_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard
        )


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.currency_detail_otm_tag)
async def work_with_uah(call: types.CallbackQuery):
    """
    Realization of kurrency button, with frize course and two buttons
    with start and stop
    """
    call_dict = json.loads(call.data)

    if call_dict.get('comm') == co.stop_tracking_tag:
        CHECK_TRACKING.update({call.from_user.id: co.stop_tracking_tag})
    else:
        CHECK_TRACKING.update({call.from_user.id: co.start_tracking_tag})

    val = call_dict['val']

    button_data_list = []
    button_data_list.append({
        'tag': co.action_otm_tag,
        'val': val,
        'comm': co.start_tracking_tag
    })
    button_data_list.append({
        'tag': co.currency_one_to_many_tag
    })
    button_text_list = [co.START_TRACKING_BUTTON, co.CURRENCY_LIST_BUTTON]
    
    kb = inline_kb(button_data_list, button_text_list)

    message_text = await take_message(val=val)

    await bot.edit_message_text(
        text=message_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.action_otm_tag)
async def val_tracking(call: types.CallbackQuery):
    """
    Tracking currency with interval? that they in the settings. Default = 1.5 seconds
    """
    call_dict = json.loads(call.data)

    CHECK_TRACKING.update({call.from_user.id: co.start_tracking_tag})

    val = call_dict['val']

    button_data_list = []
    button_data_list.append({
        'tag': co.currency_detail_otm_tag,
        'val': val,
        'comm': co.stop_tracking_tag
    })
    button_data_list.append({
        'tag': co.currency_list_tag
    })
    button_text_list = [co.STOP_TRACKING_BUTTON, co.CURRENCY_LIST_BUTTON]
    
    kb = inline_kb(button_data_list, button_text_list)
    num = 20
    for n in range(num):

            if CHECK_TRACKING[call.from_user.id] == co.stop_tracking_tag:
                break
            await asyncio.sleep(2)
            
            message_text = await take_message(val=val) + f'\nNumber of check {(num - 1) - n}\n'
            
            await bot.edit_message_text(
                text=message_text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=kb
                )

    CHECK_TRACKING.update({call.from_user.id: co.stop_tracking_tag})

#==========================================================================================
# Personal data sector


@dp.message_handler(lambda m: co.MAIN_MENU[co.settings_tag] == m.text)
async def handle_settings(message: types.Message):
    """
    Handler for settings button
    """
    user = User.objects.get(telegram_id=message.chat.id)
    data = user.formatted_data()

    button_data = {'tag': co.change_settings_tag}
    kb = inline_kb(button_data, co.MESSAGE_CHANGE_OWN_INFO)
    await message.answer(
        text=data,
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.change_settings_tag)
async def handle_change_settings(call):
    """
    Execute buttons for personal data of user.
    """
    datas = []
    texts = []

    for com, name_button in co.SETTINGS_BUTTONS.items():
        datas.append({
            'tag': co.change_specific_settings_tag,
            'command': com
        })
        texts.append(name_button)

    keyboard = inline_kb(datas, texts)

    user = User.objects.get(telegram_id=call.from_user.id)
    user_data = user.formatted_data()
    await bot.edit_message_text(
        text=f'{user_data}\n\n{co.MESSAGE_CHOISE_SPECIFIC_CATEGORY}:',
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda call: json.loads(call.data)['tag'] == co.change_specific_settings_tag)
async def handler_change_specific_settings(call):
    """
    Processor of personal data changes
    """
    call_dict = json.loads(call.data)
    if call_dict['command'] == co.change_name:
        await bot.send_message(call.message.chat.id, co.CHANGE_SETTINGS_MESSAGES[call_dict['command']])
        await FormAnswer.change_name.set()

    elif call_dict['command'] == co.change_phone:
        await bot.send_message(call.message.chat.id, co.CHANGE_SETTINGS_MESSAGES[call_dict['command']])
        await FormAnswer.change_phone.set()

    elif call_dict['command'] == co.change_email:
        await bot.send_message(call.message.chat.id, co.CHANGE_SETTINGS_MESSAGES[call_dict['command']])
        await FormAnswer.change_email.set()

    elif call_dict['command'] == co.change_city:
        await bot.send_message(call.message.chat.id, co.CHANGE_SETTINGS_MESSAGES[call_dict['command']])
        await FormAnswer.change_city.set()


@dp.message_handler(state=FormAnswer.change_name)
async def handle_change_first_name(message:types.Message, state:FSMContext ):        
    """
    Execute change name user
    """
    user = User.objects.get(telegram_id=message.from_user.id)
    try:
        user.first_name = message.text
        user.save()
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.complete_change]
    except ValidationError:
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.wrong_change]
    data = {'tag': co.change_settings_tag}
    kb = inline_kb(data, co.SETTINGS_BUTTONS[co.back_to_settings])
    await bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )
    await state.finish()


@dp.message_handler(state=FormAnswer.change_phone)
async def handle_change_phone(message:types.Message, state:FSMContext):
    """
    Execute change phone_number
    """
    user = User.objects.get(telegram_id=message.from_user.id)
    try:
        user.phone_number = message.text
        user.save()
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.complete_change]
    except ValidationError:
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.wrong_change]

    data = {'tag': co.change_settings_tag}
    kb = inline_kb(data, co.SETTINGS_BUTTONS[co.back_to_settings])
    await bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )
    await state.finish()


@dp.message_handler(state=FormAnswer.change_email)
async def handle_change_email(message:types.Message, state:FSMContext):
    """
    Execute change user email
    """
    user = User.objects.get(telegram_id=message.from_user.id)
    try:
        user.email = message.text
        user.save()
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.complete_change]
    except ValidationError:
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.wrong_change]

    data = {'tag': co.change_settings_tag}
    kb = inline_kb(data, co.SETTINGS_BUTTONS[co.back_to_settings])
    await bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )
    await state.finish()


@dp.message_handler(state=FormAnswer.change_city)
async def handle_change_city(message:types.Message, state:FSMContext):
    """
    Execute change user city
    """
    user = User.objects.get(telegram_id=message.from_user.id)
    try:
        user.user_city = message.text
        user.save()
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.complete_change]
    except ValidationError:
        message_text = co.CHANGE_SETTINGS_MESSAGES[co.wrong_change]

    data = {'tag': co.change_settings_tag}
    kb = inline_kb(data, co.CHANGE_SETTINGS_NAMES_B[co.back_to_settings])
    await bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )
    await state.finish()
