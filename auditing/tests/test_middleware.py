from bddrest import Given, status

from auditing.middleware import MiddleWare


def wsgi_application(env, start_response):
    start_response('200 OK', [('content-type', 'text/plain;charset=utf-8')])
    return [b'Index']


def test_middleware():

    def callback(audit_logs):
        for log in audit_logs:
            print(log.__dict__)

    middleware = MiddleWare(callback)

    app = middleware(wsgi_application)
    call = dict(
        title='',
        description='',
        url='/apiv1/device',
        verb='POST',
    )
    with Given(app, **call):
        assert status == 200

