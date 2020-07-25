from flask import (
    current_app, redirect, url_for, request
)


def get_route_param_names(endpoint):
    """
    Returns parameter names from the route.

    Arguments:
        endpoint (str): The absolute name of the endpoint.
    """
    try:
        g = current_app.url_map.iter_rules(endpoint)
        return next(g).arguments
    except KeyError:
        return {}


def make_redirect(actions, params, _name='action'):
    """
    Depending on the button pressed in the form, it creates a 302 redirect.

    Example:
        from functools import partial

        post_redirect = partial(make_redirect, {
            'Save': 'update',
            'Save and Create': 'create',
            'Save and Close': 'index',
        })

        @app.route('/create')
        def create():
            # ...
            if form.validate_on_submit():
                product = Product()
                form.populate_obj(product)
                db.session.add(product)
                db.session.commit()
                return make_redirect(product)
            # ...
    """
    endpoint = actions[request.form.get(_name)]
    kwargs = {}

    for name in get_route_param_names(endpoint):
        if isinstance(params, dict):
            kwargs[name] = params.get(name)
        else:
            kwargs[name] = getattr(params, name, None)

    return redirect(url_for(endpoint, **kwargs))
