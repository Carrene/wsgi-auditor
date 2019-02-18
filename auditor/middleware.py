from .context import context as AuditLogContext, Context


class MiddleWare:

    def __init__(self, wsgi_application, callback):
        self.underlying_application = wsgi_application
        self.callback = callback

    def __call__(self, environ, start_response):
        with Context(environ):

            def start_response_wrapper(status, headers, exc_info=None):

                AuditLogContext.append_request(environ, status)
                self.callback(AuditLogContext.audit_logs)
                result = start_response(status, headers)

            return self.underlying_application(environ, start_response_wrapper)


    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)

        except AttributeError:
            return self.underlying_application.__getattribute__(name)

