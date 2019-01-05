from . import AUDIT_LOG_KEY
from .logentry import RequestLogEntry


class Context:

    def append_request(cls, environ, status):
        request_log_entry = RequestLogEntry(environ, status)
        environ[AUDIT_LOG_KEY].append(request_log_entry)


class ContextProxy(Context):

    # noinspection PyInitNewSignature
    def __new__(cls) -> Context:
        type_proxy = type('ContextProxy', (object, ), {
            '__getattr__': cls.__getattr__,
            '__setattr__': cls.__setattr__,
            '__delattr__': cls.__delattr__
        })
        # noinspection PyTypeChecker
        return object.__new__(type_proxy)

    def __getattr__(self, key):
        return getattr(Context.get_current(), key)

    def __setattr__(self, key, value):
        setattr(Context.get_current(), key, value)

    def __delattr__(self, key):
        delattr(Context.get_current(), key)


context = ContextProxy()

