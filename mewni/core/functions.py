from ..utils import fmt
from aiogram import types
import asyncio

from .app import get_bot, get_app
from .ctx import message


#  TODO: Make arguments more simple for answer, ask_chat, ask functions, remove doesn't needless arguments
async def _send(
        text: str,
        web_preview: bool = True,
        notify: bool = True,
        protect: bool = False,
        reply_: bool = False,
        chat: int | str | None = None,
) -> types.Message:
    PARSE_MODE = 'Markdown'
    """
    Send the message with text
    :param text: message text
    :param web_preview: web preview for links
    :param notify: send the message silently
    :param protect: protect content for copping and sharing
    :param chat: `None` if your want to answer for a previous user message else user id or @username
    :return:
    """
    if chat is not None:
        return await get_bot().bot.send_message(
            chat_id=chat,
            text=fmt.multiline(text),
            disable_web_page_preview=None if web_preview is None else not web_preview,
            disable_notification=None if notify is None else not notify,
            protect_content=protect,
            parse_mode=PARSE_MODE
        )
    return await message().answer(
        text=fmt.multiline(text),
        disable_web_page_preview=web_preview,
        disable_notification=notify,
        protect_content=protect,
        reply=reply_,
        parse_mode=PARSE_MODE
    )
#  TODO: rename anwere to sendtext


async def send(
        text: str,
        web_preview: bool = True,
        notify: bool = True,
        protect: bool = False,
        chat: int | str | None = None,
):
    return await _send(
        text,
        web_preview,
        notify,
        protect,
        False,
        chat,
    )


async def reply(
    text: str,
    web_preview: bool = True,
    notify: bool = True,
    protect: bool = False,
    chat: int | str | None = None
):
    """
    Send reply message for previously message.
    :return:
    """
    return await _send(
        text,
        web_preview,
        notify,
        protect,
        True,
        chat,
    )


async def ask_chat(chat_id, text) -> types.Message:
    await send(text, chat=chat_id)

    future: asyncio.Future[types.Message] = asyncio.get_event_loop().create_future()

    app = get_app()
    app.register.ask_data_middleware.subscribe(chat_id, future)

    return await future


async def ask(text, chat: int | str | None = None) -> types.Message:
    """
    Send user a message with text argument and await for response from user.
    :param text: asking text
    :param chat: chat to sending. If None then send to chat from context
    :return: response message from user
    """
    # Fixme: need to stop event propagation message in AskDataMiddleware
    if chat is not None:
        return await ask(text, chat)
    msg = message()
    return await ask_chat(msg.chat.id, text)
