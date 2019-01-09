from bddrest import Given, status, response
import pytest

from auditing.context import Context as AuditLogContext, context
from auditing.middleware import MiddleWare
from auditing.logentry import ChangeAttributeLogEntry


class ModelObject:

    def __init__(self, a):
        self.a = a


def wsgi_application(env, start_response):
    with AuditLogContext(env):

        obj = ModelObject(a=1)
        context.append_change_attribute('anonymous', obj, 'a', 1, 11)

        start_response('200 OK', [('content-type', 'text/plain;charset=utf-8')])
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
            title='Testing the append change attribute method',
            url='/apiv1',
            verb=self.verb,
        )
        with Given(app, **call):
            assert status == 200
            assert len(self.log) == 2

