from sqlalchemy.event import listen
from sqlalchemy.orm import RelationshipProperty, ColumnProperty
from restfulpy.orm import DBSession
from nanohttp import context

from . import context as AuditLogContext


def observe(model, exclude=None):

    listen(model, 'after_insert', after_insert, propagate=True)

    for column in model.iter_columns():
        if hasattr(column, 'property') and \
            isinstance(column.property, RelationshipProperty):
                listen(column, 'append', append_handler)
                listen(column, 'remove', remove_handler)

        elif hasattr(column, 'property') and \
            isinstance(column.property, ColumnProperty) and \
            column.key not in exclude:
                listen(column, 'set', change_attribute, propagate=True)


def after_insert(mapper, connection, target):
    try:
        email = context.identity.email

    except:
        email = 'anonymous'

    AuditLogContext.append_instantiation(user=email, obj=target)


def change_attribute(target, value, oldvalue, initiator):
    if target in DBSession and value != oldvalue:
        AuditLogContext.append_change_attribute(
            user=context.identity.email,
            obj=target,
            attribute=initiator.key,
            old_value=oldvalue,
            new_value=value,
        )


def append_handler(target, value, initiator):
    AuditLogContext.append(
        user=context.identity.email,
        obj=target,
        attribute=initiator.key,
        value=value.title,
    )


def remove_handler(target, value, initiator):
    AuditLogContext.remove(
        user=context.identity.email,
        obj=target,
        attribute=initiator.key,
        value=value.title,
    )

