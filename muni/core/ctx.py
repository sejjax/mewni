from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from werkzeug.local import LocalStack, LocalProxy, release_local

#  Context object for storing request data
_request = LocalStack()


#  TODO: Test working context with different users and fix it
def message() -> Message:
    """
    Return request message from context (like request() in Flask)
    :return: request message
    """
    if not hasattr(_request, 'message'):
        raise RuntimeError('message function must used in request context')
    return getattr(_request, 'message')


class OpenContextMiddleware(BaseMiddleware):
    """
    Middleware for creating request context per each request.
    """
    async def on_process_message(self, msg: Message, _):
        _request.message = msg


class CloseContextMiddleware(BaseMiddleware):
    """
    Middleware for destroying request context after all handlers and middlewares.
    """
    async def on_process_message(self, _, __):
        release_local(_request)


class State:
    type: any
    storage = {}

    def __init__(self):
        pass

    def __setattr__(self, key, value):
        msg = message()
        # if storage has not instanced in storage for user then create it
        if not hasattr(self.storage, msg.chat.id):
            self.storage[msg.chat.id] = self.type()
        setattr(self.storage[msg.chat.id], key, value)

    def __delattr__(self, item):
        del self.storage[item][item]

    def __getattr__(self, item):
        msg = message()
        return self.storage[msg.chat.id][item]
