from bddrest import Given, status

from auditing.context import Context as AuditLogContext
from auditing.middleware import MiddleWare


def wsgi_application(env, start_response):
    with AuditLogContext(env):
        start_response(
            '200 OK',
            [('content-type', 'text/plain;charset=utf-8')]
        )
        return [b'Index']


class TestContext:

    def test_append_request(self):
        self.log = None
        self.verb = 'POST'

        def callback(audit_logs):
            self.log = audit_logs

        middleware = MiddleWare(callback)

        app = middleware(wsgi_application)
        call = dict(
            title='Testing the append request method',
            url='/apiv1/device',
            verb=self.verb,
        )
        with Given(app, **call):
            assert status == 200

            assert self.log[0].verb == self.verb
            assert self.log[0].status == '200 OK'
            assert self.log[0].query_string is None
            assert self.log[0].authorization is None

