from .utils import camel_to_snake


__all__ = (
    'route',
)


def route(obj, rule, *args, **kwargs):
    """Decorator for the View classes."""
    def decorator(cls):
        endpoint = kwargs.get('endpoint', camel_to_snake(cls.__name__))
        kwargs['view_func'] = cls.as_view(endpoint)
        obj.add_url_rule(rule, *args, **kwargs)
        return cls
    return decorator
