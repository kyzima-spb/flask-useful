import inspect

from flask.cli import AppGroup
from werkzeug.utils import find_modules, import_string


__all__ = (
    'register_blueprints', 'register_commands', 'register_extensions',
)


def get_import_prefix(app):
    if app.import_name == '__main__':
        return ''
    return f'{app.import_name}.'


def register_blueprints(app, import_path):
    """Registers Blueprint for the specified application.

    The argument `import_path` must be a valid import name for the package that contains the modules.
    One module - one Blueprint.
    The variable named `bp` must contain an instance of Blueprint.

    If the `BLUEPRINT_DISABLED` attribute is set in the module, then Blueprint will be ignored.
    """
    for name in find_modules(get_import_prefix(app) + import_path):
        mod = import_string(name)

        if hasattr(mod, 'bp') and not getattr(mod.bp, 'BLUEPRINT_DISABLED', False):
            app.register_blueprint(mod.bp)

            for url_prefix in getattr(mod.bp, 'BLUEPRINT_URL_PREFIXES', []):
                app.register_blueprint(mod.bp, url_prefix=url_prefix)


def register_commands(app, import_name):
    """Initializes console commands found at the specified import path.

    If the __all__ attribute is specified in the module,
    it will be used to fund commands.
    Otherwise, the search is performed using the `dir` function.

    Command is an object inherited from `flask.cli.AppGroup`.
    """
    m = import_string(get_import_prefix(app) + import_name)

    for name in getattr(m, '__all__', dir(m)):
        prop = getattr(m, name)

        if isinstance(prop, AppGroup):
            app.cli.add_command(prop)


def register_extensions(app, import_name):
    """Initializes all Flask extensions found in the specified import path.

    If the __all__ attribute is specified in the module,
    it will be used to search for extension instances.
    Otherwise, the search is performed using the `dir` function.

    An extension is an object that has an init_app method.
    """
    m = import_string(get_import_prefix(app) + import_name)

    for name in getattr(m, '__all__', dir(m)):
        prop = getattr(m, name)
        init_app = getattr(prop, 'init_app', None)

        if inspect.ismethod(init_app):
            init_app(app)
