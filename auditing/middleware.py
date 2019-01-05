from . import AUDIT_LOG_KEY
from .context import Context as AuditLogContext


class MiddleWare:

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, wsgi_application):
        return self._auditlog_middleware(wsgi_application)

    def _auditlog_middleware(self, wsgi_application):

        def wrapper(environ, start_response):

            environ[AUDIT_LOG_KEY] = []

            def start_response_wrapper(status, headers):
                AuditLogContext.append_request(environ, status)
                self.callback(environ[AUDIT_LOG_KEY])
                return start_response(status, headers)

            return wsgi_application(environ, start_response_wrapper)

        return wrapper

