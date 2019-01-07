class LogEntry:
    pass


class RequestLogEntry(LogEntry):

    def __init__(self, environ, status):
        self.verb = environ['REQUEST_METHOD']
        self.url = environ['HTTP_HOST']
        self.path_info = environ['PATH_INFO']
        self.status = status
        self.query_string = environ['QUERY_STRING'] \
            if 'QUERY_STRING' in environ else None
        self.authorization = environ['HTTP_AUTHORIZATION'] \
            if 'HTTP_AUTHORIZATION' in environ else None


class ChangeAttributeLogEntry(LogEntry):

    def __init__(self, who, attribute, old_value, new_value):
        self.who = who
        self.attribute = attribute
        self.old_value = old_value
        self.new_value = new_value

