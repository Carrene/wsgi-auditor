from bddrest import Given, status

from auditing.context import Context as AuditLogContext, context
from auditing.middleware import MiddleWare
from auditing.logentry import ChangeAttributeLogEntry


def wsgi_application(env, start_response):
    with AuditLogContext(env):
        old = dict(a=1, b=2, c=3)
        new = dict(a=1, b=2, c=4, d=None)

        context.append_change_attribute('anonymous', old, new)

        start_response(
            '200 OK',
            [('content-type', 'text/plain;charset=utf-8')]
        )

        return [b'Index']


class TestContext:

    def test_append_change_attribute(self):
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

