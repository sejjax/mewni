import typing

from aiogram.types import base
from aiogram import types

from .app import get_bot
from .ctx import message


async def answer(text: base.String,
                 parse_mode: typing.Optional[base.String] = None,
                 entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                 disable_web_page_preview: typing.Optional[base.Boolean] = None,
                 disable_notification: typing.Optional[base.Boolean] = None,
                 protect_content: typing.Optional[base.Boolean] = None,
                 allow_sending_without_reply: typing.Optional[base.Boolean] = None,
                 reply_markup: typing.Union[
                     types.InlineKeyboardMarkup,
                     types.ReplyKeyboardMarkup,
                     types.ReplyKeyboardRemove,
                     types.ForceReply,
                     None,
                 ] = None,
                 reply: base.Boolean = False) -> types.Message:
    return await message().answer(
        text,
        parse_mode,
        entities,
        disable_web_page_preview,
        disable_notification,
        protect_content,
        allow_sending_without_reply,
        reply_markup,
        reply
    )


async def send_message(
        chat_id: typing.Union[base.Integer, base.String],
        text: base.String,
        parse_mode: typing.Optional[base.String] = None,
        entities: typing.Optional[typing.List[types.MessageEntity]] = None,
        disable_web_page_preview: typing.Optional[base.Boolean] = None,
        disable_notification: typing.Optional[base.Boolean] = None,
        protect_content: typing.Optional[base.Boolean] = None,
        reply_to_message_id: typing.Optional[base.Integer] = None,
        allow_sending_without_reply: typing.Optional[base.Boolean] = None,
        reply_markup: typing.Union[types.InlineKeyboardMarkup,
                                   types.ReplyKeyboardMarkup,
                                   types.ReplyKeyboardRemove,
                                   types.ForceReply, None] = None
) -> types.Message:
    bot = get_bot()
    return await bot.send_message(
        chat_id,
        text,
        parse_mode,
        entities,
        disable_web_page_preview,
        disable_notification,
        protect_content,
        reply_to_message_id,
        allow_sending_without_reply,
        reply_markup
    )
