from functools import wraps
from .model.system import Permission
from .verify import signature_verify, permission_verify


def signature_required(f):
    """
    要求接口签名
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        signature_verify()
        return f(*args, **kwargs)
    return decorated


def permission_required(permission):
    """
    要求接口具备指定权限
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            permission_verify(permission)
            return f(*args, **kwargs)
        return decorated
    return decorator


def admin_required(f):
    """
    要求接口具备超级管理员权限
    """
    return permission_required(Permission.ADMIN)(f)
