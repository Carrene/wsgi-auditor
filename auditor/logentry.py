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

    def __init__(self, user, object_, attribute_key, attribute_label,
                 old_value, new_value):
        self.user = user
        self.object_ = object_
        self.attribute_key = attribute_key
        self.attribute_label = attribute_label
        self.old_value = old_value
        self.new_value = new_value


class InstantiationLogEntry(LogEntry):

    def __init__(self, user, object_):
        self.user = user
        self.object_ = object_


class AppendLogEntry(LogEntry):

    def __init__(self, user, object_, attribute_key, attribute_label, value):
        self.user = user
        self.object_ = object_
        self.attribute_key = attribute_key
        self.attribute_label = attribute_label
        self.value = value


class RemoveLogEntry(LogEntry):

    def __init__(self, user, object_, attribute_key, attribute_label, value):
        self.user = user
        self.object_ = object_
        self.attribute_key = attribute_key
        self.attribute_label = attribute_label
        self.value = value

