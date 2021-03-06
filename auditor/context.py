import threading

from .logentry import RequestLogEntry, ChangeAttributeLogEntry, \
    InstantiationLogEntry, AppendLogEntry, RemoveLogEntry


AUDIT_LOG_KEY = 'AUDIT_LOG'


class ContextIsNotInitializedError(Exception):
    pass


class ContextStack(list):

    def push(self, item):
        self.append(item)


class Context:

    #: Thread local variable contexts stored in
    thread_local = threading.local()

    def __call__(self, f):
        def wrapper(*args, **kw):
            with self:
                return f(*args, **kw)

        return wrapper

    @property
    def __stack__(self):
        """Nested contexts stack
        """
        THREADLOCAL_STACK_ATTRIBUTE = 'audit_log_context_stack'
        if not hasattr(self.thread_local, THREADLOCAL_STACK_ATTRIBUTE):
            setattr(
                self.thread_local, THREADLOCAL_STACK_ATTRIBUTE, ContextStack()
            )

        return getattr(self.thread_local, THREADLOCAL_STACK_ATTRIBUTE)

    def __init__(self, environ):
        """
        :param environ: WSGI environ dictionary
        """
        self.environ = environ
        self._audit_logs = []

    def __enter__(self):
        # Backing up the current context
        if hasattr(self.thread_local, 'audit_log_context'):
            self.__stack__.push(self.thread_local.audit_log_context)

        self.thread_local.audit_log_context = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.thread_local.audit_log_context
        if self.__stack__:
            self.thread_local.audit_log_context = self.__stack__.pop()

    @classmethod
    def get_current(cls) -> 'Context':
        """Get current context
            Not initialized context raises
            :class:`.ContextIsNotInitializedError`,
        """
        if not hasattr(cls.thread_local, 'audit_log_context'):
            raise ContextIsNotInitializedError(
                'Context is not initialized yet.'
            )

        return cls.thread_local.audit_log_context

    @property
    def audit_logs(self):
        return self.environ.setdefault(AUDIT_LOG_KEY, self._audit_logs)

    def append_request(self, environ, status):
        request_log_entry = RequestLogEntry(environ, status)
        self._audit_logs.append(request_log_entry)

    def append_change_attribute(self, user, object_, attribute_key,
                                attribute_label, old_value, new_value):

        self._audit_logs.append(ChangeAttributeLogEntry(
            user,
            object_,
            attribute_key,
            attribute_label,
            old_value,
            new_value
        ))

    def append_instantiation(self, user, object_):
        self._audit_logs.append(InstantiationLogEntry(user, object_))

    def append(self, user, object_, attribute_key, attribute_label, value):

        self._audit_logs.append(AppendLogEntry(
            user,
            object_,
            attribute_key,
            attribute_label,
            value,
        ))

    def remove(self, user, object_, attribute_key, attribute_label, value):

        self._audit_logs.append(RemoveLogEntry(
            user,
            object_,
            attribute_key,
            attribute_label,
            value,
        ))


class ContextProxy(Context):

    def __new__(cls) -> Context:
        type_proxy = type('ContextProxy', (object, ), {
            '__getattr__': cls.__getattr__,
            '__setattr__': cls.__setattr__,
            '__delattr__': cls.__delattr__
        })
        return object.__new__(type_proxy)

    def __getattr__(self, key):
        return getattr(Context.get_current(), key)

    def __setattr__(self, key, value):
        setattr(Context.get_current(), key, value)

    def __delattr__(self, key):
        delattr(Context.get_current(), key)


context = ContextProxy()

