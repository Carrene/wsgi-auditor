from .context import context as AuditLogContext


class MiddleWareFactory:

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, wsgi_application):
        return self._auditlog_middleware(wsgi_application)

    def _auditlog_middleware(self, wsgi_application):

        def wrapper(environ, start_response):
            def start_response_wrapper(status, headers):
                AuditLogContext.append_request(environ, status)
                self.callback(AuditLogContext.audit_logs)
                return start_response(status, headers)

            return wsgi_application(environ, start_response_wrapper)

        return wrapper

