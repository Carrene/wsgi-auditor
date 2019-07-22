from sqlalchemy.event import listen
from sqlalchemy.orm import RelationshipProperty, ColumnProperty
from restfulpy.orm import DBSession
from restfulpy.helpers import to_camel_case
from nanohttp import context

from . import context as AuditLogContext


def observe(model, exclude=None):

    listen(model, 'after_insert', after_insert_handler, propagate=True)

    for column in model.iter_columns():
        if hasattr(column, 'property') and \
            isinstance(column.property, RelationshipProperty):
                listen(column, 'append', append_handler)
                listen(column, 'remove', remove_handler)

        elif hasattr(column, 'property') and \
            isinstance(column.property, ColumnProperty) and \
            column.key not in exclude:
                listen(column, 'set', set_handler, propagate=True)


def after_insert_handler(mapper, connection, target):
    try:
        email = context.identity.email

    except:
        email = 'anonymous'

    AuditLogContext.append_instantiation(user=email, object_=target)


def set_handler(target, value, oldvalue, initiator):
    if target in DBSession and value != oldvalue:
        target_key = to_camel_case(initiator.key)
        target_label = target.json_metadata()['fields'][target_key]['label']

        AuditLogContext.append_change_attribute(
            user=context.identity.email,
            object_=target,
            attribute_key=target_key,
            attribute_label=target_label,
            old_value=oldvalue,
            new_value=value,
        )


def append_handler(target, value, initiator):
    if target in DBSession:
        target_key = to_camel_case(initiator.key)
        target_label = target.json_metadata()['fields'][target_key]['label']

        AuditLogContext.append(
            user=context.identity.email,
            object_=target,
            attribute_key=target_key,
            attribute_label=target_label,
            value=value.title,
        )


def remove_handler(target, value, initiator):
    if target in DBSession:
        target_key = to_camel_case(initiator.key)
        target_label = target.json_metadata()['fields'][target_key]['label']

        AuditLogContext.remove(
            user=context.identity.email,
            object_=target,
            attribute_key=target_key,
            attribute_label=target_label,
            value=value.title,
        )

